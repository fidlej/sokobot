# Sokobot Usage #
Checkout the sources:
```
hg clone https://sokobot.googlecode.com/hg/ sokobot
cd sokobot
```

Solve a puzzle:
```
./view.sh data/sokoban/sokoban2.txt
```

Use a different solver (`-s`):
```
./view.sh data/sokoban/sokoban2.txt -s ida
```

It is also possible to solve a few different puzzles.
For example, the [15-puzzle](http://en.wikipedia.org/wiki/Fifteen_puzzle):
```
./view.sh data/npuzzle/15puzzle1.txt
```

# Available Solvers #
  * **astar** - [A\* algorithm](http://theory.stanford.edu/~amitp/GameProgramming/). This is the default solver.
  * **ida** - [Iterative Deepening A\*](http://www.cs.ualberta.ca/~jonathan/Grad/junghanns.phd.ps.gz).
  * **relaxida** - IDA`*` with heuristics from a [hierarchy of subproblems](http://games.cs.ualberta.ca/~holte/Publications/sara2005.pdf).
  * **relaxastar** - A`*` with the heuristics from a hierarchy of subproblems. The subproblems are still solved by IDA`*`.
  * **pgida** and **pgastar** - IDA`*` and A`*` with an overestimating heuristic. The heuristic is based on the length of a suboptimal plan extracted from a [planning graph](http://sod90.asu.edu/pgSurvey.pdf). Currently only the Sokoban actions are described enough to be usable for the planning graph.

These solvers search for a path to the goal.
They expand the states based on **g** + **h**,
where **g** is the distance from the start
and **h** is the estimated distance to the goal.
They find the shortest path if **h** is not overestimated.

## Solver Options ##
It is possible to use some additional options with the solvers.
For example, a weighted A`*` solver is: `-s `**astar,hweight=1.2**

Options:
  * **hweight=**number - A number greater than 1 gives a bigger weight to **h**. So the states with low **h** are expanded more greedily. The solver will expand the states based on **g** + hweight`*`**h**. On the other hand, zero hweight results in a breadth-first search.
  * **one\_way=True** - An option for an IDA`*` solver. It explores just a single way to a state, even if it isn't the optimal one.
  * **greedy\_on\_exact=True** - An option for a relaxed solver. It quits a subproblem search when it stumbles on a solution path there. It does not care about the length of the total path.

These extra options are not used by default because they do not guarantee to find the shortest path. They are satisfied with any path.

# Statistics #
The different solvers produce different [numbers of visited states](http://sokobot.googlecode.com/svn/export/html/stats_num_visited.html).