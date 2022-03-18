import numpy as np
from Direction import Direction
from PipeDirectionsHelper import PipeDirectionsHelper_full 

# we only check win when there's no pipe mismatch in the board
# otherwise it will behave unexpectedly
class CheckWin:
    def __init__(self, pipeTypeBoard):
        self.pipeTypeBoard = pipeTypeBoard
        self.rows = len(pipeTypeBoard)
        self.columns = len(pipeTypeBoard[0])

    # get all the connected pipes around a pipe at pipePos
    # we just use pointTo() because the pipe match is already checked before in checkWin()
    def getAdjacentConnectedPipePos(self, pipePos):
        x = pipePos[0]
        y = pipePos[1]

        adjacentPipePos = []
        if (self.pipeDirectionsHelper_full.pointTo(pipePos, Direction.RIGHT)):
            adjacentPipePos.append((x, y + 1))
        if (self.pipeDirectionsHelper_full.pointTo(pipePos, Direction.UP)):
            adjacentPipePos.append((x - 1, y))
        if (self.pipeDirectionsHelper_full.pointTo(pipePos, Direction.LEFT)):
            adjacentPipePos.append((x, y - 1))
        if (self.pipeDirectionsHelper_full.pointTo(pipePos, Direction.DOWN)):
            adjacentPipePos.append((x + 1, y))
        
        return adjacentPipePos

    def checkLoop(self, current, visited, parent):
        currentX = current[0]
        currentY = current[1]
        visited[currentX][currentY] = True

        adjacentPipePos = self.getAdjacentConnectedPipePos(current)

        for pipePos in adjacentPipePos:
            x = pipePos[0]
            y = pipePos[1]

            if (visited[x][y] == False):
                if self.checkLoop(pipePos, visited, current):
                    return True
            elif (pipePos != parent):
                return True
        
        return False

    def assert_NoLoop_And_SingleGroup(self):
        visited = np.full((self.rows, self.columns), False, np.bool_)

        if (self.checkLoop((0, 0), visited, (-1, -1))):
            return False # there's loop
        if (False in visited):
            return False # pipes don't form a single group
        
        return True

    def checkWin(self, pipeDirectionBoard):
        self.pipeDirectionsHelper_full = PipeDirectionsHelper_full(self.pipeTypeBoard, pipeDirectionBoard)
       
        noLoop_And_SingleGroup = self.assert_NoLoop_And_SingleGroup()
        self.pipeDirectionsHelper_full = None # deallocate pipeDirectionsHelper
        if (noLoop_And_SingleGroup):
            return True
        else:
            return False
