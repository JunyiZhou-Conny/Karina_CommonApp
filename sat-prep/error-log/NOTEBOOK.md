# Karina SAT Math — miss notebook

Living instructor log. After each session, add what she actually missed. Next practice comes **only** from the active gaps below — not another full mixed packet.

**Why this exists:** The desk-packet Math Notes list skills one at a time (circle formula, percent change, perpendicular = negative reciprocal). The items she is falling on **stitch those skills together**. Isolated notes are not enough.

**Student-facing drill for the current gaps:** [`targeted-set-01.md`](targeted-set-01.md)  
**Your key:** [`targeted-set-01-key.md`](targeted-set-01-key.md)

Do **not** assign more easy Algebra, isolated center/radius circle lookups, or one-step linear slope items. Test 5 Module 1 was 24/27. That band is already warm.

---

## Active gaps

| ID | Knowledge point | Where it showed up | Status |
|---|---|---|---|
| **K1** | Successive percent = **multiply** growth factors, do not add the percents. Up 10% then up 10% is \(\times 1.1 \times 1.1 = 1.21\), not \(+20\%\). | Desk **B14**, desk **C4/C6**, Test 5 percent items | 🟨 teach |
| **K2** | “Increase \(x\) by \(p\%\)” means \(x(1+\frac{p}{100})\), not \(x\cdot\frac{p}{100}\). Increase by 400% is \(\times 5\). | Test 5 Math **Module 1 #25** | 🟨 teach |
| **K3** | Exponential model period: if \(P(t)=A(1+r)^{kt}\), there are \(k\) growth cycles per 1 unit of \(t\). Convert that period into months when the question asks for \(n\) months. | Test 5 Math **Module 2 #25** (Advanced Math) | 🟨 teach |
| **K4** | Tangent to a circle is **perpendicular to the radius** at the contact point. | Test 5 Math **Module 2 #26** | 🟨 teach |
| **K5** | Perpendicular slopes: \(m_1 m_2 = -1\) (negative reciprocal). Vertical radius \(\Rightarrow\) horizontal tangent (slope 0). | Test 5 Math **Module 2 #26**; desk Algebra note she did not apply | 🟨 teach |
| **K6** | Combo: circle equation \(\rightarrow\) center \(\rightarrow\) radius slope \(\rightarrow\) tangent slope \(\rightarrow\) point-slope line \(\rightarrow\) test a point. Not “just write \((x-h)^2+(y-k)^2=r^2\).” | Same official #26 vs desk D13-style notes | 🟨 teach |

When a gap is clean in a later session, change 🟨 to ✅ and **stop drilling it**.

---

## How to log the next session

Copy this block to the bottom of the session log.

```md
### YYYY-MM-DD — [source: Test N / desk / Bluebook]

| Item | Her answer | Official / key | Gap IDs | One-line why |
|---|---|---|---|---|
| | | | | |

New gaps to add to the table above:
- ...
```

Rules:

1. Write the **knowledge leak**, not “she got #26 wrong.”
2. If two topics collided, log the **collision** (K6), not only the formula she already has on the notes page.
3. Next drill set should be **new originals** on those IDs only.

---

## Session log

### 2026-08-21 — Official Test 5 Math + desk Advanced Math

**Score:** Module 1 24/27, Module 2 21/27 → raw 45 → paper conversion Math **640–700**.

You walked these with her. Official stems stay in the College Board PDFs; this log records the leak, not the copyrighted wording.

| Item | What SAT asked her to do | What she did not have ready | Gaps |
|---|---|---|---|
| Desk **B14** | Population 200, **+50% each decade**, 2 decades. SPR. | Treat each decade as \(\times 1.5\), then square. Likely added 50% twice (\(200+100+100\)) or did one step only. Key: \(200\times(1.5)^2=450\). | K1 |
| Desk **C4 / C6** (same family; you flagged PSDA successive %) | +25% then −25%; or +10% then +10%. | Same leak: adding percents, or thinking +10% twice is +20%. Keys: \(80\times1.25\times0.75=75\); \(800\times1.1^2=968\). | K1 |
| Test 5 Math **M1 #25** | “Increasing the quantity \(x\) by 400%” equals 60. | “Increase by 400%” \(\neq\) “400% of.” \(x+4x=5x=60\Rightarrow x=12\). Trap answers 15 and 240 sit on the wording. | K2 |
| Test 5 Math **M2 #25** | Exponential population model; 4% growth **every \(n\) months**. | Read the **exponent** as the clock. If the exponent is a multiple of \(t\) (years), convert 1 growth cycle into months. Official answer **A (8)**. | K3 |
| Test 5 Math **M2 #26** | Circle, given center and point of tangency; which other point is on the **tangent line**. | Did not start with “radius \(\perp\) tangent,” then \(m_r\cdot m_t=-1\), then point-slope at the contact point (not the center). Official answer **C**. | K4, K5, K6 |

**Official files (you, not her):**

- Questions: [`../official/tests/sat-practice-test-5-digital.pdf`](../official/tests/sat-practice-test-5-digital.pdf) — M1 #25 on booklet p. 41; M2 #25–26 on booklet p. 50
- Explanations: [`../official/answers/sat-practice-test-5-answers-digital.pdf`](../official/answers/sat-practice-test-5-answers-digital.pdf)
- Check sheet: [`../official/keys/test-05-math.md`](../official/keys/test-05-math.md)
- Desk B14 / C4 / C6: [`../print/SAT-MATH-DESK-PACKET.md`](../print/SAT-MATH-DESK-PACKET.md)

---

## What to say at the desk (short)

### Successive percent (K1)

- Each change is a **multiply**, not an add.
- Up \(p\%\) \(\Rightarrow\) \(\times(1+\frac{p}{100})\). Down \(p\%\) \(\Rightarrow\) \(\times(1-\frac{p}{100})\).
- Two identical ups: square the factor. +10% then +10% = \(\times 1.21\), which is a **21%** increase, not 20%.
- +10% then −10% is **not** back to start: \(\times 1.1\times 0.9=0.99\).

### “Increase by \(p\%\)” (K2)

- Increase by 100% = double (\(\times 2\)).
- Increase by 400% = add four copies of \(x\) = \(\times 5\).
- “400% **of** \(x\)” is the other sentence (\(\times 4\)). SAT uses both.

### Exponential period (K3)

- \(A(1+r)^{kt}\) completes \(k\) growth cycles in one year if \(t\) is in years.
- Months per cycle = \(12/k\).
- Example: exponent \(1.5t\) \(\Rightarrow\) 1.5 cycles/year \(\Rightarrow\) one cycle every 8 months.

### Tangent + perpendicular (K4–K6)

1. Plot center \(C\) and contact point \(P\). Segment \(CP\) is a **radius**.
2. A tangent at \(P\) is perpendicular to \(CP\).
3. \(m_{CP}=\dfrac{y_P-y_C}{x_P-x_C}\). Then \(m_t= -\dfrac{1}{m_{CP}}\), i.e. \(m_{CP}\cdot m_t=-1\).
4. Write the tangent with **point-slope at \(P\)**, never at \(C\).
5. Test each choice in that line. Points on the radius are the usual trap.

Desk Math Notes already had “perpendicular = negative reciprocal” and “\((x-h)^2+(y-k)^2=r^2\).” The missing page is the **glue** between them. That glue is now in the notes as “Combo moves.”

---

## Next sitting

Give her [`targeted-set-01.md`](targeted-set-01.md) only (12 items).  
Do not restart the 17-page packet from A1.  
After she finishes, mark each gap 🟨/✅ in the table and add a new session block.
