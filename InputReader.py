import numpy as np
from PipeType import PipeType
from Direction import Direction

def convertToPipeTypeBoard(pipeTypeNumberBoard):
    rows = len(pipeTypeNumberBoard)
    columns = len(pipeTypeNumberBoard[0])
    pipeTypeBoard = np.zeros((rows, columns), PipeType)

    for i in range(rows):
        for j in range(columns):
            pipeTypeBoard[i][j] = PipeType(pipeTypeNumberBoard[i][j])

    return pipeTypeBoard

def convertToPipeDirectionBoard(pipeDirectionNumberBoard, pipeTypeBoard):
    rows = len(pipeDirectionNumberBoard)
    columns = len(pipeDirectionNumberBoard[0])
    pipeDirectionBoard = np.zeros((rows, columns), Direction)

    for i in range(rows):
        for j in range(columns):
            pipeDirectionBoard[i][j] = Direction(pipeDirectionNumberBoard[i][j])
            # adjust the direction if user input for coupling is wrong
            if (pipeTypeBoard[i][j] == PipeType.COUPLING):
                if (pipeDirectionBoard[i][j] == Direction.LEFT):
                    pipeDirectionBoard[i][j] = Direction.RIGHT
                elif (pipeDirectionBoard[i][j] == Direction.DOWN):
                    pipeDirectionBoard[i][j] = Direction.UP  

    return pipeDirectionBoard

class InputReader:
    def __init__(self, filePath):
        self.filePath = filePath
        self.buildOutput()

    def buildOutput(self):
        with open(self.filePath) as file:
            self.array2d = [([int(digit) for digit in line.split(",")]) for line in file if ("," in line)]   
            self.numOfLines = len(self.array2d)

        pipeTypeNumberBoard = np.array(self.array2d[0 : (int(self.numOfLines / 2))])
        self.pipeTypeBoard = convertToPipeTypeBoard(pipeTypeNumberBoard)

        pipeDirectionNumberBoard = np.array(self.array2d[int(self.numOfLines / 2) : self.numOfLines])
        self.pipeDirectionBoard = convertToPipeDirectionBoard(pipeDirectionNumberBoard, self.pipeTypeBoard)

    def getPipeTypeBoard(self):
        return self.pipeTypeBoard
    
    def getDirectionBoard(self):
        return self.pipeDirectionBoard