#!/usr/bin/env python3
import argparse
import json
import re
import sqlite3
from pathlib import Path
from typing import Dict, List

from rapidfuzz.fuzz import token_set_ratio

WORD_RE = re.compile(r"[a-zA-Z0-9']+")
STOP = {
    "what","when","where","which","who","why","how","according","hormozi",
    "does","do","is","are","a","an","the","to","of","in","on","for","and"
}


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in WORD_RE.findall(text)]


def key_terms(text: str) -> List[str]:
    out = []
    for t in tokenize(text):
        if len(t) < 4 or t in STOP:
            continue
        out.append(t)
    return out


def fts_query_from_question(q: str) -> str:
    toks = [t for t in tokenize(q) if len(t) > 2]
    if not toks:
        return ""
    return " OR ".join(toks[:12])


def best_sentence(chunk_text: str, question: str) -> str:
    terms = set(key_terms(question))
    sents = re.split(r"(?<=[.!?])\s+", chunk_text)
    if not sents:
        return chunk_text.strip()

    candidates = []
    for s in sents:
        s = s.strip()
        if not s:
            continue
        stoks = set(tokenize(s))
        overlap = len(terms & stoks)
        fuzzy = token_set_ratio(question, s)
        score = (overlap * 25) + (fuzzy * 0.8)
        if len(s) < 30:
            score -= 10
        candidates.append((score, overlap, s))

    if not candidates:
        return chunk_text.strip()

    candidates.sort(key=lambda x: (x[0], x[1], len(x[2])), reverse=True)
    # Prefer sentences that actually include key terms when possible
    for _, overlap, s in candidates:
        if overlap > 0:
            return s
    return candidates[0][2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=True)
    ap.add_argument("--db", default=str(Path(__file__).resolve().parent.parent / "data" / "books.db"))
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    fts_q = fts_query_from_question(args.question)
    if not fts_q:
        print(json.dumps({"answer": None, "evidence": [], "note": "Question too short for retrieval."}, indent=2))
        return

    rows = cur.execute(
        """
        SELECT c.id, c.text, c.location, d.title,
               bm25(chunks_fts) AS score
        FROM chunks_fts
        JOIN chunks c ON c.id = chunks_fts.rowid
        JOIN docs d ON d.id = c.doc_id
        WHERE chunks_fts MATCH ?
        ORDER BY score
        LIMIT 40
        """,
        (fts_q,),
    ).fetchall()

    q_terms = set(key_terms(args.question))
    rescored: List[Dict] = []
    for r in rows:
        chunk_text = r["text"]
        sim = token_set_ratio(args.question, chunk_text)
        chunk_terms = set(tokenize(chunk_text))
        overlap = len(q_terms & chunk_terms)
        quote = best_sentence(chunk_text, args.question)
        quote_overlap = len(q_terms & set(tokenize(quote)))
        combined = (sim * 0.7) + (overlap * 15) + (quote_overlap * 20)
        rescored.append({
            "title": r["title"],
            "text": chunk_text,
            "location": json.loads(r["location"]),
            "sim": sim,
            "overlap": overlap,
            "quote_overlap": quote_overlap,
            "combined": combined,
            "bm25": r["score"],
            "quote": quote,
        })

    rescored.sort(key=lambda x: (-x["combined"], -x["sim"], x["bm25"]))

    # keep evidence diverse by book when possible
    evidence = []
    seen_books = set()
    for item in rescored:
        if item["quote_overlap"] <= 0:
            continue
        if item["title"] in seen_books and len(evidence) < max(2, args.top // 2):
            continue
        evidence.append(item)
        seen_books.add(item["title"])
        if len(evidence) >= args.top:
            break

    if len(evidence) < min(2, args.top):
        for item in rescored:
            if item in evidence:
                continue
            evidence.append(item)
            if len(evidence) >= args.top:
                break

    if not evidence or evidence[0]["sim"] < 35:
        print(json.dumps({
            "answer": None,
            "evidence": [],
            "note": "No reliable exact quote found. Try a narrower question.",
        }, indent=2))
        return

    answer = "Based on the books, here is the most direct answer supported by exact quotes."

    out = {
        "answer": answer,
        "evidence": [
            {
                "book": e["title"],
                "location": e["location"],
                "quote": e["quote"],
                "similarity": e["sim"],
            }
            for e in evidence
        ],
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
