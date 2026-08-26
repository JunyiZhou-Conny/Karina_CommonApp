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

from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve().parent
PACK = HERE.parent
STUDENT_DIR = PACK / "student"
ANSWERS_DIR = PACK / "answers"
OUT_STUDENT = HERE / "student"
OUT_KEYS = HERE / "keys"

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


def stamp_question_number(page, n: int, module_label: str):
    """Overlay 'Module XX · Question N' in the top margin."""
    box = page.mediabox
    width = float(box.width)
    height = float(box.height)
    buf = HERE / f".stamp-{module_label}-{n:02d}.pdf"
    c = canvas.Canvas(str(buf), pagesize=(width, height))
    c.setFillColorRGB(0.12, 0.12, 0.12)
    c.setFont("Times-Bold", 12)
    c.drawString(36, height - 28, f"Module {module_label}   ·   Question {n}")
    c.setFont("Times-Roman", 9)
    c.drawRightString(width - 36, height - 28, "Suite Hard  ·  no calculator ban")
    c.save()
    overlay = PdfReader(str(buf)).pages[0]
    page.merge_page(overlay)
    buf.unlink(missing_ok=True)


def make_cover(path: Path, module: dict) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter
    c.setFont("Times-Bold", 22)
    c.drawString(0.9 * inch, h - 1.3 * inch, f"Suite Hard  ·  Simulation Module {module['label']}")
    c.setFont("Times-Roman", 13)
    n = len(module["items"])
    y = h - 1.85 * inch
    lines = [
        f"{n} questions   ·   {module['minutes']} minutes   ·   official SAT Math Hard",
        "Exclude-active: these items are not on current Bluebook full-length tests.",
        "All items are Hard. This is not an adaptive Module 1. It is harder than test day.",
        "Calculator / Desmos is allowed on every item, same as Bluebook.",
        "Question 1 is the first page after this cover. Write answers on the last page.",
        "***Read the prompt carefully.*** Write the job on scratch before you copy numbers.",
        "",
        "Domain mix in this module:",
    ]
    for line in lines:
        c.drawString(0.9 * inch, y, line)
        y -= 20
    quota = module["quota"]
    for domain in ("Algebra", "Advanced Math", "PSDA", "Geometry"):
        c.drawString(1.15 * inch, y, f"{domain}:  {quota.get(domain, 0)}")
        y -= 18
    c.setFont("Times-Italic", 11)
    c.drawString(0.9 * inch, 0.85 * inch, "Do not open the next module until this one is timed and scored.")
    c.save()


def make_answer_sheet(path: Path, module: dict) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter
    c.setFont("Times-Bold", 16)
    c.drawString(0.9 * inch, h - 0.9 * inch, f"Module {module['label']}  ·  answer sheet")
    c.setFont("Times-Roman", 11)
    c.drawString(0.9 * inch, h - 1.15 * inch, "Write one answer per line. SPR: integer, decimal, or fraction.")
    n = len(module["items"])
    split = (n + 1) // 2 if n > 11 else n
    c.setStrokeColorRGB(0.4, 0.4, 0.4)
    y = h - 1.55 * inch
    for i in range(1, split + 1):
        c.setFont("Times-Bold", 12)
        c.drawString(1.0 * inch, y, f"{i:2d}.")
        c.line(1.45 * inch, y - 2, 4.6 * inch, y - 2)
        y -= 28
    if n > split:
        y = h - 1.55 * inch
        for i in range(split + 1, n + 1):
            c.setFont("Times-Bold", 12)
            c.drawString(5.3 * inch, y, f"{i:2d}.")
            c.line(5.75 * inch, y - 2, 7.6 * inch, y - 2)
            y -= 28
    c.save()


def write_module_pdf(module: dict, readers: dict[str, PdfReader]) -> Path:
    OUT_STUDENT.mkdir(parents=True, exist_ok=True)
    cover_path = HERE / f".cover-{module['label']}.pdf"
    sheet_path = HERE / f".sheet-{module['label']}.pdf"
    make_cover(cover_path, module)
    make_answer_sheet(sheet_path, module)

    writer = PdfWriter()
    writer.add_page(PdfReader(str(cover_path)).pages[0])
    for i, item in enumerate(module["items"], start=1):
        page = readers[item["domain"]].pages[item["source_n"] - 1]
        # clone via a one-page writer so we do not mutate the source reader
        tmp = PdfWriter()
        tmp.add_page(page)
        cloned = tmp.pages[0]
        stamp_question_number(cloned, i, module["label"])
        writer.add_page(cloned)
    writer.add_page(PdfReader(str(sheet_path)).pages[0])

    out = OUT_STUDENT / f"module-{module['label']}.pdf"
    with out.open("wb") as f:
        writer.write(f)
    cover_path.unlink(missing_ok=True)
    sheet_path.unlink(missing_ok=True)
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
        "1. Print [`student/module-01.pdf`](student/module-01.pdf) (cover + 22 items + answer sheet).",
        "2. 35 minutes, no pausing. Then score from the matching key.",
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
        expected_pages = 1 + len(m["items"]) + 1
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
