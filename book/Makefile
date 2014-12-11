SHELL:=/bin/bash

all:
	latex -shell-escape book.tex
	latex -shell-escape book.tex
	latex -shell-escape book.tex
	dvipdfm book.dvi

clean:
	rm -vf *.{aux,dvi,log,toc,out}

clobber: clean
	rm -vf *.pdf
