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

The puzzle on this particular [website](https://www.puzzle-pipes.com/) has 4 types of pipes and we will concentrate on solving the puzzles based on the input from the page only:
- End pipe
- Line pipe
- T pipe
- Elbow pipe
  
# Files in this project
- [PipeType.py](./PipeType.py) : 
