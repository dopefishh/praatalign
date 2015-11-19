LATEX:=latex

.SECONDARY: book.fmt

all: book.pdf

%.pdf: %.dvi
	dvipdfm $<

%.fmt: preamble.tex
	$(LATEX) -ini -jobname="$(basename $@)" "&$(LATEX) $<\dump"

%.dvi: %.tex %.fmt %.bib $(IMGS)
	$(LATEX) $<
	bibtex $(basename $<)
	$(LATEX) $<
	$(LATEX) $<

clean:
	$(RM) -v $(addprefix book.,fmt aux dvi log toc out pdf bbl blg)
