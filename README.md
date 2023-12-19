# Advent of code in Python

## About
OK, here we go again! 

After using AOC to learn Node.js and Go in 2020 and 2021, I decided to be a bit lazy and use Python :). I built a few helpers in 2022 and I am looking forward to using them this year!

https://adventofcode.com

## Quickstart
```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
python aoc.py --day 01 --year 2022 
```

## Convenience tools
### Running the aoc solutions
```
# run today's solution
python aoc.py  

# run today's solution against the test input
python aoc.py --test 

# run a specific day for a specific year
python aoc.py --day 17 --year 2022

# run day 01 against the test input
python aoc.py --day 01 --test  

# run day 05 against the file toto.txt contained in the test input folder
python aoc.py --day 05 --test --filename toto.txt 
```
### Create the base files for a new day and a specific year
```
make prepare day=03 year=2023
```

## Classic themes
### Repeating pattern with loop allowing to skip a lot of computing
- 2023 Day 14

### Djikstra
- 2023 Day 17

### Intervals
- 2023 Day 5

### LCM Lowest common multiple
- 2023 Day 8

## Tricks I learnt in 2023
### Quadratic formula
https://en.wikipedia.org/wiki/Quadratic_formula

It can be an easy way to solve an equation like ax2 + bx + c = 0, instead of doing a binary search like I did for day 6.

### Ray casting
Day 10. With a loop or polygon, one can use ray casting to know if a point is inside or outside a polygon. I did not use that method myself. 
But if you do, some adjustments had to be made for "edges" and straight lines that our ray might touch.
See https://en.wikipedia.org/wiki/Point_in_polygon

### LRU cache
Day 12. For huge tree traversal to count gazillions possibilities, lru_cache helped speed up dramatically the output. From 100+ days to 500ms...

### BFS traversal
Day 12. For the first time in aoc, explicitely made a dynamic BFS traversal, when all edges are not known and we generate them on the fly. See the utils. Still a wip, could possibly be made more general sometime.

### Shoelace theorem
Day 18. Can be useful to calculate the inside of a polygon. Henrik googled "Polygon area". https://www.themathdoctors.org/polygon-coordinates-and-areas/ https://www.reddit.com/r/adventofcode/comments/18l2nk2/2023_day_18_easiest_way_to_solve_both_parts/.
Pick's theorem. Gotcha as we dont have a pure line in this problem.

### Shapely library
Day 18. Can be used to easily calculate area of polygon and other things with coordinates.
https://shapely.readthedocs.io/en/stable/manual.html


## Tricks I learnt in 2022
### Iterate through chunks
```
l = [1, 2, 3, 4, 5, 6]
for a, b, c in zip(*(iter(l),) * 3):
    print(a, b, c)
```
```
1 2 3
4 5 6
```
### Pandas intervals
```
from pandas import Interval
a = Interval(1, 4, closed="both")
b = Interval(2, 3, closed="both")
print(a in b)
print(b in a)
print(a.overlaps(b))
```
### Reversed
```
for x in reversed(range(6)):
    print(x)
    
5
4
3
2
1
0
```
### Matplotlib
- See day 14 for animation
- https://github.com/tomsembl/AdventOfCode/blob/main/2022/14.3.py could be a source of inspiration too or https://www.reddit.com/r/adventofcode/comments/zlmwb4/2022_day_14_how_does_everyone_do_visualisations/
- See day 24 for frame by frame animation
- cmap colormaps https://matplotlib.org/stable/tutorials/colors/colormaps.html
- maybe useful in the future. 3d visualization https://aoc.just2good.co.uk/2022/18 https://www.reddit.com/r/adventofcode/comments/zwkl1f/2022_day_18python_simple_visualisation_of_the/

### Numpy for dummies
```
grid = np.zeros((10, 5))  # 10 on the y-axis, 5 on the x-axis
x = 4
y = 9
grid[y][x] = 7
print(grid)
```

### Caching results for repetitive calls with same arguments
```
import functools
    ...
    
    @functools.cache
    def find_best_path(self, robots, resources, i):
      return ....
```

### Tree pruning
Day 19 is an example of DFS with playing with conditions to reduce the possibility space.

### Deque rotation
```
from collections import deque

a = deque([1, 2, 3, 4, 5, 6, 7, 8, 9])
>> deque([1, 2, 3, 4, 5, 6, 7, 8, 9])

a.rotate(3)
>> deque([7, 8, 9, 1, 2, 3, 4, 5, 6])

a.rotate(-3)
>> deque([1, 2, 3, 4, 5, 6, 7, 8, 9])
```

### Sympy equation solving
```
from sympy import solve, symbols
x = symbols('x')
solve("x*4-2")

>> [1/2]
```

### Maybe worth looking at some day
- Interval tree concept: https://en.wikipedia.org/wiki/Interval_tree
- Graph words/things/links for inspiration if stuck some day, or to make some libraries from:
  - Depth first algorithm (visits all nodes in a graph once) DFS. Maybe https://github.com/Andrew-Foote/aoc/blob/master/solutions/python/lib/graph.py for inspiration
  - Breadth first algorithm BFS
  - DEAP: https://deap.readthedocs.io/en/master/ some kind of crazy algorithm library (seems to have a learning curve to be able to use it)
  - Reward driven research papers and stack overflow discussion: https://stackoverflow.com/questions/48152370/reasonably-efficient-algorithm-for-reward-driven-graph-traversal
- Categorization of aoc problems over the years https://www.reddit.com/r/adventofcode/comments/z0vmy0/350_stars_a_categorization_and_megaguide/
- Algorithm book: https://www.algorist.com/
- Qalc: command line calculator https://qalculate.github.io/manual/qalc.html
- "parse" python library as a layer above regexp https://github.com/r1chardj0n3s/parse 

  
### Ideas when stuck :)
- Binary search. Conditions: results can be sorted, and integers, and we have an easy "test function". See 2019 day 14 part 2