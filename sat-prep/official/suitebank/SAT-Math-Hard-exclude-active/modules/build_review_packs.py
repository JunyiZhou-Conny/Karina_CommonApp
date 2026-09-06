#!/usr/bin/env python3
"""Build last-week student packs from official Suite Hard pages.

1. Miss review: the 41 items she actually missed in scored Modules 01–06.
   Module 01 #20 landed (method only) and is omitted.
   Module 07 has no score sheet in the log, so it is not in this pack.
2. Unseen Hard PSDA: the 66 official Hard PSDA items minus anything already
   used in Modules 01–08 (completed sits + the next assigned volume).

Student PDFs have no answers. Do not give the keys to Karina.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from build_modules import (
    DOMAINS,
    HERE,
    OUT_KEYS,
    OUT_STUDENT,
    QUESTION_BAR,
    _overlay_pdf,
)

MANIFEST = HERE / "manifest.json"

# Actual wrongs only. Skip Module 01 #20 (landed).
MISSES = [
    # module, item, she wrote, leak (no official stems)
    (1, 1, "5", "Asked blackberries; solved raspberries / parked a radius."),
    (1, 3, "1410", "K29 — constant from the factors; recopied a leftover."),
    (1, 12, r"8+√2344/2", "K30 — did not finish Pythagorean."),
    (1, 13, "blank", "K11 — infinitely many; matching constants."),
    (1, 22, "−8", "Had −12; added the vertex y."),
    (2, 1, "−13", "f+g intercept off by 1."),
    (2, 4, "C", "Scatter opens down; C opens up."),
    (2, 7, "10", "K38 — bowls vs price is a quadratic, not a line."),
    (2, 8, "9", "K36 — Δy only; did not divide by days."),
    (2, 12, "A", "K37 — website poll; 98% bait."),
    (2, 13, "C", "K35 — printed constant is F(h), not F(0)."),
    (2, 16, "C", "K37 — generalize to the frame, not the table."),
    (2, 19, "C", "Factor, then difference of squares, then k."),
    (2, 20, "A", "Exponential step: f(n)(1−r^k), not A."),
    (3, 7, "8", "K36 — boxed volume leftover, not 2.56/8."),
    (3, 9, "1/3", "K49 — arc over 2πr, not disk area."),
    (3, 15, "C", "K48 — larger MoE because smaller n."),
    (3, 16, "D", "K7 — ⊥ to vertical is slope 0, not undefined."),
    (3, 18, "B", "K50 — double root is one pair."),
    (3, 19, "A", "K51 — asked x+6=0, not a bracket around x=−6."),
    (3, 22, "−422", "Arithmetic on the x coefficient; key −419."),
    (4, 3, "C", "K16 — mean of R is greater, not equal."),
    (4, 4, "D", "Pyramid: total SA minus lateral is the base."),
    (4, 9, "D", "Both I and II work; D is neither."),
    (4, 14, "D", "First-day price + extra per additional day."),
    (4, 20, "29", "Leftover from the exponential table; asked k."),
    (4, 21, "C", "Isolate the asked expression."),
    (4, 22, "−81/4", "Work had +81/4; boxed the minus."),
    (5, 1, "B", "K37 — frame too wide (whole region)."),
    (5, 2, "650", "First-stretch distance is Δy, not a later y."),
    (5, 3, "blank", "Did not finish; m+n=15.5."),
    (5, 5, "C", "K36 — mm/month → mm/year; wrong unit scale."),
    (5, 7, "9", "Leftover; a=0.09, not 9."),
    (5, 13, "C", "Each serving is 5% of the daily allowance."),
    (5, 16, "A", "Similar / parallel: only II must be true."),
    (6, 4, "B", "Congruence: neither I nor II is enough alone."),
    (6, 11, "A", "K48 — 30%±3% is 27 to 33; 35% is outside."),
    (6, 12, "C", "Opposite sides of the x-axis; odd multiple of π."),
    (6, 15, "B", "K48 — larger n ⇒ smaller MoE."),
    (6, 18, "blank", "Linear in one variable; started and stopped."),
    (6, 20, "18", "Leftover 13+5; asked length 13."),
]

EXCLUDE_PSDA_MODULES = range(1, 9)  # seen in 01–07 + assigned 08

# Manifest rows that only say *(see keys)* but the session log already has the official SPR.
KNOWN_SPR = {
    (1, 3): "210",
    (3, 9): "1/6",
    (4, 20): "8",
    (6, 20): "13",
}


def load_manifest() -> dict[int, dict]:
    payload = json.loads(MANIFEST.read_text())
    return {m["id"]: m for m in payload["modules"]}


def lookup(mods: dict[int, dict], mid: int, n: int) -> dict:
    for item in mods[mid]["items"]:
        if item["n"] == n:
            return item
    raise KeyError(f"Module {mid} #{n}")


def cover_page(title: str, lines: list[str], dest: Path) -> object:
    dest.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(dest), pagesize=letter)
    w, h = letter
    c.setFillColorRGB(0.12, 0.12, 0.12)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(54, h - 88, title)
    c.setStrokeColorRGB(0.55, 0.55, 0.55)
    c.setLineWidth(0.8)
    c.line(54, h - 100, w - 54, h - 100)
    c.setFont("Helvetica", 12)
    y = h - 132
    for line in lines:
        c.drawString(54, y, line)
        y -= 18
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.35, 0.35, 0.35)
    c.drawString(54, 54, "No answers in this file. Write on the page or on scratch paper.")
    c.save()
    return PdfReader(str(dest)).pages[0]


def labeled_review_page(src_page, n: int, total: int, source_label: str):
    """Official item with a review bar: Question N of M + original source."""
    tmp = PdfWriter()
    tmp.add_page(src_page)
    page = tmp.pages[0]
    page.add_transformation(Transformation().translate(0, -QUESTION_BAR))

    def draw(c, w, h):
        c.setFillColorRGB(0.90, 0.90, 0.90)
        c.rect(0, h - QUESTION_BAR, w, QUESTION_BAR, fill=1, stroke=0)
        box_w = 24 if n < 10 else 30
        c.setFillColorRGB(0, 0, 0)
        c.rect(18, h - QUESTION_BAR + 5, box_w, 24, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(18 + box_w / 2, h - QUESTION_BAR + 11, str(n))
        c.setFillColorRGB(0.12, 0.12, 0.12)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(18 + box_w + 8, h - QUESTION_BAR + 12, f"Question {n} of {total}")
        c.setFont("Helvetica", 10)
        c.drawRightString(w - 22, h - QUESTION_BAR + 13, source_label)
        c.setStrokeColorRGB(0.55, 0.55, 0.55)
        c.setLineWidth(0.6)
        c.line(0, h - QUESTION_BAR, w, h - QUESTION_BAR)

    _overlay_pdf(page, draw)
    return page


def write_pdf(pages, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    for page in pages:
        writer.add_page(page)
    with path.open("wb") as f:
        writer.write(f)
    return path


def build_miss_review(mods: dict[int, dict], readers: dict[str, PdfReader]) -> tuple[Path, Path]:
    rows = []
    for mid, n, wrote, leak in MISSES:
        item = lookup(mods, mid, n)
        rows.append({**item, "module": mid, "wrote": wrote, "leak": leak})

    total = len(rows)
    if total != 41:
        raise SystemExit(f"expected 41 misses, got {total}")

    cover = HERE / ".cover-miss-review.pdf"
    pages = [
        cover_page(
            "Suite Hard · miss review",
            [
                "Modules 01–06  ·  41 items she missed  ·  untimed",
                "Each page is the official item she already sat.",
                "The bar says Module X · #Y so you can match her old sheet.",
                "Module 01 #20 is omitted (she landed).",
                "Module 07 is omitted (no score sheet in the log).",
                "No answers in this file.",
            ],
            cover,
        )
    ]
    for i, row in enumerate(rows, start=1):
        src = readers[row["domain"]].pages[row["source_n"] - 1]
        pages.append(
            labeled_review_page(
                src,
                i,
                total,
                f"Module {row['module']:02d}  ·  #{row['n']}",
            )
        )
    student = write_pdf(pages, OUT_STUDENT / "miss-review-01-06.pdf")
    cover.unlink(missing_ok=True)

    lines = [
        "# Miss review · Modules 01–06 — instructor key",
        "",
        "Do **not** give this page to Karina. Student file: "
        "[`../student/miss-review-01-06.pdf`](../student/miss-review-01-06.pdf).",
        "",
        f"{total} official items she missed. Module 01 #20 omitted (landed). "
        "Module 07 omitted (no sheet).",
        "",
        "| Review # | Module | # | She wrote | Official | Domain | Source # | Question ID | Leak |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, row in enumerate(rows, start=1):
        official = KNOWN_SPR.get((row["module"], row["n"]), row["answer"])
        lines.append(
            f"| {i} | {row['module']:02d} | {row['n']} | {row['wrote']} | "
            f"{official} | {row['domain']} | {row['source_n']} | "
            f"`{row['qid']}` | {row['leak']} |"
        )
    mix = {}
    for row in rows:
        mix[row["domain"]] = mix.get(row["domain"], 0) + 1
    mix_s = ", ".join(f"{d} {mix.get(d, 0)}" for d in ("Algebra", "Advanced Math", "PSDA", "Geometry"))
    lines += ["", f"**Mix:** {mix_s}.", ""]
    key = HERE.parents[3] / "error-log" / "module-miss-review-key.md"
    # Prefer keys next to the other module keys, plus a copy in error-log.
    module_key = OUT_KEYS / "miss-review-01-06-key.md"
    text = "\n".join(lines) + "\n"
    module_key.write_text(text)
    key.write_text(text.replace("[`../student/miss-review-01-06.pdf`](../student/miss-review-01-06.pdf)",
                                "[`../official/suitebank/SAT-Math-Hard-exclude-active/modules/student/miss-review-01-06.pdf`](../official/suitebank/SAT-Math-Hard-exclude-active/modules/student/miss-review-01-06.pdf)"))
    return student, module_key


def build_unseen_psda(mods: dict[int, dict], readers: dict[str, PdfReader]) -> tuple[Path, Path]:
    used_src = set()
    used_where: dict[int, str] = {}
    for mid in EXCLUDE_PSDA_MODULES:
        for item in mods[mid]["items"]:
            if item["domain"] != "PSDA":
                continue
            used_src.add(item["source_n"])
            used_where[item["source_n"]] = f"Module {mid:02d} #{item['n']}"

    bank = []
    sheet = DOMAINS["PSDA"]["sheet"]
    for line in sheet.read_text().splitlines():
        # | n | answer | `qid` | keys_page |
        if not line.startswith("|") or line.startswith("|---") or "Question ID" in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 4 or not parts[0].isdigit():
            continue
        bank.append(
            {
                "source_n": int(parts[0]),
                "answer": parts[1],
                "qid": parts[2].strip("`"),
                "keys_page": int(parts[3]),
            }
        )
    if len(bank) != 66:
        raise SystemExit(f"PSDA check sheet has {len(bank)} rows, expected 66")

    keep = [it for it in bank if it["source_n"] not in used_src]
    if len(keep) != 66 - len(used_src):
        raise SystemExit("PSDA filter length mismatch")
    if len(used_src) != 32:
        raise SystemExit(f"expected 32 PSDA items in Modules 01–08, got {len(used_src)}")
    if len(keep) != 34:
        raise SystemExit(f"expected 34 unseen PSDA, got {len(keep)}")

    total = len(keep)
    cover = HERE / ".cover-psda-unseen.pdf"
    pages = [
        cover_page(
            "Hard PSDA · unseen",
            [
                f"{total} official Hard PSDA items  ·  suggested 50 minutes if you want a clock",
                "These 34 are not in Suite Hard Modules 01–08.",
                "Modules 01–06 she already sat. Module 07 is treated as seen.",
                "Module 08 is the next volume sit, so those 4 are held out too.",
                "Full leftover distribution of the 66-item Hard PSDA bank.",
                "No answers in this file.",
            ],
            cover,
        )
    ]
    reader = readers["PSDA"]
    for i, item in enumerate(keep, start=1):
        pages.append(
            labeled_review_page(
                reader.pages[item["source_n"] - 1],
                i,
                total,
                f"PSDA  ·  bank #{item['source_n']}",
            )
        )
    student = write_pdf(pages, OUT_STUDENT / "psda-unseen.pdf")
    cover.unlink(missing_ok=True)

    lines = [
        "# Hard PSDA · unseen (not in Modules 01–08) — instructor key",
        "",
        "Do **not** give this page to Karina. Student file: "
        "[`../student/psda-unseen.pdf`](../student/psda-unseen.pdf).",
        "",
        f"{total} items. Dropped the 32 official Hard PSDA items already used "
        "in Modules 01–08. Bank order kept so the leftover types stay in "
        "export order (full remaining distribution).",
        "",
        "| # | Answer | Bank # | Question ID | Keys page |",
        "|---|---|---|---|---|",
    ]
    for i, item in enumerate(keep, start=1):
        lines.append(
            f"| {i} | {item['answer']} | {item['source_n']} | "
            f"`{item['qid']}` | SAT-Math-Hard-PSDA-66-keys.pdf p.{item['keys_page']} |"
        )
    lines += [
        "",
        "## Held out (already in Modules 01–08)",
        "",
        "| Bank # | Where she sees / saw it |",
        "|---|---|",
    ]
    for src in sorted(used_where):
        lines.append(f"| {src} | {used_where[src]} |")
    lines.append("")
    module_key = OUT_KEYS / "psda-unseen-key.md"
    text = "\n".join(lines) + "\n"
    module_key.write_text(text)
    err = HERE.parents[3] / "error-log" / "psda-unseen-key.md"
    err.write_text(
        text.replace(
            "[`../student/psda-unseen.pdf`](../student/psda-unseen.pdf)",
            "[`../official/suitebank/SAT-Math-Hard-exclude-active/modules/student/psda-unseen.pdf`](../official/suitebank/SAT-Math-Hard-exclude-active/modules/student/psda-unseen.pdf)",
        )
    )
    return student, module_key


def verify(miss_pdf: Path, psda_pdf: Path) -> None:
    miss = PdfReader(str(miss_pdf))
    # cover + 41 items
    if len(miss.pages) != 42:
        raise SystemExit(f"miss review: {len(miss.pages)} pages, expected 42")
    psda = PdfReader(str(psda_pdf))
    # cover + 34 items
    if len(psda.pages) != 35:
        raise SystemExit(f"unseen PSDA: {len(psda.pages)} pages, expected 35")
    print(f"verify: miss-review {len(miss.pages)}p, unseen PSDA {len(psda.pages)}p")


def main() -> int:
    mods = load_manifest()
    readers = {d: PdfReader(str(meta["student"])) for d, meta in DOMAINS.items()}
    miss_pdf, miss_key = build_miss_review(mods, readers)
    psda_pdf, psda_key = build_unseen_psda(mods, readers)
    verify(miss_pdf, psda_pdf)
    print(f"wrote {miss_pdf}")
    print(f"wrote {miss_key}")
    print(f"wrote {psda_pdf}")
    print(f"wrote {psda_key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
