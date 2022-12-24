# example: "make prepare day=03"
prepare:
	touch ./2019/inputs/$(day).txt
	touch ./2019/inputs/test/$(day).txt
	mkdir ./2019/days/$(day)
	cp -r ./2022/days/00/__init__.py ./2019/days/$(day)/
