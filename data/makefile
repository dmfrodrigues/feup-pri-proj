.DELETE_ON_ERROR:

all: ../solr/data/combined.csv

../solr/data/combined.csv: eurlex/combined.csv
	cp $< $@

eurlex/combined.csv: eurlex/filtered.csv eurlex/ranked.csv eurlex-combine.py
	python3 eurlex-combine.py eurlex/filtered.csv eurlex/ranked.csv > $@

eurlex/ranked.csv: eurlex/texts.txt eurlex/filtered.csv eurlex-pagerank.py
	python3 eurlex-pagerank.py eurlex/texts.txt eurlex/filtered.csv > $@

eurlex/texts.txt: eurlex/filtered.csv eurlex-get-texts.py | eurlex/texts eurlex/notexts
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

eurlex/notexts: | eurlex
	mkdir -p $@
