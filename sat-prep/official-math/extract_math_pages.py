#!/usr/bin/env python3
"""Pull Math Module 1+2 question pages from uploaded College Board practice tests."""

from pathlib import Path
import re
import pymupdf

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
OUT_PDF = OUT_DIR / "SAT-MATH-OFFICIAL-PRACTICE-PAGES.pdf"

SOURCE_NAME = re.compile(r"^sat-practice-test-(\d+)-digital\.pdf$")
KNOWN_EXAMS = range(1, 12)


def discover_sources() -> list[tuple[int, Path]]:
    """Pick up every question booklet at the repo root, including newly added tests."""
    found: list[tuple[int, Path]] = []
    for path in ROOT.glob("sat-practice-test-*-digital.pdf"):
        match = SOURCE_NAME.fullmatch(path.name)
        if match:
            found.append((int(match.group(1)), path))
    return sorted(found, key=lambda item: item[0])


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()


def is_math_module_start(text: str) -> bool:
    t = norm(text)
    if "reading and writing" in t and "33 questions" in t:
        return False
    if "27 questions" in t and "math" in t:
        return True
    if "important math skills" in t and "directions" in t and "reading and writing" not in t:
        return True
    return False


def is_blank_or_end(text: str) -> bool:
    t = norm(text)
    if "no test material" in t:
        return True
    if "general directions" in t and "you may work on only one module" in t:
        return True
    if not t:
        return True
    return False


def find_math_ranges(doc: pymupdf.Document) -> list[tuple[int, int, str]]:
    """Return (start, end_inclusive, label) 0-based."""
    starts: list[int] = []
    for i, page in enumerate(doc):
        if is_math_module_start(page.get_text("text")):
            starts.append(i)
    ranges = []
    for n, start in enumerate(starts):
        limit = starts[n + 1] if n + 1 < len(starts) else doc.page_count
        end = start
        for j in range(start, limit):
            text = doc[j].get_text("text")
            if j > start and is_blank_or_end(text):
                break
            end = j
        label = f"Math Module {n + 1}"
        ranges.append((start, end, label))
    return ranges


def add_label_page(out: pymupdf.Document, exam: int, subtitle: str, pages: str) -> None:
    page = out.new_page(width=612, height=792)
    rect = pymupdf.Rect(54, 240, 558, 520)
    page.insert_textbox(
        rect,
        f"Official SAT Practice Test {exam}\n\n{subtitle}\n\nSource file: sat-practice-test-{exam}-digital.pdf\nPages in source: {pages}\n\nCollege Board Digital SAT practice.\nMath questions only. Scoring PDFs were skipped.",
        fontsize=16,
        fontname="helv",
        align=pymupdf.TEXT_ALIGN_CENTER,
    )


def stamp(page: pymupdf.Page, exam: int, module: str, source_page: int) -> None:
    label = f"  Source: Official SAT Practice Test {exam}  ·  {module}  ·  source page {source_page}  "
    bar = pymupdf.Rect(0, 0, page.rect.width, 18)
    page.draw_rect(bar, color=(0.15, 0.15, 0.15), fill=(0.15, 0.15, 0.15))
    page.insert_textbox(
        bar,
        label,
        fontsize=8,
        fontname="helv",
        color=(1, 1, 1),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )


def main() -> None:
    out = pymupdf.open()
    cover = out.new_page(width=612, height=792)
    lines = [
        "SAT Math - official practice pages",
        "",
        "Pulled from the College Board Digital SAT PDFs in this repo.",
        "Scoring booklets were not used.",
        "",
        "Included exams (question booklets only):",
    ]
    catalog = []
    sources = discover_sources()
    present = {exam for exam, _path in sources}
    for exam, path in sources:
        if not path.exists():
            lines.append(f"  Test {exam}: FILE MISSING")
            continue
        doc = pymupdf.open(path)
        ranges = find_math_ranges(doc)
        if not ranges:
            lines.append(f"  Test {exam}: no math modules detected")
            doc.close()
            continue
        parts = []
        for start, end, label in ranges:
            parts.append(f"{label} pp. {start+1}-{end+1}")
        lines.append(f"  Test {exam}: " + "; ".join(parts))
        catalog.append((exam, path, doc, ranges))

    # tests not uploaded among the known Digital SAT series (files present, not just extracted)
    not_uploaded = [n for n in KNOWN_EXAMS if n not in present]
    if not_uploaded:
        lines.append("")
        lines.append("Not in the repo yet: Tests " + ", ".join(str(n) for n in not_uploaded))
        lines.append("(plus any scoring-only files were ignored).")

    cover.insert_textbox(
        pymupdf.Rect(54, 80, 558, 720),
        "\n".join(lines),
        fontsize=12,
        fontname="helv",
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    for exam, path, doc, ranges in catalog:
        for start, end, label in ranges:
            add_label_page(out, exam, label, f"{start+1}-{end+1}")
            for i in range(start, end + 1):
                out.insert_pdf(doc, from_page=i, to_page=i)
                stamp(out[-1], exam, label, i + 1)
        doc.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out.save(OUT_PDF)
    print(f"Wrote {OUT_PDF}  pages={out.page_count}")
    out.close()


if __name__ == "__main__":
    main()
