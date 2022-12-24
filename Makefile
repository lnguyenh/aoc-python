# example: "make prepare year=2022 day=03"
prepare:
	touch ./$(year)/inputs/$(day).txt
	touch ./$(year)/inputs/test/$(day).txt
	mkdir ./$(year)/days/$(day)
	cp -r ./$(year)/days/00/__init__.py ./2019/days/$(day)/
