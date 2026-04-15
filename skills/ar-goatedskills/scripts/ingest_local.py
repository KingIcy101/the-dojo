#!/usr/bin/env python3
"""Ingest local Hormozi books (markdown + PDF) into SQLite FTS5 for quote retrieval."""
import argparse
import json
import re
import sqlite3
from pathlib import Path
from typing import Iterable, List, Tuple

WORD_RE = re.compile(r"[a-zA-Z0-9']+")
WS_RE = re.compile(r"\s+")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)

DEFAULT_SOURCE = Path.home() / ".openclaw/workspace/Z2A/Hormozi"
DEFAULT_DB = Path(__file__).resolve().parent.parent / "data" / "books.db"


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


def find_section(text: str, char_pos: int) -> str:
    """Find the nearest heading above a character position in markdown."""
    best = "Introduction"
    for m in HEADING_RE.finditer(text):
        if m.start() <= char_pos:
            best = m.group(1).strip()
        else:
            break
    return best


def ingest_markdown(cur, path: Path, doc_id: int):
    raw = path.read_text(encoding="utf-8", errors="ignore")
    chunk_idx = 0
    for start, end, ch in chunk_text(raw):
        section = find_section(raw, start)
        location = json.dumps({"type": "markdown", "section": section, "char_start": start, "char_end": end})
        add_chunk(cur, doc_id, chunk_idx, ch, location)
        chunk_idx += 1
    return chunk_idx


def ingest_pdf(cur, path: Path, doc_id: int):
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    chunk_idx = 0
    for i, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        for start, end, ch in chunk_text(raw):
            location = json.dumps({"type": "pdf", "page": i, "char_start": start, "char_end": end})
            add_chunk(cur, doc_id, chunk_idx, ch, location)
            chunk_idx += 1
    return chunk_idx


def clean_title(filename: str) -> str:
    """Strip file extension and common noise from filenames to get a readable title."""
    name = Path(filename).stem
    # Remove Anna's Archive hash patterns
    name = re.sub(r"\s*--\s*[a-f0-9]{32}\s*--\s*Anna's Archive", "", name)
    # Remove trailing author/year patterns like "-- Alex Hormozi -- 2023"
    name = re.sub(r"\s*--\s*Alex Hormozi\s*--\s*\d{4}", "", name)
    name = re.sub(r"\s*--\s*Alex Hormozi", "", name)
    # Clean up double spaces
    name = re.sub(r"\s+", " ", name).strip()
    return name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=str(DEFAULT_SOURCE))
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()

    source = Path(args.source_dir)
    if not source.exists():
        print(f"ERROR: Source directory not found: {source}")
        return

    # Collect all files
    md_files = sorted(source.glob("*.md"))
    pdf_files = sorted(source.glob("*.pdf"))

    # Build a map of base name -> available formats
    # Prefer .md over .pdf when both exist
    book_map = {}
    for f in md_files:
        base = f.stem
        book_map[base] = ("md", f)
    for f in pdf_files:
        base = f.stem
        if base not in book_map:  # only use PDF if no .md exists
            book_map[base] = ("pdf", f)

    if not book_map:
        print(f"ERROR: No .md or .pdf files found in {source}")
        return

    print(f"Source: {source}")
    print(f"Found {len(md_files)} .md files, {len(pdf_files)} .pdf files")
    print(f"Ingesting {len(book_map)} unique books (preferring .md over .pdf)")

    conn = init_db(Path(args.db))
    cur = conn.cursor()

    total_chunks = 0
    for base, (fmt, path) in sorted(book_map.items()):
        title = clean_title(path.name)
        cur.execute("INSERT INTO docs(title, path, format) VALUES (?, ?, ?)", (title, str(path), fmt))
        doc_id = cur.lastrowid
        print(f"  [{fmt.upper()}] {title}")
        try:
            if fmt == "md":
                chunks = ingest_markdown(cur, path, doc_id)
            else:
                chunks = ingest_pdf(cur, path, doc_id)
            total_chunks += chunks
        except Exception as e:
            print(f"  WARN: failed to ingest {title}: {e}")

    conn.commit()

    total_docs = cur.execute("SELECT COUNT(*) FROM docs").fetchone()[0]
    total_chunks_db = cur.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    print(json.dumps({"docs": total_docs, "chunks": total_chunks_db, "db": args.db}, indent=2))
    conn.close()


if __name__ == "__main__":
    main()
