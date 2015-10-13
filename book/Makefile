IMGS:=$(basename $(shell ls img/*.xz))
LATEX:=latex

.SECONDARY: book.fmt $(IMGS)

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

%.eps: %.eps.xz
	xz -kd $<

clean:
	$(RM) -v $(addprefix book.,fmt aux dvi log toc out pdf bbl blg) $(IMGS)
