all: synonyms.txt

synonyms.txt: WNprolog-3.0/prolog/wn_s.pl Syns2Syms.class
	java Syns2Syms WNprolog-3.0/prolog/wn_s.pl synonyms.txt

WNprolog-3.0/prolog/wn_s.pl:
	curl -L http://wordnetcode.princeton.edu/3.0/WNprolog-3.0.tar.gz --output WNprolog-3.0.tar.gz
	tar -xf WNprolog-3.0.tar.gz --one-top-level=WNprolog-3.0

%.class: %.java
	javac $<
