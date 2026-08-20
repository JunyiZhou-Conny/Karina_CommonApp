#!/usr/bin/env python3
"""Build the desk packet HTML with KaTeX-rendered math."""

from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
MD_PATH = HERE / "SAT-MATH-DESK-PACKET.md"
HTML_PATH = HERE / "SAT-MATH-DESK-PACKET.html"

HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SAT Math Desk Packet — Karina</title>
<link rel="stylesheet" href="vendor/katex/katex.min.css">
<style>
  body {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 12.5pt;
    line-height: 1.5;
    max-width: 800px;
    margin: 1.5rem auto;
    padding: 0 1.2rem 3rem;
    color: #111;
  }
  h1 { font-size: 22pt; margin-top: 1.6rem; page-break-after: avoid; }
  h2 { font-size: 16pt; margin-top: 1.5rem; page-break-after: avoid; page-break-before: always; }
  h1 + p + p + p + p + hr + h2 { page-break-before: avoid; }
  h3 { font-size: 13.5pt; page-break-after: avoid; }
  table { border-collapse: collapse; width: 100%; margin: 0.8rem 0; font-size: 11pt; }
  th, td { border: 1px solid #444; padding: 5px 7px; text-align: left; vertical-align: top; }
  th { background: #eee; }
  p { margin: 0.45rem 0; }
  li { margin: 0.25rem 0; }
  .katex { font-size: 1.05em; }
  @media print {
    body { margin: 0; max-width: none; padding: 0; }
    a { color: inherit; text-decoration: none; }
  }
  @page { size: letter; margin: 0.75in; }
</style>
</head>
<body>
"""

HTML_TAIL = """
</body>
</html>
"""


def stash_math(md: str) -> tuple[str, list[tuple[str, bool]]]:
    stored: list[tuple[str, bool]] = []

    def keep(tex: str, display: bool) -> str:
        stored.append((tex, display))
        return f"@@MATH{len(stored) - 1}@@"

    md = re.sub(r"\$\$([\s\S]+?)\$\$", lambda m: keep(m.group(1), True), md)
    md = re.sub(r"\\\[([\s\S]+?)\\\]", lambda m: keep(m.group(1), True), md)
    md = re.sub(r"\\\(([\s\S]+?)\\\)", lambda m: keep(m.group(1), False), md)
    return md, stored


def restore_placeholders(html: str, stored: list[tuple[str, bool]]) -> str:
    def repl(m: re.Match) -> str:
        return f"@@MATH{m.group(1)}@@DISPLAY{int(stored[int(m.group(1))][1])}@@TEX@@{stored[int(m.group(1))][0]}@@END@@"

    # Leave placeholders for the node script, but include the tex.
    for i, (tex, display) in enumerate(stored):
        token = f"@@MATH{i}@@"
        payload = (
            f'<span class="math-src" data-display="{int(display)}">{tex}</span>'
        )
        html = html.replace(token, payload)
    return html


def to_html(md: str) -> str:
    import markdown

    return markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"])


def main() -> None:
    raw = MD_PATH.read_text(encoding="utf-8")
    stashed, stored = stash_math(raw)
    html = to_html(stashed)
    html = restore_placeholders(html, stored)
    HTML_PATH.write_text(HTML_HEAD + html + HTML_TAIL, encoding="utf-8")
    subprocess.run(["node", str(HERE / "render_math.mjs"), str(HTML_PATH)], check=True)
    print(f"Wrote {HTML_PATH} ({len(stored)} math fragments)")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
