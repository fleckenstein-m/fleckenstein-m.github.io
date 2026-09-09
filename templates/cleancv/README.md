# CleanCV

Unmodified `cleancv.sty` from https://github.com/giladturok/CleanCV (downloaded September 8, 2026). Distributed under the included MIT LICENSE.

The generator in `scripts/build_clean_cv.py` writes LaTeX from the shared `content/academic.md` file. It uses CleanCV's ET Book typography, centered name, small-cap headings, page geometry, icons and purple links. We customize the contact bar for the supplied contact details and display the source record's update date rather than the compilation date. No social links are invented.

Requires pdfLaTeX with ETbb, fontawesome, needspace and the packages imported by cleancv.sty. MiKTeX on this machine already provides these. `ACADEMIC_LATEX` may point to a pdflatex executable.
