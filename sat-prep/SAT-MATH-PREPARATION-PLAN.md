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
4. A **fully concrete Weekend 1 lesson plan** for **Saturday 4h + Sunday 4h**, with:
   - minute-by-minute agenda
   - concepts to teach
   - worked examples
   - practice sets in SAT style
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
| Sequence | Concepts → then intensive practice | Fixed |
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
| Problem-Solving & Data Analysis | ~15% | 5–7 | Ratios/%, units, 1- and 2-var data, probability, stats claims |
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
  weekend-02/ …                      # stubs or full packs in later phases
  (optional later) pdf/              # exported PDFs if tooling available
```

Common App docs stay untouched under `docs/`.

---

## Teaching design

### Multi-weekend arc (Math-only)

| Weekend | Theme | Goal |
|---|---|---|
| **1 (this plan’s deep build)** | Digital SAT Math orientation + **Algebra complete** + Advanced Math kickoff | Close linear fluency gaps; start nonlinear |
| 2 | **Advanced Math** deep dive (quadratics, exponentials, equivalent expressions) | Accuracy on ~35% of test |
| 3 | Advanced Math finish + **PSDA** (ratios, %, data, probability) | Kill careless data/ratio misses |
| 4 | **Geometry & Trigonometry** + mixed adaptive strategy | Cover remaining ~15% + Module 1 pacing |
| 5 | Full Bluebook Math section(s) + error log clinic | Convert concepts → score |
| 6+ | Targeted weak-skill cram + timed modules | Push toward 780 |

Your stated model fits: Weekends 1–4 = concept runs; 5+ = cramming/practice denser.

### Weekend 1 concrete agenda (what you asked for)

#### Saturday — 4 hours (Algebra foundation)

| Block | Time | Content |
|---|---|---|
| 0 | 0:00–0:25 | Digital SAT Math orientation: adaptive modules, SPR grid, Desmos, pacing (~1.6 min/Q) |
| 1 | 0:25–1:25 | Linear equations in 1 variable; “isolate / clear fractions / check” routine |
| 2 | 1:25–2:15 | Linear equations in 2 variables; slope-intercept ↔ standard form; interpreting slope/intercept in context |
| Break | 2:15–2:25 | |
| 3 | 2:25–3:15 | Systems of two linear equations (substitution, elimination, graphing in Desmos) |
| 4 | 3:15–3:55 | Linear inequalities (1- and 2-variable); “which values satisfy” / graph shading intuition |
| 5 | 3:55–4:00 | Exit ticket: 3 mixed Algebra items + assign Question Bank filter homework |

#### Sunday — 4 hours (Algebra polish + Advanced Math start)

| Block | Time | Content |
|---|---|---|
| 0 | 0:00–0:20 | Saturday error review + “fast fail” checklist |
| 1 | 0:20–1:10 | Linear functions word problems (science/social context; ~30% of Math is in-context) |
| 2 | 1:10–2:00 | Equivalent expressions / factoring warm-up → bridge to Advanced Math |
| Break | 2:00–2:10 | |
| 3 | 2:10–3:10 | Quadratics: forms, zeros, vertex, Desmos graph check |
| 4 | 3:10–3:50 | Exponential growth/decay vs linear; interpreting parameters |
| 5 | 3:50–4:00 | Weekend recap + Week 2 preview + 15-item mixed set take-home |

Each concept block in the markdown will include:

- Learning objective
- Mini-lesson notes (instructor talk track)
- 1–2 fully worked examples
- 4–8 practice items (original SAT-style + links to official samples where available)
- Common traps for ~680 scorers aiming for 750–800

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

### Phase 2 — Weekend 1 full teaching pack

Write saturday/sunday scripts, practice set, answer key with worked solutions and Desmos notes.

**Acceptance:** Instructor can teach Weekend 1 from the markdown alone without inventing structure.

### Phase 3 — Stretch (if time) / stubs

Create `weekend-02/` … `weekend-04/` **outline stubs** (titles + skill lists) so the roadmap is tangible; full packs can follow after you approve Weekend 1 quality.

**Acceptance:** Stubs exist with skills + suggested hour splits.

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
3. Confirm Algebra-first Weekend 1 is OK (recommended) vs starting with her weakest domain from a question-level error log.
4. Preference: Markdown only, or Markdown + PDF.

---

## Execution status (updated 2026-08-20)

| Phase | Status |
|---|---|
| 0 Assumptions in README | Done |
| 1 Foundations docs | Done |
| 2 Weekend 1 full pack | Done — see `weekend-01/` |
| 3 Weekends 2–4 stubs | Done |
| 4 Optional PDF | Skipped (Markdown is source of truth) |
| 5 Commit + push | Done on `cursor/college-application-data-235e` |

**Next (only if requested):** expand `weekend-02/` … `weekend-04/` from stubs into full Sat/Sun packs; optional PDF export.
