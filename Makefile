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
	python3 $(SCRIPT) --file $I/$(FILE) > $O/$(FILE).txt
	@echo
	@#cat $(FILE).csv | python3 $S/deduphash.py > $(FILE).dedup.csv

