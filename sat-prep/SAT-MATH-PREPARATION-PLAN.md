# Plan: Digital SAT Math Weekend Curriculum (Karina)

> **This file is SAT prep only.** It is intentionally separate from the Common App / supplementary-essay packet under `docs/`.  
> Do not merge SAT materials into `docs/supplemental-essays-and-plans-2026-27.md`.

## Repo separation (important)

| Workstream | Location | Purpose |
|---|---|---|
| **Common App / essays / college list** | `docs/` | Supplemental essay prompts, ED/EA/RD deadlines |
| **SAT Math preparation** | `sat-prep/` (this folder) | Digital SAT structure, Math content map, weekend lesson plans |

## Executive Summary

Build an **up-to-date Digital SAT Math** teaching packet inside **`sat-prep/`** in the existing `Karina_CommonApp` repo, focused on raising Math from ~**680 → ~780**.

Primary deliverables:

1. A short **Digital SAT structure primer** (what changed vs the old paper SAT).
2. A complete **College Board Math content map** (4 domains → concrete skills).
3. A **multi-weekend curriculum roadmap** aligned to your teaching model: *concepts first, then drill*.
4. **Fully concrete Weekend 1–4 lesson packs** for **Saturday 4h + Sunday 4h**, with:
   - minute-by-minute agenda
   - Q&A / nitpick mode (student already knows the basics)
   - Weekend 1 = **all four domains** at high level
   - Weekends 2–4 = deep dive on Advanced Math, PSDA, Geometry & Trig
   - practice sets in SAT style + answer keys
   - Desmos / Bluebook tips
5. Readable **Markdown** docs (optional PDF export). Not Jupyter notebooks.

**No new GitHub repository.** Everything lives under `sat-prep/` in the current repo.

---

## Student / coaching context (assumptions)

| Item | Assumption | Needs confirm? |
|---|---|---|
| Practice Math score | ~680 | Exact Bluebook score report preferred |
| Total score | “1000 and 140” → likely **1140** (or 1040) | Confirm exact total + RW |
| Target Math | ~780 (+100) | Confirm |
| Cadence | Sat 4h + Sun 4h | Fixed |
| Sequence | High-level survey of all four → then intensive practice / nitpick | Fixed |
| First focus | Math only (RW later) | Fixed unless you say otherwise |

**Important score math check:** If Math is 680 and total is 1040, Reading & Writing would be ~360. If total is 1140, RW ≈ 460. Please confirm the score report so we don’t mis-prioritize later.

---

## What “current SAT Math” means (research basis)

We will ground materials in **College Board Digital SAT Suite** specs (not 2016–2023 paper SAT):

- **Platform:** Bluebook app; multistage **adaptive** (Module 2 harder/easier based on Module 1).
- **Math timing:** 2 modules × **35 minutes**, **22 questions** each (20 scored + 2 pretest) → **44 Q / 70 min**.
- **Formats:** ~75% multiple choice, ~25% student-produced response (SPR).
- **Calculator:** Allowed **entire** Math section; built-in **Desmos** graphing calculator + personal approved calculator.
- **Ordering:** Within a module, generally easier → harder.
- **Domains (every module mixes all four):**

| Domain | Approx. share | # questions | Core skills |
|---|---|---|---|
| Algebra | ~35% | 13–15 | Linear equations/inequalities, linear functions, systems |
| Advanced Math | ~35% | 13–15 | Nonlinear: quadratic, exponential, absolute value, polynomials, rationals, radicals |
| Problem-Solving & Data Analysis (**PSDA**) | ~15% | 5–7 | Ratios/%, units, 1- and 2-var data, probability, stats claims |
| Geometry & Trigonometry | ~15% | 5–7 | Area/volume, angles/triangles, right-triangle trig, circles |

Sources to cite in docs: College Board Math Overview, Digital SAT Specs Overview PDF, Official Bluebook practice, Student Question Bank.

### Authentic practice policy (copyright-safe)

We will **not** dump full Bluebook practice tests or pirated “real past papers” into the repo.

Instead:

1. **Link + cite** College Board public sample questions / Official Digital SAT sample PDFs.
2. Teach how to pull filtered items from the **Official Student Question Bank** (by domain/skill/difficulty).
3. Write **original SAT-style** questions matching each skill (with full solutions), clearly labeled as instructor-created.
4. Optional: paste only items College Board explicitly publishes for free educational use, with attribution and source URL.

This keeps the packet usable, legal, and still “exam-real.”

---

## Repo layout (to create)

```text
sat-prep/
  README.md                          # how instructor + student use this folder
  CURRICULUM.md                      # multi-weekend roadmap + goals
  00-digital-sat-overview.md         # structure, scoring, Bluebook/Desmos changes
  01-math-content-map.md             # full skill checklist by domain
  resources.md                       # Bluebook, Question Bank, Khan, Desmos links
  weekend-01/
    README.md                        # Sat/Sun overview + goals
    saturday.md                      # 4-hour script + concepts + examples + set
    sunday.md                        # 4-hour script + concepts + examples + set
    practice-set-01.md               # mixed practice for weekend 1
    answer-key-01.md                 # full worked solutions
  weekend-02/ … weekend-04/          # full Sat/Sun packs (not stubs)
  (optional later) pdf/              # exported PDFs if tooling available
```

Common App docs stay untouched under `docs/`.

---

## Teaching design

### Multi-weekend arc (Math-only)

| Weekend | Theme | Goal |
|---|---|---|
| **1** | **All four domains** at high level (Q&A / nitpick) + mixed diagnostic | She already knows the basics; diagnose leaks |
| 2 | **Advanced Math** deep dive (equivalent expressions, abs/rational/radical, exponentials, nonlinear systems) | Accuracy on ~35% of test |
| 3 | **PSDA** (ratios, %, data, probability, margin of error, study claims) | Kill careless wording / table misses |
| 4 | **Geometry & Trigonometry** + Module 1 mixed simulation | Cover remaining ~15% + pacing |
| 5 | Full Bluebook Math section(s) + error log clinic | Convert concepts → score |
| 6+ | Targeted weak-skill cram + timed modules | Push toward 780 |

**PSDA** = Problem-Solving and Data Analysis. Not a fifth subject — it is College Board’s name for the story / table / percent / probability slice.

Weekend 1 is a **tour of all four**. Weekends 2–4 go deep. 5+ = official timed practice.

### Weekend 1 concrete agenda (updated)

Student is familiar with A–D. Saturday is **not** an Algebra-only course.

#### Saturday — 4 hours (all four domains)

| Block | Time | Content |
|---|---|---|
| 0 | 0:00–0:20 | Orientation + name the four domains + what **PSDA** means |
| 1 | 0:20–1:10 | Algebra A1–A5 Q&A + rapid items |
| 2 | 1:10–2:00 | Advanced Math B1–B4 Q&A + rapid items |
| Break | 2:00–2:10 | |
| 3 | 2:10–3:00 | PSDA C1–C7 Q&A + rapid items |
| 4 | 3:00–3:50 | Geometry & Trig D1–D4 Q&A + rapid items |
| 5 | 3:50–4:00 | Exit ticket: one item per domain |

#### Sunday — 4 hours (mixed diagnostic + nitpick)

| Block | Time | Content |
|---|---|---|
| 0 | 0:00–0:20 | Saturday miss review |
| 1 | 0:20–0:45 | Timed 12-item mixed diagnostic (all four) |
| 2 | 0:45–1:40 | Nitpick clinic on the diagnostic |
| Break | 1:40–1:50 | |
| 3 | 1:50–3:10 | Four-domain pressure stations (student talks setup first) |
| 4 | 3:10–3:50 | SPR + Desmos + Module 1 habits |
| 5 | 3:50–4:00 | 16-item all-domain take-home |

Each content block is **Q&A first**, then items, then a 5-minute trap recap — not a from-scratch mini-lesson. Extra linear reps live in `weekend-01/optional-algebra-drill.md` if Algebra is actually sloppy.

---

## Execution phases

### Phase 0 — Clarify scores (parallel, non-blocking)

Capture exact Math/RW/total + Bluebook practice test number if known. Defaults proceed with Math ~680 → ~780.

**Acceptance:** Assumptions logged in `sat-prep/README.md`.

### Phase 1 — Foundations docs

Write:

- `00-digital-sat-overview.md`
- `01-math-content-map.md` (every College Board skill listed as a checklist)
- `CURRICULUM.md`
- `resources.md`
- root `sat-prep/README.md`
- Update repo root `README.md` to link Common App docs + SAT prep

**Acceptance:** Accurate Digital SAT facts; domain table matches College Board; no paper-SAT leftovers (no separate no-calc section).

### Phase 2 — Weekend 1 full teaching pack (all four domains)

Write saturday/sunday scripts, practice set, answer key. Saturday covers A+B+C+D at high level.

**Acceptance:** Instructor can teach Weekend 1 from the markdown alone without inventing structure.

### Phase 3 — Weekends 2–4 full packs

Full Sat/Sun scripts + practice sets + answer keys for Advanced Math, PSDA, Geometry & Trig.

**Acceptance:** Each weekend folder is teachable the same way as Weekend 1.

### Phase 4 — Optional PDF

If `pandoc`/`weasyprint` available, export Weekend 1 pack to PDF; otherwise keep Markdown as source of truth.

### Phase 5 — Commit + push

Commit on current branch (or a new `cursor/sat-math-prep-…` branch if cleaner) and push to the same GitHub repo.

---

## Testing / QA

- Fact-check overview against College Board specs PDF + Math overview page.
- Every skill in content map maps to a College Board domain skill name.
- Practice items tagged by domain/skill/difficulty.
- Answer key independently re-solved.
- Copyright review: no unauthorized full-form dumps.

---

## Out of scope (unless you expand)

- Full Reading & Writing curriculum
- Live interactive web app / Khan clone
- Guaranteeing a specific score
- Paying for third-party question banks or uploading copyrighted Bluebook forms

---

## What I need from you (optional but helpful)

1. Exact practice score report (Math / RW / total; Bluebook test # if any).
2. Next real SAT date (or target month).
3. After Weekend 1, which domain leaked most (use that to decide extra Question Bank filters).
4. Preference: Markdown only, or Markdown + PDF.

---

## Execution status (updated 2026-08-20)

| Phase | Status |
|---|---|
| 0 Assumptions in README | Done |
| 1 Foundations docs | Done |
| 2 Weekend 1 full pack (all four domains, Q&A) | Done — see `weekend-01/` |
| 3 Weekends 2–4 **full packs** | Done — see `weekend-02/` … `weekend-04/` |
| 4 Optional PDF | Skipped (Markdown is source of truth) |
| 5 Commit + push | On `cursor/sat-weekend-packs-f685` |

**Next (only if requested):** Weekend 5 Bluebook clinic notes; PDF export; plug in exact scores / test date.
