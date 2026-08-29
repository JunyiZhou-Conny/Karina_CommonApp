# Targeted SAT Math — Set 05

**Student:** Karina  
**Homework after Bluebook Practice Test 6 and Suite Hard Module 01.** Work on paper. Calculator / Desmos is fine.

These are **new** questions on the items that missed — not those official questions, and not copies from Sets 01–04.

**SPR** = student-produced response. Write a number (integer, decimal, or fraction). On **#7** and **#8**, also write the four event sentences and the formula before you compute.

***Write the job first.***

<style>
.circ-lead {
  color: #b00000;
  font-style: italic;
  font-weight: 800;
  font-size: 1.2em;
  border: 2.5px solid #b00000;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.45em;
  height: 1.45em;
  line-height: 1;
  margin: 0 0.12em;
  vertical-align: -0.15em;
  font-family: Georgia, "Times New Roman", serif;
}
.blank-line { border-bottom: 1px solid #333; display: inline-block; min-width: 22em; height: 1.15em; }
</style>

---

## 1. Notes for this set only

### Polynomial in factor form — the constant \(c\)

If the zeros are \(r,s,t\), a monic cubic is

\[h(x)=(x-r)(x-s)(x-t)=x^3+\cdots+c.\]

The constant \(c\) is what you get when you multiply the three constant pieces of those factors. You do **not** need \(a\) or \(b\).

- Zeros \(-2,-3,4\) means the factors are \((x+2)(x+3)(x-4)\). The constant is \(2\cdot 3\cdot(-4)\), not a guess from multiplying the zeros raw.
- Same idea for a degree-6 polynomial: six factors, six constants, multiply.
- If the leading coefficient is **not** 1, multiply that leading number through at the end. \(c\) scales with it. Look at the number in front of the highest power of \(x\) before you multiply.

### Finish the rectangle

If one side is \(d\) more than the other and they give a diagonal (or the square of a diagonal), write

\[x^2+(x+d)^2=\text{(diagonal)}^2\]

and solve. Ugly numbers are not a signal to hunt for a trick. They are a signal to write Pythagorean and finish.

### Infinitely many solutions

Two linear expressions in \(x\) are the **same line** when matching coefficients are equal: the \(x\)-coefficients match, **and** the constants match.

If the right-hand side already shows a constant \(K\), and the question asks for the constant term of the expanded left-hand side, that constant **is** \(K\). You do not have to finish the expansion.

If they ask for the value of \(p\) that makes a system have infinitely many solutions, scale one equation until the \(x\) and \(y\) pieces match, then force the constants to match too. That same \(p\) is also the cutoff: any other value of \(p\) gives **no** solution (parallel, different constant).

### Minimum of a quadratic — which \(x\)

For \(f(x)=ax^2+bx+c\) with \(a>0\), the minimum is at

\[x=-\dfrac{b}{2a}.\]

That is the whole job if they asked for the \(x\)-value. Completing the square finds the vertex \((h,k)\). You do not need \(k\) unless they asked for the minimum **value**.

### Conditional probability — write the events first

\[P(A\mid B)=\dfrac{P(A\cap B)}{P(B)}\]

- Event \(A\) is a yes/no sentence about the random pick.
- Event \(B\) is a different yes/no sentence.
- Event \(A\cap B\) is **both** sentences at once. The symbol \(\cap\) means “and.”
- Event \(A\mid B\) is “\(A\) happens, **restricted to the cases where \(B\) already happened**.” The denominator is no longer the whole table. It is only the \(B\) column (or row).
- \(P(B)\) is (count of \(B\)) / (grand total). \(P(A\cap B)\) is (count of both) / (grand total). \(P(A\mid B)\) is (count of both) / (count of \(B\)).

On **#7** and **#8**, write those four sentences and the formula **before** you divide.

### Circle moved, radius changed

\((x-h)^2+(y-k)^2=r^2\).

- Up \(p\) units: \(k\) becomes \(k+p\). Down \(p\): \(k\) becomes \(k-p\). Left/right changes \(h\).
- A new radius \(R\) means the right-hand side is \(R^2\), not the old \(r^2\).
- Write the new equation. Do not reuse the old radius just because the center movement was the part you noticed first.

### Factored form \(\to a+b\) or \(a+2b+3c\)

Zeros at \(r\) and \(s\) means \(f(x)=a(x-r)(x-s)\). One extra point finds \(a\). Then expand to \(ax^2+bx+c\) and evaluate the combination they asked for.

\(a+b+c=f(1)\). \(a+2b+3c\) is **not** \(f(1)\). Expand, then plug the three coefficients into that expression.

### Tangents around a circle, then a right triangle

- Two tangent segments from the **same exterior point** are congruent.
- The radius to a point of tangency is **perpendicular** to that tangent. That is a right triangle: radius, tangent segment, line from the center to the exterior point.
- A huge number is not a reason to abandon Pythagorean. Write \(r^2+t^2=d^2\) and compute.

---

## 2. Questions

**1.** (SPR) The function \(h\) is defined by \(h(x)=x^3+ax^2+bx+c\), where \(a\), \(b\), and \(c\) are constants. The zeros of \(h\) are \(-5\), \(-6\), and \(-7\). What is the value of \(c\)?

**2.** (SPR) The function \(p\) is defined by \(p(x)=x^6+ax^5+bx^4+dx^3+ex^2+fx+c\), where the letters other than \(x\) are constants. The zeros of \(p\) are \(-1\), \(-1\), \(-2\), \(-3\), \(3\), and \(1\). What is the value of \(c\)?

**3.** (SPR) The function \(h\) is defined by \(h(x)=\)<span class="circ-lead">2</span>\(x^3+ax^2+bx+c\), where \(a\), \(b\), and \(c\) are constants. The zeros of \(h\) are \(-5\), \(-6\), and \(-7\) — the same three zeros as in question 1. What is the value of \(c\)?

The leading coefficient is the circled number. It is not 1.

**4.** (SPR) In rectangle \(PQRS\), side \(\overline{PQ}\) is \(12\) units longer than side \(\overline{PS}\). The square of the length of diagonal \(\overline{PR}\) is \(4{,}304\). What is the length of the longer side of the rectangle?

**5.** (SPR) The equation \(11p(x-5)+3(x+7)=sx+214\) has infinitely many solutions, where \(p\) and \(s\) are constants. What is the value of \(3(7)-55p\)?

**6.** (SPR) The function \(f\) is defined by \(f(x)=2x^2-11x+15\). What is the value of \(x\) at which \(f\) takes its minimum value?

**7.** A grove has only spruce trees and elm trees. Each tree is tagged or not tagged. The table shows the counts.

| | Tagged | Not tagged | Total |
|---|---:|---:|---:|
| Spruce | 14 | 6 | 20 |
| Elm | 9 | 21 | 30 |
| Total | 23 | 27 | 50 |

A tree is selected at random. Let \(A\) be the event that the tree is a spruce. Let \(B\) be the event that the tree is tagged.

Write a one-sentence interpretation for each event. Then write the formula, then the probability.

- Event \(A\): <span class="blank-line"></span>
- Event \(B\): <span class="blank-line"></span>
- Event \(A\mid B\): <span class="blank-line"></span>
- Event \(A\cap B\) (the \(\cap\) symbol means “and”): <span class="blank-line"></span>
- Formula: \(P(A\mid B)=\) <span class="blank-line"></span>
- (SPR) The value of \(P(A\mid B)\): ______________

**8.** A school club has only juniors and seniors. Each member is either enrolled in calculus or not enrolled in calculus. The table shows the counts.

| | Calculus | No calculus | Total |
|---|---:|---:|---:|
| Junior | 8 | 22 | 30 |
| Senior | 18 | 12 | 30 |
| Total | 26 | 34 | 60 |

A member is selected at random. Let \(A\) be the event that the member is a senior. Let \(B\) be the event that the member is enrolled in calculus.

Write a one-sentence interpretation for each event. Then write the formula, then the probability.

- Event \(A\): <span class="blank-line"></span>
- Event \(B\): <span class="blank-line"></span>
- Event \(A\mid B\): <span class="blank-line"></span>
- Event \(A\cap B\) (the \(\cap\) symbol means “and”): <span class="blank-line"></span>
- Formula: \(P(A\mid B)=\) <span class="blank-line"></span>
- (SPR) The value of \(P(A\mid B)\): ______________

**9.** (SPR) In the \(xy\)-plane, a circle has equation \((x+4)^2+(y-1)^2=49\). The circle is translated \(6\) units down, and the radius of the resulting circle is \(3\). Write the equation of the new circle as \((x-h)^2+(y-k)^2=r^2\). What is the value of \(r^2-k\)?

**10.** (SPR) A quadratic function \(f\) has zeros at \(x=-3\) and \(x=5\), and the graph of \(y=f(x)\) passes through \((0,30)\). If \(f(x)=ax^2+bx+c\), what is the value of \(a+2b+3c\)?

**11.** (SPR) A circle with center \(C\) has radius \(1{,}365\). Four lines, each tangent to the circle, form quadrilateral \(HXYZ\). The circle lies inside the quadrilateral and is tangent to all four sides. Point \(H\) is a vertex of the quadrilateral — it is the intersection of the two tangent lines that contain sides \(\overline{HX}\) and \(\overline{HZ}\).

The perimeter of \(HXYZ\) is \(13{,}312\). Side \(\overline{XY}\) has length \(4{,}056\), side \(\overline{YZ}\) has length \(4{,}056\), and \(\overline{HX}=\overline{HZ}\).

The circle is tangent to \(\overline{HX}\) at point \(P\), and \(PX=780\).

The radius to a point of tangency is perpendicular to the tangent line. What is the distance \(CH\)?

**12.** (SPR) In the system below, \(p\) is a constant.

\[
\begin{align*}
6x+3y&=p\\
2x+y&=4
\end{align*}
\]

The system has infinitely many solutions for one value of \(p\), and it has no solution for every other value of \(p\). What is that value of \(p\) that gives infinitely many solutions?
