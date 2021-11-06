.DELETE_ON_ERROR:

all: eurlex/combined.csv

eurlex/combined.csv: eurlex/filtered.csv eurlex/texts.txt eurlex-combine.py
	python3 eurlex-combine.py eurlex/filtered.csv eurlex/texts.txt > $@

eurlex/texts.txt: eurlex/filtered.csv eurlex-get-texts.py | eurlex/texts
	python3 eurlex-get-texts.py < $< > $@

eurlex/filtered.csv: eurlex/processed.csv eurlex-filter.py
	python3 eurlex-filter.py < $< > $@

eurlex/processed.csv: eurlex/raw.json eurlex-process.py
	python3 eurlex-process.py < $< > $@

eurlex/raw.json: eurlex-get-raw.py | eurlex
	python3 eurlex-get-raw.py > eurlex/raw.json

# Directories
eurlex:
	mkdir -p $@

eurlex/texts: | eurlex
	mkdir -p $@
