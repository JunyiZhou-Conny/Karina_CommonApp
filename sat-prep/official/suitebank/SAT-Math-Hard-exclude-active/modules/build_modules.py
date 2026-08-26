#!/usr/bin/env python3
"""Shuffle the 340 Hard SAT Math items into mixed 22-question simulation modules.

Source: official Suite Bank exports (exclude-active). Student PDFs are 1 page / item.
Do not give the keys folder to Karina.
"""

from __future__ import annotations

import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve().parent
PACK = HERE.parent
STUDENT_DIR = PACK / "student"
ANSWERS_DIR = PACK / "answers"
OUT_STUDENT = HERE / "student"
OUT_KEYS = HERE / "keys"
# Standard SAT Math directions + reference (same wording/layout on every official booklet).
OFFICIAL_DIRECTIONS = HERE.parents[2] / "tests/sat-practice-test-4-digital.pdf"
DIRECTIONS_PAGE_INDEXES = (31, 32)  # 1-based pages 32–33

SEED = 20260826
FULL_SIZE = 22
N_FULL = 15
REM_SIZE = 10

DOMAINS = {
    "Algebra": {
        "short": "Alg",
        "count": 84,
        "student": STUDENT_DIR / "SAT-Math-Hard-Algebra-84.pdf",
        "keys": ANSWERS_DIR / "SAT-Math-Hard-Algebra-84-keys.pdf",
        "sheet": ANSWERS_DIR / "SAT-Math-Hard-Algebra-84-check-sheet.md",
    },
    "Advanced Math": {
        "short": "Adv",
        "count": 102,
        "student": STUDENT_DIR / "SAT-Math-Hard-AdvancedMath-102.pdf",
        "keys": ANSWERS_DIR / "SAT-Math-Hard-AdvancedMath-102-keys.pdf",
        "sheet": ANSWERS_DIR / "SAT-Math-Hard-AdvancedMath-102-check-sheet.md",
    },
    "PSDA": {
        "short": "PSDA",
        "count": 66,
        "student": STUDENT_DIR / "SAT-Math-Hard-PSDA-66.pdf",
        "keys": ANSWERS_DIR / "SAT-Math-Hard-PSDA-66-keys.pdf",
        "sheet": ANSWERS_DIR / "SAT-Math-Hard-PSDA-66-check-sheet.md",
    },
    "Geometry": {
        "short": "Geo",
        "count": 88,
        "student": STUDENT_DIR / "SAT-Math-Hard-GeoTrig-88.pdf",
        "keys": ANSWERS_DIR / "SAT-Math-Hard-GeoTrig-88-keys.pdf",
        "sheet": ANSWERS_DIR / "SAT-Math-Hard-GeoTrig-88-check-sheet.md",
    },
}

ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|$"
)


def parse_check_sheet(path: Path, domain: str) -> list[dict]:
    items = []
    for line in path.read_text().splitlines():
        m = ROW_RE.match(line.strip())
        if not m:
            continue
        num, answer, qid, keys_page = m.groups()
        items.append(
            {
                "domain": domain,
                "source_n": int(num),
                "answer": answer.strip(),
                "qid": qid,
                "keys_page": int(keys_page),
            }
        )
    return items


def load_bank() -> dict[str, list[dict]]:
    bank = {}
    for domain, meta in DOMAINS.items():
        items = parse_check_sheet(meta["sheet"], domain)
        if len(items) != meta["count"]:
            raise SystemExit(
                f"{domain}: check sheet has {len(items)} rows, expected {meta['count']}"
            )
        reader = PdfReader(str(meta["student"]))
        if len(reader.pages) != meta["count"]:
            raise SystemExit(
                f"{domain}: student PDF has {len(reader.pages)} pages, expected {meta['count']}"
            )
        for item in items:
            if item["source_n"] < 1 or item["source_n"] > len(reader.pages):
                raise SystemExit(f"{domain}: bad source_n {item['source_n']}")
        bank[domain] = items
    return bank


def apportion_remainder(counts: dict[str, int], rem_size: int) -> dict[str, int]:
    """Hamilton apportionment, at least 1 per domain, mix the leftover 10."""
    total = sum(counts.values())
    raw = {k: counts[k] * rem_size / total for k in counts}
    take = {k: max(1, int(raw[k])) for k in counts}
    while sum(take.values()) > rem_size:
        k = max(take, key=lambda d: (take[d] - raw[d], take[d]))
        if take[k] > 1:
            take[k] -= 1
        else:
            break
    while sum(take.values()) < rem_size:
        k = max(counts, key=lambda d: raw[d] - take[d])
        take[k] += 1
    return take


def allocate_full_modules(pool: dict[str, int], n_full: int, full_size: int) -> list[dict[str, int]]:
    """Each module gets all four domains; counts sum to 22; pool is emptied."""
    remaining = dict(pool)
    schedule: list[dict[str, int]] = []
    names = list(remaining)
    for i in range(n_full):
        left = n_full - i
        take = {}
        for d in names:
            later = left - 1
            # Leave later modules at least 3 of this domain when stock allows.
            min_leave = 3 * later if remaining[d] >= 3 * later else max(0, remaining[d] - 8)
            max_now = remaining[d] - min_leave
            target = remaining[d] / left
            take[d] = int(target)
            lo = 3 if remaining[d] >= 3 * left else (1 if remaining[d] >= left else 0)
            take[d] = min(max(take[d], lo), max_now, 8)
        def bump(delta: int) -> None:
            order = sorted(
                names,
                key=lambda d: (
                    remaining[d] - take[d],
                    remaining[d] / left - take[d],
                ),
                reverse=delta > 0,
            )
            for d in order:
                later = left - 1
                min_leave = 3 * later if remaining[d] >= 3 * later else max(0, remaining[d] - 8)
                max_now = remaining[d] - min_leave
                if delta > 0 and take[d] < min(8, max_now):
                    take[d] += 1
                    return
                if delta < 0 and take[d] > (3 if remaining[d] >= 3 * left else 0):
                    take[d] -= 1
                    return
            raise RuntimeError(f"cannot adjust module {i+1}: {take} remaining={remaining}")

        guard = 0
        while sum(take.values()) != full_size:
            bump(1 if sum(take.values()) < full_size else -1)
            guard += 1
            if guard > 40:
                raise RuntimeError(f"stuck allocating module {i+1}: {take} rem={remaining}")
        for d in names:
            remaining[d] -= take[d]
            if remaining[d] < 0:
                raise RuntimeError(f"overdrew {d} on module {i+1}")
        schedule.append(take)
    if any(remaining.values()):
        raise RuntimeError(f"leftover after 15 modules: {remaining}")
    return schedule


def interleave(groups: dict[str, list[dict]], rng: random.Random) -> list[dict]:
    """Round-robin so a module is not a domain clump."""
    order = list(groups)
    rng.shuffle(order)
    queues = {d: list(groups[d]) for d in order}
    out: list[dict] = []
    while any(queues.values()):
        for d in order:
            if queues[d]:
                out.append(queues[d].pop(0))
    return out


def build_roster(bank: dict[str, list[dict]]) -> list[dict]:
    rng = random.Random(SEED)
    shuffled = {d: list(items) for d, items in bank.items()}
    for d in shuffled:
        rng.shuffle(shuffled[d])

    counts = {d: len(shuffled[d]) for d in shuffled}
    rem_q = apportion_remainder(counts, REM_SIZE)
    pool = {d: counts[d] - rem_q[d] for d in counts}
    full_q = allocate_full_modules(pool, N_FULL, FULL_SIZE)

    modules = []
    cursor = {d: 0 for d in shuffled}

    def take(domain: str, n: int) -> list[dict]:
        start = cursor[domain]
        chunk = shuffled[domain][start : start + n]
        cursor[domain] = start + n
        if len(chunk) != n:
            raise RuntimeError(f"short take {domain} {n}")
        return chunk

    for i, quota in enumerate(full_q, start=1):
        groups = {d: take(d, quota[d]) for d in quota if quota[d]}
        items = interleave(groups, rng)
        modules.append(
            {
                "id": i,
                "label": f"{i:02d}",
                "kind": "full",
                "minutes": 35,
                "quota": quota,
                "items": items,
            }
        )

    rem_groups = {d: take(d, rem_q[d]) for d in rem_q if rem_q[d]}
    rem_items = interleave(rem_groups, rng)
    modules.append(
        {
            "id": 16,
            "label": "16",
            "kind": "remainder",
            "minutes": 16,
            "quota": rem_q,
            "items": rem_items,
        }
    )

    used = [(it["domain"], it["source_n"]) for m in modules for it in m["items"]]
    if len(used) != 340 or len(set(used)) != 340:
        raise RuntimeError(f"item coverage broken: {len(used)} / unique {len(set(used))}")
    if any(cursor[d] != len(shuffled[d]) for d in shuffled):
        raise RuntimeError(f"unused tail: {cursor}")
    return modules


def _html_y_to_pdf(y_from_top: float, page_h: float = 792.0) -> float:
    return page_h - y_from_top


def _overlay_pdf(page, draw) -> None:
    buf = HERE / f".overlay-{id(page)}.pdf"
    box = page.mediabox
    c = canvas.Canvas(str(buf), pagesize=(float(box.width), float(box.height)))
    draw(c, float(box.width), float(box.height))
    c.save()
    page.merge_page(PdfReader(str(buf)).pages[0])
    buf.unlink(missing_ok=True)


def official_directions_pages(module: dict) -> list:
    """Official SAT Math directions + reference, with this module's count."""
    if not OFFICIAL_DIRECTIONS.exists():
        raise SystemExit(f"missing official directions: {OFFICIAL_DIRECTIONS}")
    src = PdfReader(str(OFFICIAL_DIRECTIONS))
    n = len(module["items"])
    mod_n = str(module["id"])
    pages = []

    def patch_count(c, w, h):
        # Official booklet says "27 QUESTIONS". Cover just that number.
        x0, x1 = 124.0, 146.0
        y0, y1 = _html_y_to_pdf(161.2), _html_y_to_pdf(141.8)
        c.setFillColorRGB(1, 1, 1)
        c.rect(x0, y0, x1 - x0, y1 - y0, fill=1, stroke=0)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 13)
        label = str(n)
        c.drawCentredString((x0 + x1) / 2, y0 + 4, label)

    def patch_module(c, w, h, x_center: float):
        # Official header "Module / 1" — write this module number.
        c.setFillColorRGB(0.82, 0.82, 0.82)  # match the gray header pill
        c.rect(x_center - 14, _html_y_to_pdf(65.0), 28, 26, fill=1, stroke=0)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 16 if len(mod_n) == 1 else 13)
        c.drawCentredString(x_center, _html_y_to_pdf(61.5), mod_n)

    for i, idx in enumerate(DIRECTIONS_PAGE_INDEXES):
        tmp = PdfWriter()
        tmp.add_page(src.pages[idx])
        page = tmp.pages[0]
        first = i == 0
        needs_overlay = first or module["id"] != 1
        if needs_overlay:

            def draw(c, w, h, first=first):
                if first:
                    patch_count(c, w, h)
                if module["id"] != 1:
                    patch_module(c, w, h, 297.4 if first else 315.4)

            _overlay_pdf(page, draw)
        pages.append(page)
    return pages


QUESTION_BAR = 34


def labeled_question_page(src_page, n: int, total: int, module_id: int):
    """Official item page, shifted down, with a SAT-style Question N of M bar on top."""
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
        c.drawRightString(w - 22, h - QUESTION_BAR + 13, f"Module {module_id}")
        c.setStrokeColorRGB(0.55, 0.55, 0.55)
        c.setLineWidth(0.6)
        c.line(0, h - QUESTION_BAR, w, h - QUESTION_BAR)

    _overlay_pdf(page, draw)
    return page


def write_module_pdf(module: dict, readers: dict[str, PdfReader]) -> Path:
    OUT_STUDENT.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    for page in official_directions_pages(module):
        writer.add_page(page)
    total = len(module["items"])
    for i, item in enumerate(module["items"], start=1):
        writer.add_page(
            labeled_question_page(
                readers[item["domain"]].pages[item["source_n"] - 1],
                i,
                total,
                module["id"],
            )
        )
    out = OUT_STUDENT / f"module-{module['label']}.pdf"
    with out.open("wb") as f:
        writer.write(f)
    return out


def write_module_key(module: dict) -> Path:
    OUT_KEYS.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Suite Hard · Module {module['label']} — instructor key",
        "",
        "Do **not** give this page to Karina. Student file: "
        f"[`../student/module-{module['label']}.pdf`](../student/module-{module['label']}.pdf).",
        "",
        f"{len(module['items'])} items · {module['minutes']} minutes · seed `{SEED}`.",
        "",
        "| # | Answer | Domain | Source # | Question ID | Keys page |",
        "|---|---|---|---|---|---|",
    ]
    for i, item in enumerate(module["items"], start=1):
        src = DOMAINS[item["domain"]]["keys"].name
        lines.append(
            f"| {i} | {item['answer']} | {item['domain']} | {item['source_n']} | "
            f"`{item['qid']}` | {src} p.{item['keys_page']} |"
        )
    quota = module["quota"]
    mix = ", ".join(f"{d} {quota.get(d, 0)}" for d in ("Algebra", "Advanced Math", "PSDA", "Geometry"))
    lines += ["", f"**Mix:** {mix}.", ""]
    path = OUT_KEYS / f"module-{module['label']}-key.md"
    path.write_text("\n".join(lines) + "\n")
    return path


def write_master_key(modules: list[dict]) -> Path:
    lines = [
        "# Suite Hard simulation modules — master instructor key",
        "",
        "Do **not** print this for Karina. Give her one student module PDF at a time.",
        "",
        f"Seed `{SEED}`. 15 modules × 22 = 330, plus Module 16 remainder of 10 = **340**.",
        "Every official Hard exclude-active item is used once. Domains are shuffled and mixed.",
        "",
        "A 5/5/6/6 split is not possible: PSDA only has **66** Hard items (that split would need 90). "
        "The builder keeps all four domains in every 22-item module and spends the extra Advanced Math / Geometry stock. "
        "Typical mix is about 5–6 Algebra, 6–8 Advanced, 4–5 PSDA, 5–6 Geometry.",
        "",
        "| Module | Items | Min | Algebra | Adv | PSDA | Geo | Student PDF | Key |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for m in modules:
        q = m["quota"]
        lines.append(
            f"| {m['label']} | {len(m['items'])} | {m['minutes']} | "
            f"{q.get('Algebra', 0)} | {q.get('Advanced Math', 0)} | "
            f"{q.get('PSDA', 0)} | {q.get('Geometry', 0)} | "
            f"[module-{m['label']}.pdf](student/module-{m['label']}.pdf) | "
            f"[key](keys/module-{m['label']}-key.md) |"
        )
    lines += [
        "",
        "## How to sit",
        "",
        "1. Print [`student/module-01.pdf`](student/module-01.pdf). Pages 1–2 are the official SAT Math directions + reference. Question 1 starts on page 3; each item has **Question N of 22** above the official page.",
        "2. 35 minutes, no pausing. Score from the matching key in [`keys/`](keys/) — do not put answers in the student PDF.",
        "3. Log misses by **module # + item #** (and domain). Do not restack a clean domain.",
        "4. Next unused official Bluebook sit is still **4, 6, 7, 8, or 10** — these modules do not replace that.",
        "",
    ]
    path = HERE / "README.md"
    path.write_text("\n".join(lines) + "\n")
    return path


def write_manifest(modules: list[dict]) -> Path:
    payload = {
        "seed": SEED,
        "source": "SAT Suite Educator Question Bank · SAT · Math · Hard · exclude active",
        "total_items": 340,
        "modules": [
            {
                "id": m["id"],
                "label": m["label"],
                "kind": m["kind"],
                "minutes": m["minutes"],
                "quota": m["quota"],
                "items": [
                    {
                        "n": i,
                        "domain": it["domain"],
                        "source_n": it["source_n"],
                        "qid": it["qid"],
                        "answer": it["answer"],
                        "keys_page": it["keys_page"],
                    }
                    for i, it in enumerate(m["items"], start=1)
                ],
            }
            for m in modules
        ],
    }
    path = HERE / "manifest.json"
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return path


def verify(modules: list[dict], bank: dict[str, list[dict]]) -> None:
    answer_by = {(it["domain"], it["source_n"]): it["answer"] for d in bank for it in bank[d]}
    qid_by = {(it["domain"], it["source_n"]): it["qid"] for d in bank for it in bank[d]}
    seen = []
    for m in modules:
        pdf = OUT_STUDENT / f"module-{m['label']}.pdf"
        reader = PdfReader(str(pdf))
        expected_pages = 2 + len(m["items"])  # official directions + items
        if len(reader.pages) != expected_pages:
            raise SystemExit(f"module {m['label']}: {len(reader.pages)} pages, expected {expected_pages}")
        if len(set(it["domain"] for it in m["items"])) < (4 if m["kind"] == "full" else 3):
            raise SystemExit(f"module {m['label']} is not mixed enough: {m['quota']}")
        if m["kind"] == "full" and len(m["items"]) != 22:
            raise SystemExit(f"module {m['label']} has {len(m['items'])} items")
        key = (OUT_KEYS / f"module-{m['label']}-key.md").read_text()
        for i, it in enumerate(m["items"], start=1):
            seen.append((it["domain"], it["source_n"]))
            if it["answer"] != answer_by[(it["domain"], it["source_n"])]:
                raise SystemExit(f"answer drift {m['label']} #{i}")
            if it["qid"] != qid_by[(it["domain"], it["source_n"])]:
                raise SystemExit(f"qid drift {m['label']} #{i}")
            if it["qid"] not in key:
                raise SystemExit(f"key missing qid {it['qid']} in module {m['label']}")
    if len(seen) != 340 or len(set(seen)) != 340:
        raise SystemExit(f"verify coverage {len(seen)} unique {len(set(seen))}")
    print("verify: 16 PDFs, 340 unique items, answers match check sheets")


def main() -> int:
    bank = load_bank()
    modules = build_roster(bank)
    readers = {d: PdfReader(str(meta["student"])) for d, meta in DOMAINS.items()}
    for m in modules:
        write_module_pdf(m, readers)
        write_module_key(m)
        q = m["quota"]
        print(
            f"module {m['label']}: {len(m['items'])}q  "
            f"A{q.get('Algebra', 0)} V{q.get('Advanced Math', 0)} "
            f"P{q.get('PSDA', 0)} G{q.get('Geometry', 0)}"
        )
    write_master_key(modules)
    write_manifest(modules)
    verify(modules, bank)
    return 0


if __name__ == "__main__":
    sys.exit(main())
