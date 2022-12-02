# example: "make prepare day=03"
prepare:
	touch ./inputs/$(day).txt
	touch ./inputs/test/$(day).txt
	mkdir ./days/$(day)
	cp -r ./days/00/__init__.py ./days/$(day)/
