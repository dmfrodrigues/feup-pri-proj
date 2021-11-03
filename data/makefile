all: eurlex/compiled.json

eurlex/compiled.json: eurlex/filtered.json eurlex-compile.py | eurlex
	python3 eurlex-compile.py < $< > $@

eurlex/filtered.json: eurlex/with_texts.json eurlex-filter.py | eurlex
	python3 eurlex-filter.py < $< > $@

eurlex/with_texts.json: eurlex/raw.json eurlex-get-texts.py | eurlex
	python3 eurlex-get-texts.py < $< > $@

eurlex/raw.json: eurlex-get-raw.py | eurlex
	python3 eurlex-get-raw.py > eurlex/raw.json

# Directories
eurlex:
	mkdir -p eurlex

