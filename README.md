# Matt's Markdown/LaTeX/PDF CV/Website

The main CV file is the markdown file `index.md`.
The `makefile` compiles the CV into a LaTeX .pdf and an HTML via pandoc.

For the HTML conversion I use a CSS stylesheet (`style.css`) which:
+ Gives a custom background and div settings for the content area.
+ Creates a "table of contents" from the section headings and converts that into a menu bar where the subsections drop down.
+ Hides some longer content away to reappear on mouseover.

For the LaTeX/pdf conversion, I use a pandoc filter `deflists.py` that filters out the Abstract of the papers.
In addition, formatting is done in the YAML file `LaTexFormat.yaml`

## Use
Make changes to the markdown file `index.md`. 
Run `make` and it will produce a .pdf and .html.
