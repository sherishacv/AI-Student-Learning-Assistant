# AI Student Learning Assistant — Project Report

This folder contains an Overleaf-compatible LaTeX report generated from the repository source, configuration, tests, and README. It is intentionally evidence-led: the report distinguishes implemented code from project claims and does not invent evaluation data, deployment details, or educational outcomes.

## Overleaf

1. Upload the contents of this `report/` folder to a new Overleaf project, preserving `chapters/` and `figures/`.
2. Set `main.tex` as the root document.
3. Select **XeLaTeX** (or LuaLaTeX) as the compiler. If Times New Roman is installed, the document uses it; otherwise it falls back to TeX Gyre Termes, a Times-style font.
4. Compile with BibTeX enabled for the references. The citation data is in `references.bib`.
5. Replace the bracketed identity, institution, guide, certificate, declaration, acknowledgement, and evaluation placeholders with verified information before academic submission.

The document configures 12-point body text, 1.5 line spacing, justified paragraphs, a 1.5-inch left margin and 1-inch other margins, chapter page breaks, page numbers, and chapter-numbered figures, tables, and equations.

## Report structure

- `main.tex`: layout, front matter, chapter order, bibliography, and appendices.
- `chapters/`: twelve report chapters and four appendices.
- `figures/`: TikZ source for the architecture and query-workflow diagrams.
- `references.bib`: cited academic paper and official technology documentation.

## Evidence and validation limits

The repository contains one test module with two smoke-level tests; the workspace used to prepare this report did not have `pytest` installed. No LaTeX engine (`pdflatex`, `latexmk`, `xelatex`, or `lualatex`) was available, so no PDF was built here. Compile the project in Overleaf and run the test suite in a properly provisioned environment before treating either as verified.

No measured retrieval, answer-quality, latency, throughput, usability, or learning-outcome results were present. The results chapter therefore reports source-level evidence only, while Appendix C provides a blank template for future measurements.
