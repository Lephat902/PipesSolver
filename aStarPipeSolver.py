import numpy as np
from queue import PriorityQueue
from PipeType import PipeType
from Direction import Direction
from BoardPrinter import BoardPrinter
from CheckWin import CheckWin
from PipeDirectionsHelper import *
import time # used to measure elapsed time
import psutil # used to measure memory usage

def xnor(a, b):
    return ((a and b) or (not a and not b))

def printMemoryUsage():
    # print memory usage
    memoryUsage = psutil.Process().memory_info().rss / (1024 * 1024)
    print("The memory usage is: {0} (MB)".format(memoryUsage))

def convertToPipeTypeBoard(pipeTypeNumber):
    rows = len(pipeTypeNumber)
    columns = len(pipeTypeNumber[0])
    pipeTypeBoard = np.zeros((rows, columns), PipeType)

    for i in range(rows):
        for j in range(columns):
            pipeTypeBoard[i][j] = PipeType(pipeTypeNumber[i][j])

    return pipeTypeBoard

def convertToPipeDirectionBoard(pipeDirectionNumber, pipeTypeBoard):
    rows = len(pipeDirectionNumber)
    columns = len(pipeDirectionNumber[0])
    pipeDirectionBoard = np.zeros((rows, columns), Direction)

    for i in range(rows):
        for j in range(columns):
            pipeDirectionBoard[i][j] = Direction(pipeDirectionNumber[i][j])
            # adjust the direction if user input for coupling is wrong
            if (pipeTypeBoard[i][j] == PipeType.COUPLING):
                if (pipeDirectionBoard[i][j] == Direction.LEFT):
                    pipeDirectionBoard[i][j] = Direction.RIGHT
                elif (pipeDirectionBoard[i][j] == Direction.DOWN):
                    pipeDirectionBoard[i][j] = Direction.UP  

    return pipeDirectionBoard 

class pqItem:
    def __init__(self, directionBoard, pipePos, movesList, hValue):
        self.directionBoard = directionBoard
        self.pipePos = pipePos
        self.movesList = movesList
        self.hValue = hValue

    def __lt__(self, other):
        if self.hValue == other.hValue:
            return len(self.movesList) > len(other.movesList) # prioritize longer movesList
        else:
            return self.hValue < other.hValue
    
    def getDirectionBoard(self):
        return self.directionBoard
    def getPipePos(self):
        return self.pipePos
    def getMovesList(self):
        return self.movesList
    def getHValue(self):
        return self.hValue

class PipeSolver:
    def __init__(self, pipeTypeBoard, pipeDirectionBoard):
        self.pipeTypeBoard = pipeTypeBoard
        self.pipeDirectionBoard = pipeDirectionBoard
        self.rows = len(pipeTypeBoard)
        self.columns = len(pipeTypeBoard[0])
        self.checkWin_obj = CheckWin(pipeTypeBoard)
        self.pipeDirectionsHelper = PipeDirectionsHelper(pipeTypeBoard)
    
    # check top and left pipe
    def isValidMove(self, currentDirectionBoard, pipePos, operation):
        x = pipePos[0]
        y = pipePos[1]
        directions_current = self.pipeDirectionsHelper.get_directions_pipe_point_to(pipePos, operation)
        directions_top = self.pipeDirectionsHelper.get_directions_pipe_point_to((x - 1, y), currentDirectionBoard[x - 1][y])
        directions_left = self.pipeDirectionsHelper.get_directions_pipe_point_to((x, y - 1), currentDirectionBoard[x][y - 1])

        matchLeft = xnor((Direction.LEFT in directions_current), (Direction.RIGHT in directions_left))
        matchTop = xnor((Direction.UP in directions_current), (Direction.DOWN in directions_top))

        return (matchLeft and matchTop)
        
    # next Pos to execute in A*
    def getNextPos(self, pipePos):
        x = pipePos[0]
        y = pipePos[1]

        if (x == self.rows - 1 and y == self.columns - 1):
            return (-1, -1)
        elif (y == self.columns - 1):
            return (x + 1, 0)
        else:
            return (x, y + 1)

    def getAllPossibleOperations(self, pipePos):
        i = pipePos[0]
        j = pipePos[1]
        if (self.pipeTypeBoard[i][j] == PipeType.COUPLING):
            otherOperations = [Direction.UP, Direction.RIGHT]
            return otherOperations
        else:
            otherOperations = [opt for opt in Direction]
            return otherOperations

    # we call this method once for the first state
    def getNumOfPipeMismatches_init(self, directionBoard):
        counter = 0
        pipeDirectionsHelper_full = PipeDirectionsHelper_full(self.pipeTypeBoard, directionBoard)

        # each pipe checks the right and bottom pipe of its
        for i in range(self.rows):
            for j in range(self.columns):
                currentPipePos = (i,j)
                matchRight = pipeDirectionsHelper_full.matchRight(currentPipePos)
                matchBottom = pipeDirectionsHelper_full.matchBottom(currentPipePos)
                if not matchRight:
                    counter += 1
                if not matchBottom:
                    counter += 1
                
                if (i == 0): # if it's at the top edge
                    matchTop = pipeDirectionsHelper_full.matchTop(currentPipePos)
                    if not matchTop:
                        counter += 1
                if (j == 0): # if it's at the left edge
                    matchLeft = pipeDirectionsHelper_full.matchLeft(currentPipePos)
                    if not matchLeft:
                        counter += 1

        return counter

    def isValidIndex(self, pipePos):
        x = pipePos[0]
        y = pipePos[1]
        return (x >= 0 and x < self.rows and y >= 0 and y < self.columns)

    # those below list is utilities for getNumOfPipeMismatchesAt()
    adjPos_X = [0,-1,0,1]
    adjPos_Y = [1,0,-1,0]
    fourDirections = [dir for dir in Direction]

    def getNumOfPipeMismatchesAt(self, directionBoard, pipePos):
        x = pipePos[0]
        y = pipePos[1]
        
        numOfMismatches = 0

        directions_current = self.pipeDirectionsHelper.get_directions_pipe_point_to(pipePos, directionBoard[x][y])
        for direction, plusX, plusY in zip(self.fourDirections, self.adjPos_X, self.adjPos_Y):
            adjX = x + plusX
            adjY = y + plusY

            directions_adj = {}
            if (self.isValidIndex((adjX, adjY))):
                directions_adj = self.pipeDirectionsHelper.get_directions_pipe_point_to((adjX, adjY), directionBoard[adjX][adjY])
            oppositeDirection = Direction.getOppositeDirection(direction)
            match = xnor(direction in directions_current, oppositeDirection in directions_adj)
            if not match:
                numOfMismatches += 1

        return numOfMismatches

    # cal hValue for new state (not the initial state)
    def calHValue(self, currentDirectionBoard, newDirectionBoard, pipePos, currentHValue):
        numOfMismatches_current = self.getNumOfPipeMismatchesAt(currentDirectionBoard, pipePos)
        numOfMismatches_new = self.getNumOfPipeMismatchesAt(newDirectionBoard, pipePos)
        # newH = currentH + numOfPipeMismatches difference of 2 states when change direction of a pipe
        return (currentHValue + (numOfMismatches_new - numOfMismatches_current))

    def aStar(self):
        start_time = time.time() # get the start time
        openList = PriorityQueue()
        # In this game, we only rotate at most (rows x columns) pipes
        # so we don't consider the depth of the tree then there's no gValue or gValue = 0 for all states
        #
        # hValue is calculated as number of pipeMismatches (E.g. pipeA points to pipeB
        # but pipeB doesn't do the same)
        # priority queue will take the state has the lowest hValue
        hValueOfFirstItem = self.getNumOfPipeMismatches_init(self.pipeDirectionBoard) # hValue
        firstItem = pqItem(self.pipeDirectionBoard, (0,0), [], hValueOfFirstItem)
        openList.put(firstItem)
        counter = 0 # count for the times popping the queue

        while not openList.empty():
            counter += 1
            current = openList.get()
            currentDirectionBoard = current.getDirectionBoard()
            currentPos = current.getPipePos()
            currentMovesList = current.getMovesList()
            currentHValue = current.getHValue()
            
            # we only check win when there's no mismatch pipes
            if (currentHValue == 0 and self.checkWin_obj.checkWin(currentDirectionBoard)):
                end_time = time.time()
                elapsedTime = end_time - start_time
                self.boardPrinter = BoardPrinter(self.pipeTypeBoard, self.pipeDirectionBoard)
                self.boardPrinter.printBoard(currentMovesList)
                print("Total time taken by A* Algorithm: {0} second(s)".format(elapsedTime))
                print("Number of times popping queue: {0} times".format(counter))
                return

            if (currentPos != (-1, -1)):
                currentX = currentPos[0]
                currentY = currentPos[1]
                possibleOperations = self.getAllPossibleOperations(currentPos)
    
                for operation in possibleOperations:
                    if self.isValidMove(currentDirectionBoard, currentPos, operation):
                        newDirectionBoard = currentDirectionBoard.copy()
                        newPos = self.getNextPos(currentPos)
                        newMovesList = currentMovesList.copy()
                        newHValue = currentHValue
                        
                        # if there's any change in board then we update those values
                        if (currentDirectionBoard[currentX][currentY] != operation):
                            newDirectionBoard[currentX][currentY] = operation
                            newMovesList.append((currentPos, operation))
                            newHValue = self.calHValue(currentDirectionBoard, newDirectionBoard, currentPos, currentHValue)   

                        newItem = pqItem(newDirectionBoard, newPos, newMovesList, newHValue)                   
                        openList.put(newItem)
        end_time = time.time()
        elapsedTime = end_time - start_time
        print("Cannot find a solution")
        print("Total time taken by A* Algorithm: {0} second(s)".format(elapsedTime))

# Input of the game
pipeTypeNumber = np.array([
    np.array([1,2,1,1,2,2,0,1,1,2]),
    np.array([1,3,3,2,2,3,3,1,1,0]),
    np.array([1,3,3,3,3,2,0,2,3,3]),
    np.array([1,2,1,3,3,1,1,0,1,1]),
    np.array([1,2,1,2,3,3,2,3,3,1]),
    np.array([1,3,1,0,2,3,3,1,2,2]),
    np.array([2,3,3,0,2,3,3,3,0,2]),
    np.array([3,1,0,1,3,3,1,2,2,1]),
    np.array([1,1,3,1,2,3,0,2,1,1]),
    np.array([1,3,3,1,2,0,1,2,0,2])
])

pipeDirectionNumber = np.array([
    np.array([0,1,3,1,1,2,1,1,2,1]),
    np.array([0,2,3,1,2,3,1,1,3,1]),
    np.array([1,3,2,3,0,3,0,2,3,1]),
    np.array([1,3,1,1,0,3,3,0,0,1]),
    np.array([3,2,3,1,1,1,3,1,3,0]),
    np.array([0,2,3,0,3,2,1,1,2,3]),
    np.array([3,3,3,1,3,0,2,0,1,2]),
    np.array([2,0,1,1,2,0,3,0,0,2]),
    np.array([0,2,2,1,1,2,0,0,3,3]),
    np.array([2,0,3,3,0,2,3,3,0,2]) 
])

pipeTypeBoard = convertToPipeTypeBoard(pipeTypeNumber)
pipeDirectionBoard = convertToPipeDirectionBoard(pipeDirectionNumber, pipeTypeBoard)

pipeSolver = PipeSolver(pipeTypeBoard, pipeDirectionBoard)
pipeSolver.aStar()
printMemoryUsage()
