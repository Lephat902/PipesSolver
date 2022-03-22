# AI Introduction Course: Search Algorithms

1st Assignment for AI Introduction course at HCMUT university. In this project we use Search Algorithm such as BFS (blind search) and heuristic search algorithm called A* to solve [pipes puzzle](https://www.puzzle-pipes.com/). The simulation process is implemented in [BoardPrinter.py](./BoardPrinter.py) by printing text in the terminals (Which can be improved by using other GUI Frameworks)

# Technologies
> Python 3
# A thing about [this puzzle](https://www.puzzle-pipes.com/)

Pipes also known as FreeNet, or NetWalker is played on
a grid filled with pipes of many types; each tile (square) of the grid can be rotated and the aim of the game is to connect all the pipes WITHOUT forming loops and disconnected pipes. 
<br>
<br>
**Puzzle examples:** <br>
<div align="center">
  <img alt="puzzle-examples" src="https://user-images.githubusercontent.com/49335345/158781136-455155ca-c3e8-4ad2-91f6-70b3147e6817.png" width="300px" height="300px">
</div>
 <br>
There is a loop in the puzzle and some unconnected pipes <br>
<div align="center">
<img src="https://user-images.githubusercontent.com/49335345/158779185-59562582-c434-4d07-89aa-87f9e9b815be.png" width="300px" height="300px">
</div>

**Win state:** <br>
<div align="center">
 <img src="https://user-images.githubusercontent.com/49335345/158780784-c21c3aa0-267d-45ec-b20d-7ed1837719f4.png" width="300px" height="300px">
 </div>

The puzzle on this particular [website](https://www.puzzle-pipes.com/) has 4 [types of pipes](types) and we will concentrate on solving the puzzles based on the input from the page only:
- End pipe    <img src="https://user-images.githubusercontent.com/49335345/158784228-9d52b3c7-4b14-43b6-b122-d56f0805007d.png" width="15px" height="15px">
- Line pipe  <img src="https://user-images.githubusercontent.com/49335345/158784779-e7d550e3-d9c0-419f-af91-bbd34eaf6363.png" width="15px" height="15px">
- T pipe <img src="https://user-images.githubusercontent.com/49335345/158784912-764c73d2-d9dd-4c49-b2d0-89dc1fcc6a71.png" width="15px" height="15px">
- Elbow pipe <img src="https://user-images.githubusercontent.com/49335345/158785040-c731d6ae-0d29-47ca-b8d9-3f6d77eaf2b2.png" width="15px" height="15px">

  
# Files in this project
- [PipeType.py](./PipeType.py) : define 4 [types](types) of pipes
- [Direction.py](./Direction.py) : define the direction of each pipe can have
- [CheckWin.py](./CheckWin.py) : modules to check if we have solved the puzzles while searching by checking all connected pipes without loops
- [PipeDirectionsHelper.py](./PipeDirectionsHelper.py) : define the direction that the pipe is pointing to and check if the surrouding pipes match
- [BFSPipeSolver.py](./BFSPipeSolver.py): Implement BFS to solve the puzzle
- [aStarPipeSolver.py](./aStarPipeSolver.py): Implement A* to solve the puzzle
- [BoardPrinter.py](./BoardPrinter.py): Used to print the game boards.

# Things that can be improved
- More interactive, user-friendly UI
- Convert real image input to "usable" input that can be used in code