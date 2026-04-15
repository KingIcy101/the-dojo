#!/usr/bin/env python3
import argparse
import json
import os
import re
import sqlite3
from pathlib import Path
from typing import Iterable, List, Tuple

import gdown
from ebooklib import epub, ITEM_DOCUMENT
from pypdf import PdfReader

WORD_RE = re.compile(r"[a-zA-Z0-9']+")
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def normalize_ws(text: str) -> str:
    return WS_RE.sub(" ", text).strip()


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in WORD_RE.findall(text)]


def chunk_text(text: str, chunk_size: int = 1400, overlap: int = 240) -> Iterable[Tuple[int, int, str]]:
    text = normalize_ws(text)
    if not text:
        return
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + chunk_size)
        # try to break on punctuation/space for cleaner quotes
        if end < n:
            for sep in [". ", "? ", "! ", "\n", " "]:
                idx = text.rfind(sep, start, end)
                if idx != -1 and idx > start + 400:
                    end = idx + len(sep)
                    break
        yield start, end, text[start:end].strip()
        if end >= n:
            break
        start = max(end - overlap, start + 1)


def init_db(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(
        """
        PRAGMA journal_mode=WAL;
        DROP TABLE IF EXISTS chunks_fts;
        DROP TABLE IF EXISTS chunks;
        DROP TABLE IF EXISTS docs;

        CREATE TABLE docs (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            path TEXT NOT NULL,
            format TEXT NOT NULL
        );

        CREATE TABLE chunks (
            id INTEGER PRIMARY KEY,
            doc_id INTEGER NOT NULL,
            chunk_index INTEGER NOT NULL,
            text TEXT NOT NULL,
            location TEXT NOT NULL,
            token_count INTEGER NOT NULL,
            FOREIGN KEY(doc_id) REFERENCES docs(id)
        );

        CREATE VIRTUAL TABLE chunks_fts USING fts5(
            text,
            content='chunks',
            content_rowid='id'
        );
        """
    )
    conn.commit()
    return conn


def add_chunk(cur, doc_id: int, chunk_index: int, text: str, location: str):
    tc = len(tokenize(text))
    cur.execute(
        "INSERT INTO chunks(doc_id, chunk_index, text, location, token_count) VALUES (?, ?, ?, ?, ?)",
        (doc_id, chunk_index, text, location, tc),
    )
    rowid = cur.lastrowid
    cur.execute("INSERT INTO chunks_fts(rowid, text) VALUES (?, ?)", (rowid, text))


def ingest_pdf(cur, path: Path, doc_id: int):
    reader = PdfReader(str(path))
    chunk_idx = 0
    for i, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        for start, end, ch in chunk_text(raw):
            location = json.dumps({"type": "pdf", "page": i, "char_start": start, "char_end": end})
            add_chunk(cur, doc_id, chunk_idx, ch, location)
            chunk_idx += 1


def ingest_epub(cur, path: Path, doc_id: int):
    book = epub.read_epub(str(path))
    chunk_idx = 0
    sec = 0
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        sec += 1
        raw_html = item.get_body_content().decode("utf-8", errors="ignore")
        txt = normalize_ws(TAG_RE.sub(" ", raw_html))
        for start, end, ch in chunk_text(txt):
            location = json.dumps({"type": "epub", "section": sec, "item": item.file_name, "char_start": start, "char_end": end})
            add_chunk(cur, doc_id, chunk_idx, ch, location)
            chunk_idx += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--drive-url", required=True)
    ap.add_argument("--download-dir", default=str(Path.home() / ".openclaw/skills/podhi-book-quote-rag/data/books_raw"))
    ap.add_argument("--db", default=str(Path.home() / ".openclaw/skills/podhi-book-quote-rag/data/books.db"))
    args = ap.parse_args()

    download_dir = Path(args.download_dir)
    download_dir.mkdir(parents=True, exist_ok=True)

    print("Downloading folder from Drive...")
    gdown.download_folder(url=args.drive_url, output=str(download_dir), quiet=False, use_cookies=False, remaining_ok=True)

    conn = init_db(Path(args.db))
    cur = conn.cursor()

    files = sorted([p for p in download_dir.rglob("*") if p.is_file() and p.suffix.lower() in {".pdf", ".epub"}])
    print(f"Found {len(files)} files to ingest")

    for fp in files:
        fmt = fp.suffix.lower().lstrip(".")
        title = fp.name
        cur.execute("INSERT INTO docs(title, path, format) VALUES (?, ?, ?)", (title, str(fp), fmt))
        doc_id = cur.lastrowid
        print(f"Ingesting: {title}")
        try:
            if fmt == "pdf":
                ingest_pdf(cur, fp, doc_id)
            elif fmt == "epub":
                ingest_epub(cur, fp, doc_id)
        except Exception as e:
            print(f"WARN: failed to ingest {title}: {e}")
    conn.commit()

    total_docs = cur.execute("SELECT COUNT(*) FROM docs").fetchone()[0]
    total_chunks = cur.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    print(json.dumps({"docs": total_docs, "chunks": total_chunks, "db": args.db}, indent=2))


if __name__ == "__main__":
    main()
