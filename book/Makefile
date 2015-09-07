SHELL:=/bin/bash
VERSION:=1.5
IMGS:=$(basename $(shell ls img/*.xz))
LATEX:=latex

.SECONDARY: book.fmt $(IMGS)

all: book.pdf

%.pdf: %.dvi
	dvipdfm $<

%.fmt: preamble.tex
	$(LATEX) -ini -jobname="$(basename $@)" "&$(LATEX) $<\dump"

%.dvi: %.tex %.fmt $(IMGS)
	$(LATEX) $<
	$(LATEX) $<

%.eps: %.eps.xz
	xz -kd $<

clean:
	$(RM) -v book.{fmt,aux,dvi,log,toc,out,pdf} $(IMGS)