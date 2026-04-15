#!/usr/bin/env python3
"""
Minimal Sentry API helper for triage/debugging.

Auth:
  - Set SENTRY_AUTH_TOKEN (recommended; avoids shell history leaks)
  - Optional: SENTRY_BASE_URL (default: https://sentry.io)
  - Optional: SENTRY_ORG and SENTRY_PROJECT defaults

Examples:
  python3 scripts/sentry.py whoami
  python3 scripts/sentry.py issues --limit 20
  python3 scripts/sentry.py issue --issue-id 123456789
  python3 scripts/sentry.py event-latest --issue-id 123456789 --frames 16
  python3 scripts/sentry.py report --limit 15 > sentry-report.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Iterable, Iterator


DEFAULT_BASE_URL = "https://sentry.io"
API_PREFIX = "/api/0"


class SentryApiError(RuntimeError):
    pass


@dataclass(frozen=True)
class Config:
    base_url: str
    auth_token: str
    org: str | None
    project: str | None


def _env(name: str) -> str | None:
    value = os.environ.get(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


def load_config(args: argparse.Namespace) -> Config:
    base_url = (args.base_url or _env("SENTRY_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    auth_token = args.auth_token or _env("SENTRY_AUTH_TOKEN") or ""
    org = args.org or _env("SENTRY_ORG")
    project = args.project or _env("SENTRY_PROJECT")
    return Config(base_url=base_url, auth_token=auth_token, org=org, project=project)


def require_auth(config: Config) -> None:
    if not config.auth_token:
        raise SentryApiError(
            "Missing SENTRY_AUTH_TOKEN (set env var; avoid passing via CLI to prevent leaking to shell history)."
        )


def require_project(config: Config) -> tuple[str, str]:
    if not config.org or not config.project:
        raise SentryApiError(
            "Missing SENTRY_ORG and/or SENTRY_PROJECT. Set env vars or pass --org/--project."
        )
    return config.org, config.project


def build_api_url(config: Config, api_path: str, params: dict[str, Any] | None = None) -> str:
    if not api_path.startswith("/"):
        api_path = "/" + api_path
    url = f"{config.base_url}{API_PREFIX}{api_path}"
    if params:
        # Drop None values
        clean = {k: v for k, v in params.items() if v is not None}
        if clean:
            url = f"{url}?{urllib.parse.urlencode(clean, doseq=True)}"
    return url


def _request_json(
    config: Config,
    method: str,
    api_path: str,
    params: dict[str, Any] | None = None,
) -> tuple[Any, dict[str, str]]:
    require_auth(config)
    url = build_api_url(config, api_path, params)
    req = urllib.request.Request(
        url,
        method=method.upper(),
        headers={
            "Authorization": f"Bearer {config.auth_token}",
            "Accept": "application/json",
            "User-Agent": "codex-sentry-debugger/1.0",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace").strip()
            headers = {k: v for k, v in resp.headers.items()}
            if not body:
                return None, headers
            try:
                return json.loads(body), headers
            except json.JSONDecodeError as exc:
                raise SentryApiError(f"Non-JSON response from Sentry API ({exc}): {body[:2000]}")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        msg = f"Sentry API error {exc.code} for {url}"
        try:
            payload = json.loads(raw)
            detail = payload.get("detail") or payload.get("error") or payload
            msg = f"{msg}: {detail}"
        except Exception:
            if raw.strip():
                msg = f"{msg}: {raw.strip()[:2000]}"
        raise SentryApiError(msg) from exc
    except urllib.error.URLError as exc:
        raise SentryApiError(f"Network error calling Sentry API: {exc}") from exc


_LINK_RE = re.compile(r'<(?P<url>[^>]+)>;\s*rel="(?P<rel>[^"]+)"(?P<rest>.*)$')
_CURSOR_RE = re.compile(r'cursor="(?P<cursor>[^"]+)"')
_RESULTS_RE = re.compile(r'results="(?P<results>true|false)"')


def _next_cursor_from_link_header(link_header: str | None) -> str | None:
    if not link_header:
        return None

    parts = [p.strip() for p in link_header.split(",") if p.strip()]
    for part in parts:
        m = _LINK_RE.match(part)
        if not m:
            continue
        if m.group("rel") != "next":
            continue
        rest = m.group("rest")
        results_m = _RESULTS_RE.search(rest)
        if results_m and results_m.group("results") != "true":
            return None
        cursor_m = _CURSOR_RE.search(rest)
        if cursor_m:
            return cursor_m.group("cursor")

        # Fallback: parse cursor from URL query
        try:
            parsed = urllib.parse.urlparse(m.group("url"))
            qs = urllib.parse.parse_qs(parsed.query)
            cursor_vals = qs.get("cursor")
            if cursor_vals:
                return cursor_vals[0]
        except Exception:
            pass

    return None


def _paginate(
    config: Config,
    api_path: str,
    params: dict[str, Any] | None,
    limit: int,
) -> Iterator[Any]:
    remaining = max(limit, 0)
    cursor: str | None = None
    per_page = 100 if remaining == 0 else min(100, remaining)

    while True:
        page_params = dict(params or {})
        page_params["per_page"] = per_page
        if cursor:
            page_params["cursor"] = cursor

        data, headers = _request_json(config, "GET", api_path, page_params)
        if not isinstance(data, list):
            raise SentryApiError(f"Expected list response from {api_path}, got {type(data).__name__}")

        for item in data:
            yield item
            if remaining:
                remaining -= 1
                if remaining <= 0:
                    return

        cursor = _next_cursor_from_link_header(headers.get("Link"))
        if not cursor:
            return


def _iso_to_local(iso: str | None) -> str:
    if not iso:
        return "?"
    # Keep this stable: avoid locale-specific formatting.
    try:
        parsed = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return parsed.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception:
        return iso


def _truncate(s: str, n: int) -> str:
    s = s.replace("\n", " ").strip()
    if len(s) <= n:
        return s
    return s[: max(0, n - 1)].rstrip() + "…"


def cmd_whoami(config: Config, args: argparse.Namespace) -> int:
    me, _headers = _request_json(config, "GET", "/users/me/")
    if args.format == "json":
        print(json.dumps(me, indent=2, sort_keys=True))
        return 0
    name = (me or {}).get("name") or (me or {}).get("email") or "<unknown>"
    print(name)
    return 0


def cmd_issues(config: Config, args: argparse.Namespace) -> int:
    org, project = require_project(config)
    api_path = f"/projects/{org}/{project}/issues/"

    params: dict[str, Any] = {}
    if args.query:
        params["query"] = args.query

    items = list(_paginate(config, api_path, params, args.limit))
    if args.format == "json":
        print(json.dumps(items, indent=2))
        return 0
    if args.format == "md":
        print(f"# Sentry Issues ({org}/{project})")
        print()
        print("| ID | Level | Count | Last Seen | Title |")
        print("|---:|:------|------:|:----------|:------|")
        for it in items:
            issue_id = it.get("id", "?")
            level = it.get("level", "?")
            count = it.get("count", "?")
            last_seen = _iso_to_local(it.get("lastSeen"))
            title = _truncate(it.get("title") or "", 120)
            print(f"| {issue_id} | {level} | {count} | {last_seen} | {title} |")
        return 0

    for it in items:
        issue_id = it.get("id", "?")
        level = it.get("level", "?")
        count = it.get("count", "?")
        last_seen = _iso_to_local(it.get("lastSeen"))
        title = _truncate(it.get("title") or "", 140)
        print(f"{issue_id}\t{level}\t{count}\t{last_seen}\t{title}")
    return 0


def cmd_issue(config: Config, args: argparse.Namespace) -> int:
    data, _headers = _request_json(config, "GET", f"/issues/{args.issue_id}/")
    if args.format == "json":
        print(json.dumps(data, indent=2))
        return 0
    print(f"ID: {data.get('id')}")
    print(f"Title: {data.get('title')}")
    print(f"Culprit: {data.get('culprit')}")
    print(f"Level: {data.get('level')}")
    print(f"Status: {data.get('status')}")
    print(f"Count: {data.get('count')}")
    print(f"First Seen: {_iso_to_local(data.get('firstSeen'))}")
    print(f"Last Seen: {_iso_to_local(data.get('lastSeen'))}")
    if data.get("permalink"):
        print(f"Permalink: {data.get('permalink')}")
    return 0


def _fetch_event_details(config: Config, issue_id: str, event_id: str) -> Any:
    org = config.org
    project = config.project
    candidates: list[str] = []
    if org and project:
        candidates.append(f"/projects/{org}/{project}/events/{event_id}/")
    if org:
        candidates.append(f"/organizations/{org}/events/{event_id}/")
    candidates.append(f"/issues/{issue_id}/events/{event_id}/")

    last_err: Exception | None = None
    for api_path in candidates:
        try:
            data, _headers = _request_json(config, "GET", api_path)
            return data
        except SentryApiError as exc:
            # Try the next endpoint if this one doesn't exist.
            if "error 404" in str(exc).lower():
                last_err = exc
                continue
            last_err = exc
            break
    raise SentryApiError(
        f"Unable to fetch event details for event_id={event_id}. Last error: {last_err}"
    )


def _extract_exception_entries(event: dict[str, Any]) -> list[dict[str, Any]]:
    entries = event.get("entries") or []
    if not isinstance(entries, list):
        return []
    out: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if entry.get("type") != "exception":
            continue
        data = entry.get("data") or {}
        values = (data.get("values") or []) if isinstance(data, dict) else []
        if not isinstance(values, list):
            continue
        for ex in values:
            if not isinstance(ex, dict):
                continue
            out.append(ex)
    return out


def _format_frame(frame: dict[str, Any]) -> str:
    filename = frame.get("filename") or frame.get("abs_path") or frame.get("module") or "?"
    lineno = frame.get("lineno")
    func = frame.get("function") or frame.get("symbol") or "?"
    in_app = frame.get("in_app")
    in_app_str = "app" if in_app else "dep"
    if lineno is None:
        return f"[{in_app_str}] {filename} :: {func}"
    return f"[{in_app_str}] {filename}:{lineno} :: {func}"


def cmd_event_latest(config: Config, args: argparse.Namespace) -> int:
    issue_id = args.issue_id
    events, _headers = _request_json(
        config,
        "GET",
        f"/issues/{issue_id}/events/",
        params={"per_page": 1},
    )
    if not isinstance(events, list) or not events:
        raise SentryApiError(f"No events found for issue {issue_id}")

    ev = events[0]
    event_id = ev.get("eventID") or ev.get("id")
    if not event_id:
        raise SentryApiError(f"Unable to determine event id from response: {ev}")

    event = _fetch_event_details(config, issue_id=issue_id, event_id=str(event_id))
    if not isinstance(event, dict):
        raise SentryApiError(f"Unexpected event payload type: {type(event).__name__}")

    if args.format == "json":
        print(json.dumps(event, indent=2))
        return 0

    print(f"Issue: {issue_id}")
    print(f"Event: {event_id}")
    if event.get("dateCreated"):
        print(f"Created: {_iso_to_local(event.get('dateCreated'))}")
    if event.get("platform"):
        print(f"Platform: {event.get('platform')}")
    tags = event.get("tags") or []
    if isinstance(tags, list) and tags:
        # Surface high-signal tags if present.
        tag_map = {t.get("key"): t.get("value") for t in tags if isinstance(t, dict)}
        for key in ("environment", "release", "transaction", "url", "runtime"):
            if key in tag_map:
                print(f"{key.capitalize()}: {tag_map[key]}")

    exceptions = _extract_exception_entries(event)
    if not exceptions:
        print()
        print("No exception entry found on this event.")
        return 0

    print()
    for idx, ex in enumerate(exceptions, start=1):
        ex_type = ex.get("type") or "Exception"
        ex_value = ex.get("value") or ""
        print(f"Exception {idx}: {ex_type}: {ex_value}")
        stack = ex.get("stacktrace") or {}
        frames = stack.get("frames") if isinstance(stack, dict) else None
        if not isinstance(frames, list) or not frames:
            continue

        # Prefer in-app frames; fall back to all frames if none are in-app.
        in_app_frames = [f for f in frames if isinstance(f, dict) and f.get("in_app") is True]
        selected = in_app_frames or [f for f in frames if isinstance(f, dict)]
        # Sentry frames are usually oldest->newest; show most recent frames first.
        selected = list(reversed(selected))[: max(0, args.frames)]
        for f in selected:
            print(f"  - {_format_frame(f)}")
        print()

    return 0


def cmd_report(config: Config, args: argparse.Namespace) -> int:
    org, project = require_project(config)
    issues_path = f"/projects/{org}/{project}/issues/"
    params: dict[str, Any] = {}
    if args.query:
        params["query"] = args.query

    issues = list(_paginate(config, issues_path, params, args.limit))

    now = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"# Sentry Triage Report: {org}/{project}")
    print()
    print(f"- Generated: {now}")
    if args.query:
        print(f"- Query: `{args.query}`")
    print()

    for it in issues:
        issue_id = it.get("id", "?")
        title = _truncate(it.get("title") or "", 200)
        level = it.get("level", "?")
        count = it.get("count", "?")
        last_seen = _iso_to_local(it.get("lastSeen"))
        permalink = it.get("permalink")
        print(f"## {title}")
        print()
        print(f"- Issue ID: `{issue_id}`")
        print(f"- Level: `{level}`")
        print(f"- Count: `{count}`")
        print(f"- Last Seen: `{last_seen}`")
        if permalink:
            print(f"- Link: {permalink}")
        print()

    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Sentry API helper for debugging.")
    p.add_argument("--base-url", help="Sentry base URL (default: env SENTRY_BASE_URL or https://sentry.io)")
    p.add_argument("--auth-token", help="Sentry auth token (prefer env SENTRY_AUTH_TOKEN)")
    p.add_argument("--org", help="Sentry organization slug (default: env SENTRY_ORG)")
    p.add_argument("--project", help="Sentry project slug (default: env SENTRY_PROJECT)")

    sub = p.add_subparsers(dest="cmd", required=True)

    whoami = sub.add_parser("whoami", help="Verify auth and print current user")
    whoami.add_argument("--format", choices=("text", "json"), default="text")
    whoami.set_defaults(_fn=cmd_whoami)

    issues = sub.add_parser("issues", help="List issues for the configured project")
    issues.add_argument("--limit", type=int, default=20)
    issues.add_argument("--query", help="Sentry issue search query (e.g. 'is:unresolved')")
    issues.add_argument("--format", choices=("text", "json", "md"), default="text")
    issues.set_defaults(_fn=cmd_issues)

    issue = sub.add_parser("issue", help="Show details for a single issue")
    issue.add_argument("--issue-id", required=True, dest="issue_id")
    issue.add_argument("--format", choices=("text", "json"), default="text")
    issue.set_defaults(_fn=cmd_issue)

    ev = sub.add_parser("event-latest", help="Fetch and summarize the latest event for an issue")
    ev.add_argument("--issue-id", required=True, dest="issue_id")
    ev.add_argument("--frames", type=int, default=12, help="Max frames to print per exception")
    ev.add_argument("--format", choices=("text", "json"), default="text")
    ev.set_defaults(_fn=cmd_event_latest)

    report = sub.add_parser("report", help="Generate a Markdown triage report for issues")
    report.add_argument("--limit", type=int, default=15)
    report.add_argument("--query", help="Sentry issue search query (e.g. 'is:unresolved')")
    report.set_defaults(_fn=cmd_report)

    return p


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_config(args)
    try:
        return args._fn(config, args)
    except SentryApiError as exc:
        print(f"[sentry.py] {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

