#!/usr/bin/env python3
"""Build the desk packet HTML with KaTeX-rendered math."""

from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
DEFAULT_MD = HERE / "SAT-MATH-DESK-PACKET.md"

SHARED_CSS = """
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
  h3 { font-size: 13.5pt; page-break-after: avoid; }
  table { border-collapse: collapse; width: 100%; margin: 0.8rem 0; font-size: 11pt; }
  th, td { border: 1px solid #444; padding: 5px 7px; text-align: left; vertical-align: top; }
  th { background: #eee; }
  p { margin: 0.45rem 0; }
  li { margin: 0.25rem 0; }
  .katex { font-size: 1.05em; }
  .page-break { break-before: page; page-break-before: always; }
  @media print {
    body { margin: 0; max-width: none; padding: 0; }
    a { color: inherit; text-decoration: none; }
  }
  @page { size: letter; margin: 0.75in; }
"""

DESK_H2 = "  h2 { font-size: 16pt; margin-top: 1.5rem; page-break-after: avoid; page-break-before: always; }\n  h1 + p + p + p + p + hr + h2 { page-break-before: avoid; }\n"
COMPACT_H2 = "  h2 { font-size: 16pt; margin-top: 1.5rem; page-break-after: avoid; }\n"
COMPACT_EXTRA = """
  p { margin: 0.5rem 0 0.85rem; }
  li { margin: 0.32rem 0; }
  table { margin: 0.55rem 0 1rem; }
  .q-gap { height: 0.7em; }
"""


def html_head(title: str, compact: bool) -> str:
    h2 = COMPACT_H2 if compact else DESK_H2
    extra = COMPACT_EXTRA if compact else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="vendor/katex/katex.min.css">
<style>
{h2}{SHARED_CSS}{extra}
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


def build(md_path: Path, compact: bool = False) -> Path:
    html_path = md_path.with_suffix(".html")
    raw = md_path.read_text(encoding="utf-8")
    title = next((line[2:].strip() for line in raw.splitlines() if line.startswith("# ")), md_path.stem)
    if compact:
        raw = re.sub(r"\n\n(\*\*\d+\.\*\*)", r'\n\n<div class="q-gap"></div>\n\n\1', raw)
    stashed, stored = stash_math(raw)
    html = to_html(stashed)
    html = restore_placeholders(html, stored)
    html_path.write_text(html_head(title, compact) + html + HTML_TAIL, encoding="utf-8")
    subprocess.run(["node", str(HERE / "render_math.mjs"), str(html_path)], check=True)
    print(f"Wrote {html_path} ({len(stored)} math fragments)")
    return html_path


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--compact"]
    compact = "--compact" in sys.argv[1:]
    md_path = HERE / args[0] if args else DEFAULT_MD
    if not md_path.is_absolute():
        candidate = HERE / md_path
        md_path = candidate if candidate.exists() else Path(args[0])
    if not compact:
        compact = md_path.name != "SAT-MATH-DESK-PACKET.md"
    build(md_path, compact=compact)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
