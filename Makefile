all:
	pdflatex test.tex 
	convert -density 300 test.pdf -quality 95 test.png
	rm -f test.aux  test.log test.pdf
