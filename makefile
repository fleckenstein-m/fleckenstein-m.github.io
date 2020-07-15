compile:
	pandoc index.md -s -c style.css --toc -o index.html
	pandoc index.md LaTexFormat.yaml --filter deflists.py --pdf-engine=pdflatex -o index.pdf 
