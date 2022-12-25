# example: "make prepare year=2022 day=03"
prepare:
	touch ./year$(year)/inputs/$(day).txt
	touch ./year$(year)/inputs/test/$(day).txt
	mkdir ./year$(year)/days/$(day)
	cp -r ./year2022/days/00/__init__.py ./year$(year)/days/$(day)/
