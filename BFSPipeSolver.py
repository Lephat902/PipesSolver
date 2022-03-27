import numpy as np
from InputReader import InputReader
from PipeType import PipeType
from Direction import Direction
from BoardPrinter import BoardPrinter
from CheckWin import CheckWin
from PipeDirectionsHelper import *
import time  # used to measure elapsed time
import psutil  # used to measure memory usage


def xnor(a, b):
    return ((a and b) or (not a and not b))


def printMemoryUsage():
    # print memory usage
    memoryUsage = psutil.Process().memory_info().rss / (1024 * 1024)
    print("The memory usage is: {0} (MB)".format(memoryUsage))


class queueItem:
    def __init__(self, directionBoard, pipePos, movesList, numOfPipeMismatches):
        self.directionBoard = directionBoard
        self.pipePos = pipePos
        self.movesList = movesList
        self.numOfPipeMismatches = numOfPipeMismatches

    def getDirectionBoard(self):
        return self.directionBoard

    def getPipePos(self):
        return self.pipePos

    def getMovesList(self):
        return self.movesList

    def getNumOfPipeMismatches(self):
        return self.numOfPipeMismatches


class PipeSolver:
    def __init__(self, pipeTypeBoard, pipeDirectionBoard):
        self.pipeTypeBoard = pipeTypeBoard
        self.pipeDirectionBoard = pipeDirectionBoard
        self.rows = len(pipeTypeBoard)
        self.columns = len(pipeTypeBoard[0])
        self.checkWin_obj = CheckWin(self.pipeTypeBoard)
        self.pipeDirectionsHelper = PipeDirectionsHelper(pipeTypeBoard)

    # check if the current pipe's direction matches the left and above ones.
    # the reason why to check the left and top is that they are
    # currently immutable bacause they're already executed
    # Complexity : O(1)
    def isValidMove(self, currentDirectionBoard, pipePos, operation):
        x = pipePos[0]
        y = pipePos[1]

        directions_current = self.pipeDirectionsHelper.get_directions_pipe_point_to(
            pipePos, operation)
        directions_above = self.pipeDirectionsHelper.get_directions_pipe_point_to(
            (x - 1, y), currentDirectionBoard[x - 1][y])
        directions_left = self.pipeDirectionsHelper.get_directions_pipe_point_to(
            (x, y - 1), currentDirectionBoard[x][y - 1])

        matchLeft = xnor((Direction.LEFT in directions_current),
                         (Direction.RIGHT in directions_left))
        matchTop = xnor((Direction.UP in directions_current),
                        (Direction.DOWN in directions_above))

        if (x == self.rows - 1):  # at the bottom edge
            matchBottom = not(Direction.DOWN in directions_current)
            if not matchBottom:
                return False
        if (y == self.columns - 1):  # at the right edge
            matchRight = not(Direction.RIGHT in directions_current)
            if not matchRight:
                return False

        return (matchTop and matchLeft)

    # next position to execute in board
    # Complexity: O(1)
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
        pipeDirectionsHelper_full = PipeDirectionsHelper_full(
            self.pipeTypeBoard, directionBoard)

        # each pipe checks the right and bottom pipe of its
        # Complexity O(n ^ 2)
        for i in range(self.rows):
            for j in range(self.columns):
                currentPipePos = (i, j)
                matchRight = pipeDirectionsHelper_full.matchRight(
                    currentPipePos)
                matchBottom = pipeDirectionsHelper_full.matchBottom(
                    currentPipePos)
                if not matchRight:
                    counter += 1
                if not matchBottom:
                    counter += 1

                if (i == 0):  # if it's at the top edge
                    matchTop = pipeDirectionsHelper_full.matchTop(
                        currentPipePos)
                    if not matchTop:
                        counter += 1
                if (j == 0):  # if it's at the left edge
                    matchLeft = pipeDirectionsHelper_full.matchLeft(
                        currentPipePos)
                    if not matchLeft:
                        counter += 1

        return counter

     # Complexity: O(1)
    def isValidIndex(self, pipePos):
        x = pipePos[0]
        y = pipePos[1]
        return (x >= 0 and x < self.rows and y >= 0 and y < self.columns)

    # those below list is utilities for getNumOfPipeMismatchesAt()
    adjPos_X = [0, -1, 0, 1]
    adjPos_Y = [1, 0, -1, 0]
    fourDirections = [dir for dir in Direction]

    # Complexity : O(1)
    def getNumOfPipeMismatchesAt(self, directionBoard, pipePos):
        x = pipePos[0]
        y = pipePos[1]

        numOfMismatches = 0

        directions_current = self.pipeDirectionsHelper.get_directions_pipe_point_to(
            pipePos, directionBoard[x][y])
        for direction, plusX, plusY in zip(self.fourDirections, self.adjPos_X, self.adjPos_Y):
            adjX = x + plusX
            adjY = y + plusY
            directions_adj = {}
            if (self.isValidIndex((adjX, adjY))):
                directions_adj = self.pipeDirectionsHelper.get_directions_pipe_point_to(
                    (adjX, adjY), directionBoard[adjX][adjY])

            oppositeDirection = Direction.getOppositeDirection(direction)
            match = xnor(direction in directions_current,
                         oppositeDirection in directions_adj)
            if not match:
                numOfMismatches += 1

        return numOfMismatches

    # cal numOfPipeMismatches for new state (not the initial state)
    def getNewNumOfPipeMismatches(self, currentDirectionBoard, newDirectionBoard, pipePos, currentMismatch):
        numOfMismatches_current = self.getNumOfPipeMismatchesAt(
            currentDirectionBoard, pipePos)
        numOfMismatches_new = self.getNumOfPipeMismatchesAt(
            newDirectionBoard, pipePos)
        # new = current + numOfPipeMismatches difference of 2 states when change direction of a pipe
        return (currentMismatch + (numOfMismatches_new - numOfMismatches_current))

    # we don't need the closed list here because we go from left to right, top to bottom.
    # It's guaranteed that there's no loop (the same state occurs one more time)
    def BFS(self):
        start_time = time.time()  # get the start time
        openList = []  # queue
        initialNumOfPipeMismatches = self.getNumOfPipeMismatches_init(
            self.pipeDirectionBoard)
        firstItem = queueItem(self.pipeDirectionBoard,
                              (0, 0), [], initialNumOfPipeMismatches)
        openList.append(firstItem)
        counter = 0  # count for the times popping the queue

        while (openList):
            counter += 1
            current = openList.pop(0)  # pop the first element
            currentDirectionBoard = current.getDirectionBoard()
            currentPos = current.getPipePos()
            currentMovesList = current.getMovesList()
            currentNumOfPipeMismatches = current.getNumOfPipeMismatches()

            # we only check win when there's no mismatch pipes
            if (currentNumOfPipeMismatches == 0 and self.checkWin_obj.checkWin(currentDirectionBoard)):
                end_time = time.time()
                elapsedTime = end_time - start_time
                self.boardPrinter = BoardPrinter(self.pipeTypeBoard, self.pipeDirectionBoard)
                self.boardPrinter.printBoard(currentMovesList)
                print("Total time taken by BFS Algorithm: {0} second(s)".format(elapsedTime))
                print("Number of times popping queue: {0} times".format(counter))
                return

            # the last pipe: we can't rotate any pipe if currentPos = (-1,-1)
            if (currentPos != (-1, -1)):
                currentX = currentPos[0]
                currentY = currentPos[1]
                possibleOperations = self.getAllPossibleOperations(currentPos)

                for operation in possibleOperations:
                    if self.isValidMove(currentDirectionBoard, currentPos, operation):
                        newDirectionBoard = currentDirectionBoard.copy()
                        newPos = self.getNextPos(currentPos)
                        newMovesList = currentMovesList.copy()
                        newNumOfPipeMismatches = currentNumOfPipeMismatches

                        # if there's any change in board then we update those values
                        if (currentDirectionBoard[currentX][currentY] != operation):
                            newDirectionBoard[currentX][currentY] = operation
                            newMovesList.append((currentPos, operation))
                            newNumOfPipeMismatches = self.getNewNumOfPipeMismatches(currentDirectionBoard,
                                                    newDirectionBoard, currentPos, currentNumOfPipeMismatches)

                        newItem = queueItem(newDirectionBoard, newPos, newMovesList, newNumOfPipeMismatches)
                        openList.append(newItem)
        end_time = time.time()
        elapsedTime = end_time - start_time
        print("Cannot find a solution")
        print("Total time taken by BFS Algorithm: {0} second(s)".format(elapsedTime))
        print("Number of times popping queue: {0} times".format(counter))


# Input of the game
inputReader = InputReader('input/test6.txt')
pipeTypeBoard = inputReader.getPipeTypeBoard()
pipeDirectionBoard = inputReader.getDirectionBoard()

pipeSolver = PipeSolver(pipeTypeBoard, pipeDirectionBoard)
pipeSolver.BFS()
printMemoryUsage()
