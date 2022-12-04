# Advent of code 2022

## About
OK, here we go again!

https://adventofcode.com/2022

## Quickstart
```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
python aoc.py --day "01"
```

## Convenience tools
### Create the base files for a new day
```
make prepare day=03
```
### Run a solution for the test input
```
. ./venv/bin/activate
python aoc.py --day "01" --test
```

### Tricks I learnt
#### Iterate through chunks
```
l = [1, 2, 3, 4, 5, 6]
for a, b, c in zip(*(iter(l),) * 3):
    print(a, b, c)
```
```
1 2 3
4 5 6
```
#### Pandas intervals
```
from pandas import Interval
a = Interval(1, 4, closed="both")
b = Interval(2, 3, closed="both")
print(a in b)
print(b in a)
print(a.overlaps(b))
```
