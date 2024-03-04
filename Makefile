SHELL:=/bin/bash

all:
	@echo "choose explicit target = type 'make ' and press TAB"

S=scripts
I=in
O=out


# ===== MAIN STUFF 

FILE=brusszel
FUNC=orig
NOF=4
#NOF=10 # for `_dep` files
CCNS=0,1

SCRIPT=$S/csql.py
do:
	@echo "--- $@" 1>&2
	python3 $(SCRIPT) --file $I/$(FILE) --func $(FUNC) --number-of-fields $(NOF) --can-contain-noske-sep $(CCNS) > $O/$(FILE).$(FUNC).txt
	@echo
	@#cat $(FILE).csv | python3 $S/deduphash.py > $(FILE).dedup.csv

