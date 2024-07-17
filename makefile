compile:
	pandoc index.md -s -c style.css --toc --lua-filter=links-to-blank.lua -o index.html
	pandoc index.md LaTexFormat.yaml --filter deflists.py --pdf-engine=pdflatex -o index.pdf 
