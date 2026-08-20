#!/usr/bin/env python3
"""Assemble the SAT Math desk packet (markdown + print HTML)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent

SECTIONS = [
    ("Digital SAT overview", ROOT / "00-digital-sat-overview.md"),
    ("Math content map", ROOT / "01-math-content-map.md"),
    ("Curriculum roadmap", ROOT / "CURRICULUM.md"),
    ("Official resources", ROOT / "resources.md"),
    ("Preparation plan", ROOT / "SAT-MATH-PREPARATION-PLAN.md"),
    ("Weekend 1 overview", ROOT / "weekend-01/README.md"),
    ("Weekend 1 Saturday", ROOT / "weekend-01/saturday.md"),
    ("Weekend 1 Sunday", ROOT / "weekend-01/sunday.md"),
    ("Weekend 1 practice set", ROOT / "weekend-01/practice-set-01.md"),
    ("Weekend 1 optional Algebra drill", ROOT / "weekend-01/optional-algebra-drill.md"),
    ("Weekend 2 overview", ROOT / "weekend-02/README.md"),
    ("Weekend 2 Saturday", ROOT / "weekend-02/saturday.md"),
    ("Weekend 2 Sunday", ROOT / "weekend-02/sunday.md"),
    ("Weekend 2 practice set", ROOT / "weekend-02/practice-set-02.md"),
    ("Weekend 3 overview", ROOT / "weekend-03/README.md"),
    ("Weekend 3 Saturday", ROOT / "weekend-03/saturday.md"),
    ("Weekend 3 Sunday", ROOT / "weekend-03/sunday.md"),
    ("Weekend 3 practice set", ROOT / "weekend-03/practice-set-03.md"),
    ("Weekend 4 overview", ROOT / "weekend-04/README.md"),
    ("Weekend 4 Saturday", ROOT / "weekend-04/saturday.md"),
    ("Weekend 4 Sunday", ROOT / "weekend-04/sunday.md"),
    ("Weekend 4 practice set", ROOT / "weekend-04/practice-set-04.md"),
    ("Answer key — Weekend 1", ROOT / "weekend-01/answer-key-01.md"),
    ("Answer key — Weekend 2", ROOT / "weekend-02/answer-key-02.md"),
    ("Answer key — Weekend 3", ROOT / "weekend-03/answer-key-03.md"),
    ("Answer key — Weekend 4", ROOT / "weekend-04/answer-key-04.md"),
]

COVER = """# SAT Math Desk Packet

**Student:** Karina (Newton North High School)
**Instructor desk copy** — Digital SAT Math, ~680 → ~780
**Cadence:** Saturday 4 hours + Sunday 4 hours
**Compiled from** the `sat-prep/` folder in Karina_CommonApp

This is one printable packet of everything in the SAT prep repository. It is not condensed. Use it at the desk: point, write, and talk.

**PSDA** = Problem-Solving and Data Analysis (ratios, percents, data, probability, statistical claims). About 15% of SAT Math.

## How to use this printout

1. Weekend 1 Saturday is a high-level Q&A tour of **all four** domains. Student talks first.
2. Weekends 2–4 go deep on Advanced Math, then PSDA, then Geometry & Trig.
3. Practice sets are mixed into each weekend. Time them when the script says to.
4. **Answer keys start after Weekend 4.** Skip printing those pages if Karina should not see solutions during a set. Or fold them under / keep them on the instructor side of the desk.
5. Official Bluebook / Question Bank items are **not** copied here. Links are in the resources section.

## Packet contents

1. Digital SAT overview
2. Math content map (skill checklist)
3. Curriculum roadmap
4. Official resources
5. Preparation plan
6. Weekend 1 — all four domains (Sat / Sun / practice / optional Algebra drill)
7. Weekend 2 — Advanced Math
8. Weekend 3 — PSDA
9. Weekend 4 — Geometry & Trig + Module 1
10. Answer keys (Weekends 1–4)

---
"""

HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SAT Math Desk Packet — Karina</title>
<style>
  body {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 13pt;
    line-height: 1.55;
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1.5rem 4rem;
    color: #111;
  }
  h1 { font-size: 22pt; margin-top: 2rem; page-break-after: avoid; }
  h2 { font-size: 18pt; margin-top: 1.8rem; page-break-after: avoid; }
  h3 { font-size: 14pt; page-break-after: avoid; }
  table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 11.5pt; }
  th, td { border: 1px solid #444; padding: 6px 8px; text-align: left; vertical-align: top; }
  th { background: #eee; }
  code, pre { font-family: "Courier New", monospace; font-size: 11pt; }
  pre { white-space: pre-wrap; background: #f6f6f6; padding: 0.8rem; }
  hr { border: none; border-top: 1px solid #999; margin: 2rem 0; }
  blockquote { margin-left: 0; padding-left: 1rem; border-left: 3px solid #888; }
  .section-break { page-break-before: always; }
  @media print {
    body { margin: 0; max-width: none; padding: 0; font-size: 12pt; }
    a { color: inherit; text-decoration: none; }
  }
  @page { size: letter; margin: 0.85in; }
</style>
</head>
<body>
"""

HTML_TAIL = """
</body>
</html>
"""


def strip_first_heading(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        if lines and not lines[0].strip():
            lines = lines[1:]
    return "\n".join(lines).rstrip() + "\n"


def to_html(md: str) -> str:
    try:
        import markdown

        return markdown.markdown(
            md,
            extensions=["tables", "fenced_code", "sane_lists"],
        )
    except ImportError:
        # Minimal fallback: keep markdown readable in a <pre> if the library is missing.
        escaped = (
            md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        return f"<pre>{escaped}</pre>"


def main() -> None:
    parts = [COVER]
    for title, path in SECTIONS:
        raw = path.read_text(encoding="utf-8")
        body = strip_first_heading(raw)
        prefix = "\n\n"
        if title in {
            "Weekend 1 overview",
            "Weekend 2 overview",
            "Weekend 3 overview",
            "Weekend 4 overview",
        }:
            prefix = '\n\n<div class="section-break"></div>\n\n'
        if title.startswith("Answer key — Weekend 1"):
            prefix = (
                '\n\n<div class="section-break"></div>\n\n'
                "# Answer keys\n\n"
                "Instructor side. Do not hand these pages to Karina during a timed set.\n\n"
            )
        parts.append(f"{prefix}# {title}\n\n{body}")

    md_text = "".join(parts)
    md_path = OUT / "SAT-MATH-DESK-PACKET.md"
    html_path = OUT / "SAT-MATH-DESK-PACKET.html"
    md_path.write_text(md_text, encoding="utf-8")
    html_path.write_text(HTML_HEAD + to_html(md_text) + HTML_TAIL, encoding="utf-8")
    print(f"Wrote {md_path}")
    print(f"Wrote {html_path}")
    print(f"Markdown lines: {md_text.count(chr(10))}")


if __name__ == "__main__":
    main()
