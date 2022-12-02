# example: "make prepare day=03"
prepare:
	touch ./inputs/$(day).txt
	touch ./inputs/test/$(day).txt
	cp -r ./days/00 ./days/$(day)
