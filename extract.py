"""Extract the Bonnar Bible into a structured data.json for the prototype site.

Walks the PDF's TOC bookmarks and assigns each section the text from its start
page up to the next bookmark that begins on a later page.
"""
import json
import re
import os
import fitz  # PyMuPDF

SRC = r"C:\Users\f737167\OneDrive - Fortescue Metals Group\Documents\Personal\House and Finances\Scott Bonnar\Bonnar Bible V25.pdf"
OUT = os.path.join(os.path.dirname(__file__), "data", "data.json")


def clean(t: str) -> str:
    # normalise the odd bullet/dash glyph and collapse runaway whitespace
    t = t.replace("", "-").replace("�", "-")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


LIST_RE = re.compile(r"^(\d+[.)]|[-•·*])\s")


def reflow(text: str) -> str:
    """Merge mid-sentence line wraps into paragraphs; keep numbered/bulleted
    steps as their own paragraphs. Returns paragraphs separated by blank lines."""
    out, buf = [], ""

    def flush():
        nonlocal buf
        if buf.strip():
            out.append(buf.strip())
        buf = ""

    for raw in text.split("\n"):
        s = raw.strip()
        if not s:
            flush()
        elif LIST_RE.match(s):
            flush()
            buf = s
        else:
            buf = (buf + " " + s).strip() if buf else s
    flush()
    return "\n\n".join(out)


def slug(s: str, i: int) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return f"{i:03d}-{base}"[:60]


def main():
    doc = fitz.open(SRC)
    toc = doc.get_toc()  # [level, title, page(1-based)]
    n = doc.page_count

    # page text cache
    page_text = [clean(doc[i].get_text()) for i in range(n)]

    # determine each entry's end page = page before the next entry on a LATER page
    sections = []
    current_chapter = "Front Matter"
    for idx, (level, title, start) in enumerate(toc):
        title = clean(title)
        if level == 1:
            current_chapter = title
        # find next start page strictly greater than this one
        end = n  # 1-based exclusive handled below
        for j in range(idx + 1, len(toc)):
            if toc[j][2] > start:
                end = toc[j][2]
                break
        # pages are 1-based in toc; slice 0-based [start-1, end-1)
        s0 = max(0, start - 1)
        e0 = min(n, end - 1)
        if e0 <= s0:
            e0 = s0 + 1
        text = reflow("\n\n".join(page_text[s0:e0]).strip())
        sections.append({
            "id": slug(title, idx),
            "level": level,
            "chapter": current_chapter,
            "title": title,
            "page": start,
            "text": text,
        })

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({
            "source": os.path.basename(SRC),
            "pages": n,
            "count": len(sections),
            "sections": sections,
        }, f, ensure_ascii=False)

    size = os.path.getsize(OUT)
    print(f"Wrote {len(sections)} sections, {n} pages -> {OUT} ({size/1024:.0f} KB)")
    # quick sanity: chapters
    chs = [s["title"] for s in sections if s["level"] == 1]
    print("Chapters:", len(chs))
    for c in chs:
        print("  ", c)


if __name__ == "__main__":
    main()
