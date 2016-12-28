DOC:=book
LATEX:=latex
BIBTEX:=bibtex
LATEXFLAGS:=-file-line-error -halt-on-error -no-shell-escape

TEXS:=$(wildcard *.tex)

.PHONY: all
.SECONDARY: $(DOC).fmt

all: $(DOC).pdf

%.fmt: preamble.tex
	$(LATEX) $(LATEXFLAGS) -ini -jobname="$(basename $@)" "&$(LATEX) $<\dump"

%.pdf: %.dvi
	dvipdfm $<

%.dvi: %.tex %.fmt %.bib $(TEXS)
	$(LATEX) $(LATEXFLAGS) $<
	grep -q '^\\bibdata{' $(basename $<).aux && $(BIBTEX) $(basename $<) || true
	$(LATEX) $(LATEXFLAGS) $< | tee $(basename $<).mlog
	grep -iqF 'rerun' $(basename $<).mlog &&\
		$(LATEX) $(LATEXFLAGS) $< || true

clean:
	$(RM) $(addprefix $(DOC).,aux log fmt toc bbl blg mlog run.xml out pdf)
