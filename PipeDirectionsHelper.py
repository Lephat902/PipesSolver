import numpy as np
from Direction import Direction
from PipeType import PipeType

def xnor(a, b):
    return ((a and b) or (not a and not b))  

fourDirections = {dir for dir in Direction} 

class PipeDirectionsHelper:
    def __init__(self, pipeTypeBoard):
        self.pipeTypeBoard = pipeTypeBoard
        self.rows = len(pipeTypeBoard)
        self.columns = len(pipeTypeBoard[0])

    def get_directions_Coupling_point_to(direction):
        oppositeDirection = Direction.getOppositeDirection(direction)
        return {direction, oppositeDirection}

    def get_directions_EndCap_point_to(direction):
        return {direction}
    
    def get_directions_Elbow_point_to(direction):
        nextDirection = Direction.getNextDirection_clockwise(direction)
        return {direction, nextDirection} 
    def get_directions_Tee_point_to(direction):
        directions = fourDirections.copy()
        notPointedToDirection = Direction.getNextDirection_anticlockwise(direction)
        # remove the not pointed to direction from directions of the tee
        directions.remove(Direction(notPointedToDirection))
        
        return directions
    
    def isValidIndex(self, pipePos):
        i = pipePos[0]
        j = pipePos[1]

        return (i >= 0 and i < self.rows and j >= 0 and j < self.columns)

    # pass the position and the current direction, it will return all the directions the pipe's currently pointing to
    def get_directions_pipe_point_to(self, pipePos, direction):
        i = pipePos[0]
        j = pipePos[1]

        if not self.isValidIndex(pipePos):
            return {}

        if self.pipeTypeBoard[i][j] == PipeType.COUPLING:
            return PipeDirectionsHelper.get_directions_Coupling_point_to(direction)
        elif self.pipeTypeBoard[i][j] == PipeType.END_CAP:
            return PipeDirectionsHelper.get_directions_EndCap_point_to(direction)
        elif self.pipeTypeBoard[i][j] == PipeType.ELBOW:
            return PipeDirectionsHelper.get_directions_Elbow_point_to(direction)
        elif self.pipeTypeBoard[i][j] == PipeType.TEE:
            return PipeDirectionsHelper.get_directions_Tee_point_to(direction)

# full: build a full matrix
# if we use normal one (get directions of a pipe multiple times), there will be a bit time & space waste
class PipeDirectionsHelper_full(PipeDirectionsHelper): # inherit from PipeDirectionsHelper
    def __init__(self, pipeTypeBoard, pipeDirectionBoard):
        super().__init__(pipeTypeBoard)
        self.directions_matrix = np.zeros(shape=(self.rows, self.columns), dtype=set)
        self.buildDirectionsMatrix(pipeDirectionBoard)

    def pointTo(self, pipePos, direction):
        x = pipePos[0]
        y = pipePos[1]
        return (direction in self.directions_matrix[x][y]) 

    # match a pipe's direction and its right one
    def matchRight(self, pipePos):
        x = pipePos[0]
        y = pipePos[1]
        rightPipePos = (x, y + 1)

        # check if it's the right edge pipe
        if (y == self.columns - 1):
            if self.pointTo(pipePos, Direction.RIGHT):
                return False
            else:
                return True
        else:
            return xnor(self.pointTo(pipePos, Direction.RIGHT), self.pointTo(rightPipePos, Direction.LEFT))
    
    # match a pipe's direction and its bottom one
    def matchBottom(self, pipePos):
        x = pipePos[0]
        y = pipePos[1]
        bottomPipePos = (x + 1, y)

        # check if it's the bottom edge pipe
        if (x == self.rows - 1):
            if self.pointTo(pipePos, Direction.DOWN):
                return False
            else:
                return True
        else:
            return xnor(self.pointTo(pipePos, Direction.DOWN), self.pointTo(bottomPipePos, Direction.UP))       

    # match a pipe's direction and its left one
    def matchLeft(self, pipePos):
        x = pipePos[0]
        y = pipePos[1]
        leftPipePos = (x, y - 1)

        # check if it's the left edge pipe
        if (y == 0):
            if self.pointTo(pipePos, Direction.LEFT):
                return False
            else:
                return True
        else:
            return xnor(self.pointTo(pipePos, Direction.LEFT), self.pointTo(leftPipePos, Direction.RIGHT)) 

    # match a pipe's direction and its top one
    def matchTop(self, pipePos):
        x = pipePos[0]
        y = pipePos[1]
        topPipePos = (x - 1, y)

        # check if it's the top edge pipe
        if (x == 0):
            if self.pointTo(pipePos, Direction.UP):
                return False
            else:
                return True
        else:
            return xnor(self.pointTo(pipePos, Direction.UP), self.pointTo(topPipePos, Direction.DOWN))
    
    # Note: this method will build a full matrix 
    # the matrix of the directions pointed by each pipe in board
    def buildDirectionsMatrix(self, pipeDirectionBoard):
        for i in range(self.rows):
            for j in range(self.columns):
                self.directions_matrix[i][j] = self.get_directions_pipe_point_to((i,j), pipeDirectionBoard[i][j]) 
