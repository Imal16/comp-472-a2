# comp-472-a2
 Artificial Intelligence Assignment 2: N-Puzzle

The goal of this assignment is to implement & analyze several search algorithms, notably Uniform Cost Search, Greedy Best First Search and A*.

The program attempts to run these algorithms to find solutions to a custom N-puzzle.

Our N-puzzles adds the following rules:
- If the 0 tile is in a corner, it can switch with the tile at the opposite side in a "wrap around" move (vertical wrap-around can only occur if there are more than 2 rows)
- If the 0 tile is in a corner, it can move diagonally with the tile in its immediate diagonal or the tile on the opposite corner


## Heuristics

We chose the following:
- Sum of Permutation Inversions
- Manhattan Distance

## Execution

Call main.py from the command line or using your preferred text editor / IDE.

## Dependencies

- Numpy

## Arguments
```
-f or --file : Name of the puzzle file. Defaults to samplePuzzles.txt.

-t or --timeout : Number of seconds before the search functions are timed out. Defaults to 60 seconds.

-r or --rows : Number of rows each puzzle has. Defaults to 2.

-c or --columns : Number of columns each puzzle has. Defaults to 4.

-o or --output : Specifies which directory to write files to. Defaults to "output".
```

Github URL: https://github.com/OliRac/comp-472-a2 <br />

