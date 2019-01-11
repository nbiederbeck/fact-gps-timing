all:

examples: $(addprefix build/, $(addsuffix .pdf, histogram))

build:
	mkdir -p $@

build/histogram.pdf: examples/histogram.py | build
	python $<

.PHONY: all examples
