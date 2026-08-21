# Printable SAT Math desk packet

Math notes and exam-style questions only — no Saturday 2:00–2:30 lesson clock.

**Print the full desk packet:** [`SAT-MATH-DESK-PACKET.pdf`](SAT-MATH-DESK-PACKET.pdf)

**Print the current gap set (25 items):** [`TARGETED-SET-01.pdf`](TARGETED-SET-01.pdf) — notes + questions for Karina; last page is the key.

| File | Use |
|---|---|
| `SAT-MATH-DESK-PACKET.md` | Source (edit this) |
| `SAT-MATH-DESK-PACKET.html` | Browser reprint |
| `SAT-MATH-DESK-PACKET.pdf` | Desk printout |
| `build_packet.py` | Rebuild HTML + rendered math |

Equations are rendered with KaTeX before the PDF is made, so they should print as real math, not raw `\( ... \)` code.

Answer keys are the last section. Skip those pages if Karina should not see solutions during a set.

Rebuild:

```bash
python3 sat-prep/print/build_packet.py
python3 sat-prep/print/build_packet.py TARGETED-SET-01.md
# then print HTML to PDF, or:
timeout 45 google-chrome --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
  --user-data-dir=/tmp/chrome-sat-pdf \
  --print-to-pdf=sat-prep/print/TARGETED-SET-01.pdf \
  file://$PWD/sat-prep/print/TARGETED-SET-01.html
```
