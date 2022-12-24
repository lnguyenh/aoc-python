# example: "make prepare year=2022 day=03"
prepare:
	touch ./$(year)/inputs/$(day).txt
	touch ./$(year)/inputs/test/$(day).txt
	mkdir ./$(year)/days/$(day)
	cp -r ./2022/days/00/__init__.py ./$(year)/days/$(day)/
