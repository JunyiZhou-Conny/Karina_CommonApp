#!/usr/bin/env python3
"""Build the two-family PSDA desk pack.

Family A — sampling frame / generalize / MoE / experiment vs observational
Family B — frequency tables, box plots, two data sets, mean / median / spread

Official items come from the Hard exclude-active PSDA bank (skill tag).
Originals come from Targeted Sets 03 / 04 / 06 / 07 and the desk packet.

Student PDF has no answers. Instructor PDF uses official keys pages plus
an answer bar on the originals.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from build_modules import DOMAINS, HERE, _overlay_pdf
from build_review_packs import labeled_review_page, write_pdf

PACK = HERE.parent
PRINT = HERE.parents[3] / "print"
ERROR = HERE.parents[3] / "error-log"
KEYS_PDF = PACK / "answers" / "SAT-Math-Hard-PSDA-66-keys.pdf"
STUDENT_PDF = PACK / "student" / "SAT-Math-Hard-PSDA-66.pdf"
SHEET = PACK / "answers" / "SAT-Math-Hard-PSDA-66-check-sheet.md"
ORIGINALS_MD = PRINT / "PSDA-FRAME-DATA-ORIGINALS.md"

KNOWN_SPR = {
    55: "2.6, 13/5",
    61: "1",
}

ORIGINALS = [
    # n, answer, source, family, job
    (26, "B", "Set 06 #3", "A", "Volunteer website poll is not a random sample."),
    (27, "B", "Set 06 #10", "A", "Random assignment ⇒ experiment / cause."),
    (28, "D", "Set 06 #14", "A", "Generalize to the sampling frame, not the table subset."),
    (29, "B", "Set 06 #20", "A", "Watch, don’t assign ⇒ observational. No cause."),
    (30, "C", "Set 07 #3", "A", "Larger MoE ⇔ smaller n. Not the percent in favor."),
    (31, "B", "Set 07 #4", "A", r"38±3 is 35 to 41. Not “exactly 38%.”"),
    (32, "B", "Set 07 #5", "A", "Larger n ⇒ smaller MoE."),
    (33, "B", "Desk C11", "A", r"52±4 is 48 to 56."),
    (34, "B", "Desk C12", "A", "Honors hallway is not the whole school."),
    (35, "C", "Desk M16", "A", "“Exactly 61%” is the unjustified claim."),
    (36, "9", "Set 03 #1", "B", "Max data value. Frequency 0 kills 7."),
    (37, "A", "Set 03 #7", "B", "Max frequency is 20, not data value 40."),
    (38, "18", "Set 03 #18", "B", "Max data value. 17 has frequency 0."),
    (39, "C", "Set 04 #2", "B", "Add a constant: center moves, spread stays."),
    (40, "0", "Set 06 #8", "B", "Same bins ⇒ smallest |mean A−mean B| is 0."),
    (41, "9", "Set 06 #19", "B", "Push the lists apart. Width-10 integers differ by at most 9."),
]


def skill_of(text: str) -> str:
    low = text.lower()
    if "inf er ence" in low or "inference from sample" in low:
        return "inference"
    if "e valuating statistical" in low or "evaluating statistical" in low:
        return "claims"
    if "one-variable data" in low:
        return "onevar"
    return "other"


def parse_check_sheet() -> list[dict]:
    items = []
    for line in SHEET.read_text().splitlines():
        if not line.startswith("|") or line.startswith("|---") or "Question ID" in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 4 or not parts[0].isdigit():
            continue
        items.append(
            {
                "source_n": int(parts[0]),
                "answer": parts[1],
                "qid": parts[2].strip("`"),
                "keys_page": int(parts[3]),
            }
        )
    if len(items) != 66:
        raise SystemExit(f"PSDA check sheet has {len(items)} rows, expected 66")
    return items


def classify_official() -> tuple[list[dict], list[dict]]:
    keys = PdfReader(str(KEYS_PDF))
    bank = parse_check_sheet()
    frame, data = [], []
    for item in bank:
        page_i = item["keys_page"] - 1
        if page_i < 0 or page_i >= len(keys.pages):
            raise SystemExit(f"bad keys_page {item['keys_page']} for {item['qid']}")
        skill = skill_of(keys.pages[page_i].extract_text() or "")
        if skill in ("inference", "claims"):
            frame.append({**item, "family": "A", "skill": skill})
        elif skill == "onevar":
            data.append({**item, "family": "B", "skill": skill})
    if len(frame) != 11:
        raise SystemExit(f"expected 11 frame/inference items, got {len(frame)}")
    if len(data) != 14:
        raise SystemExit(f"expected 14 one-variable items, got {len(data)}")
    return frame, data


def keys_page_span(items: list[dict], item: dict) -> range:
    """Official keys PDF pages for one item, including continuation pages."""
    starts = sorted({it["keys_page"] for it in items})
    start = item["keys_page"]
    later = [s for s in starts if s > start]
    end = later[0] if later else item["keys_page"] + 1
    return range(start, end)


def cover_page(title: str, lines: list[str], dest: Path, footer: str) -> object:
    dest.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(dest), pagesize=letter)
    w, h = letter
    c.setFillColorRGB(0.12, 0.12, 0.12)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(54, h - 80, title)
    c.setStrokeColorRGB(0.55, 0.55, 0.55)
    c.setLineWidth(0.8)
    c.line(54, h - 92, w - 54, h - 92)
    c.setFont("Helvetica", 11)
    y = h - 124
    for line in lines:
        c.drawString(54, y, line)
        y -= 16
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.35, 0.35, 0.35)
    c.drawString(54, 48, footer)
    c.save()
    return PdfReader(str(dest)).pages[0]


def stamp_answer_bar(page, n: int, answer: str):
    def draw(c, w, h):
        c.setFillColorRGB(0.15, 0.15, 0.15)
        c.rect(0, 0, w, 28, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(18, 10, f"#{n}   Answer: {answer}   ·   instructor only")

    _overlay_pdf(page, draw)
    return page


def html_to_pdf(html: Path, pdf: Path) -> Path:
    pdf.parent.mkdir(parents=True, exist_ok=True)
    pdf.unlink(missing_ok=True)
    cmd = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--virtual-time-budget=8000",
        f"--user-data-dir=/tmp/chrome-psda-frame-{pdf.stem}",
        f"--print-to-pdf={pdf}",
        html.resolve().as_uri(),
    ]
    try:
        subprocess.run(cmd, check=True, timeout=40)
    except subprocess.TimeoutExpired:
        if not pdf.exists() or pdf.stat().st_size < 1000:
            raise
    if not pdf.exists() or pdf.stat().st_size < 1000:
        raise SystemExit(f"chrome did not write {pdf}")
    return pdf


def render_originals() -> list:
    sys.path.insert(0, str(PRINT))
    from build_packet import build

    html = build(ORIGINALS_MD, compact=True)
    tmp = HERE / ".originals-frame-data.pdf"
    html_to_pdf(html, tmp)
    pages = list(PdfReader(str(tmp)).pages)
    tmp.unlink(missing_ok=True)
    # First page is the title; each later page is one original.
    body = pages[1:] if len(pages) > 1 else pages
    if len(body) != len(ORIGINALS):
        raise SystemExit(f"originals PDF has {len(body)} item pages, expected {len(ORIGINALS)}")
    return body


def write_key_md(official: list[dict]) -> Path:
    lines = [
        "# PSDA frame + one-variable data — instructor key",
        "",
        "Do **not** give this page or the answers PDF to Karina.",
        "",
        "Student: [`../../print/PSDA-FRAME-DATA-QUESTIONS.pdf`](../../print/PSDA-FRAME-DATA-QUESTIONS.pdf)  ",
        "Answers PDF: [`../../error-log/PSDA-FRAME-DATA-ANSWERS.pdf`](../../error-log/PSDA-FRAME-DATA-ANSWERS.pdf)",
        "",
        "Official items are the Hard exclude-active PSDA bank, skill-tagged",
        "**Inference / Evaluating statistical claims** (family A) and",
        "**One-variable data** (family B). Originals are from Targeted Sets",
        "03 / 04 / 06 / 07 and the desk packet. No official stems on this page.",
        "",
        "## Official",
        "",
        "| # | Family | Bank # | Official | Skill | Question ID |",
        "|---|---|---|---|---|---|",
    ]
    for i, item in enumerate(official, start=1):
        fam = "A frame" if item["family"] == "A" else "B data"
        ans = KNOWN_SPR.get(item["source_n"], item["answer"])
        lines.append(
            f"| {i} | {fam} | {item['source_n']} | **{ans}** | "
            f"{item['skill']} | `{item['qid']}` |"
        )
    lines += [
        "",
        "## Originals",
        "",
        "| # | Family | Source | Official | Job |",
        "|---|---|---|---|---|",
    ]
    for n, ans, src, fam, job in ORIGINALS:
        label = "A frame" if fam == "A" else "B data"
        lines.append(f"| {n} | {label} | {src} | **{ans}** | {job} |")
    lines += [
        "",
        f"**Counts:** official A {sum(1 for x in official if x['family']=='A')}, "
        f"official B {sum(1 for x in official if x['family']=='B')}, "
        f"originals {len(ORIGINALS)}. Total {len(official)+len(ORIGINALS)}.",
        "",
        "The leftover Hard PSDA skills (percent, ratio, probability, two-variable",
        "scatter, units) are **not** in this pack. Full 66-item bank is still",
        "[`../student/SAT-Math-Hard-PSDA-66.pdf`](../student/SAT-Math-Hard-PSDA-66.pdf).",
        "",
    ]
    text = "\n".join(lines)
    out = ERROR / "psda-frame-data-key.md"
    out.write_text(text)
    (HERE / "keys" / "psda-frame-data-key.md").write_text(
        text.replace("../../print/", "../../../print/").replace(
            "../../error-log/", "../../../error-log/"
        )
    )
    return out


def main() -> None:
    frame, data = classify_official()
    official = frame + data
    total = len(official) + len(ORIGINALS)
    if total != 41:
        raise SystemExit(f"expected 41 items, got {total}")

    student_bank = PdfReader(str(STUDENT_PDF))
    keys_bank = PdfReader(str(KEYS_PDF))
    all_bank = parse_check_sheet()
    originals_pages = render_originals()

    cover_lines = [
        "41 items  ·  two PSDA families only  ·  untimed",
        "1–11   Family A  ·  official  ·  frame / generalize / MoE / experiment",
        "12–25  Family B  ·  official  ·  frequency / box plot / two data sets",
        "26–35  Family A  ·  repo originals (Sets 06 / 07 + desk)",
        "36–41  Family B  ·  repo originals (Sets 03 / 04 / 06)",
        "Official pages are the Hard exclude-active bank. Originals are not",
        "College Board stems. Do not re-sit Bluebook 4 / 5 / 6 / 8 / 9 / 11.",
    ]
    q_cover = HERE / ".cover-frame-data-q.pdf"
    a_cover = HERE / ".cover-frame-data-a.pdf"
    q_pages = [
        cover_page(
            "PSDA · frame + one-variable data",
            cover_lines,
            q_cover,
            "No answers in this file. Write on the page or on scratch paper.",
        )
    ]
    a_pages = [
        cover_page(
            "PSDA · frame + one-variable data  ·  ANSWERS",
            cover_lines
            + ["", "Instructor only. Official keys pages include the rationale."],
            a_cover,
            "Do not give this file to Karina.",
        )
    ]

    for i, item in enumerate(official, start=1):
        label = (
            f"Family A  ·  bank #{item['source_n']}"
            if item["family"] == "A"
            else f"Family B  ·  bank #{item['source_n']}"
        )
        src = student_bank.pages[item["source_n"] - 1]
        q_pages.append(labeled_review_page(src, i, total, label))
        for p in keys_page_span(all_bank, item):
            raw = keys_bank.pages[p - 1]
            tmp = PdfWriter()
            tmp.add_page(raw)
            page = tmp.pages[0]
            stamp_answer_bar(page, i, KNOWN_SPR.get(item["source_n"], item["answer"]))
            a_pages.append(page)

    for (n, ans, src, fam, _job), page in zip(ORIGINALS, originals_pages):
        label = f"Family {'A' if fam == 'A' else 'B'}  ·  {src}"
        q_pages.append(labeled_review_page(page, n, total, label))
        tmp = PdfWriter()
        tmp.add_page(page)
        keyed = tmp.pages[0]
        stamp_answer_bar(keyed, n, ans)
        a_pages.append(keyed)

    student_out = PRINT / "PSDA-FRAME-DATA-QUESTIONS.pdf"
    answers_out = ERROR / "PSDA-FRAME-DATA-ANSWERS.pdf"
    write_pdf(q_pages, student_out)
    write_pdf(a_pages, answers_out)
    q_cover.unlink(missing_ok=True)
    a_cover.unlink(missing_ok=True)
    key = write_key_md(official)
    print(f"student  {student_out}  ({len(q_pages)} pages)")
    print(f"answers  {answers_out}  ({len(a_pages)} pages)")
    print(f"key      {key}")


if __name__ == "__main__":
    main()
