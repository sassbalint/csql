SHELL:=/bin/bash

all:
	@echo "choose explicit target = type 'make ' and press TAB"

S=scripts
I=in
O=out


# ===== MAIN STUFF 

FILE=brusszel

SCRIPT=$S/csql2.py
do:
	@echo "--- $@" 1>&2
	python3 $(SCRIPT) --file $I/$(FILE) --number-of-fields 4 --can-contain-noske-sep 0,1 > $O/$(FILE).txt
	@echo
	@#cat $(FILE).csv | python3 $S/deduphash.py > $(FILE).dedup.csv

