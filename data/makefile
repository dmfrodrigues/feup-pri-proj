.DELETE_ON_ERROR:

all: eurlex/with_texts.csv

# eurlex/compiled.json: eurlex/with_texts.json eurlex-compile.py | eurlex
# 	python3 eurlex-compile.py < $< > $@

eurlex/with_texts.csv: eurlex/filtered.csv eurlex-get-texts.py | eurlex eurlex/texts
	python3 eurlex-get-texts.py < $< > $@

eurlex/filtered.csv: eurlex/processed.csv eurlex-filter.py | eurlex
	python3 eurlex-filter.py < $< > $@

eurlex/processed.csv: eurlex/raw.json eurlex-process.py | eurlex
	python3 eurlex-process.py < $< > $@

eurlex/raw.json: eurlex-get-raw.py | eurlex
	python3 eurlex-get-raw.py > eurlex/raw.json

# Directories
eurlex:
	mkdir -p $@

eurlex/texts: | eurlex
	mkdir -p $@
