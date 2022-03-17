from PipeType import PipeType
from  Direction import Direction
import numpy as np
from os import system, name

def clearScreen():
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')    

# how to use this module?
# we first pass the pipeTypeBoard and pipeDirectionBoard and it will automatically create the board
# after we find a solution, we pass a list of moves to printBoard() and it will print the solution step by step

class BoardPrinter:
    NUM_OF_ROWS_PER_PIPE = NUM_OF_COLUMNS_PER_PIPE = 3 # rows of columns to represent a pipe
    getRowInBoard = lambda self, row : (self.NUM_OF_ROWS_PER_PIPE * row) # get the actual row in the board to print
    getColumnInBoard = lambda self, column : (self.NUM_OF_COLUMNS_PER_PIPE * column)
    
    def __init__(self, pipeTypeBoard, pipeDirectionBoard):
        self.pipeTypeBoard = pipeTypeBoard
        
        self.rows = len(pipeTypeBoard)
        self.columns = len(pipeTypeBoard[0])
        self.rows_PL = self.rows * self.NUM_OF_ROWS_PER_PIPE
        self.columns_PL = self.columns * self.NUM_OF_COLUMNS_PER_PIPE
        
        self.board_to_print = np.full((self.rows_PL, self.columns_PL), " ", str)
        self.createBoard(pipeDirectionBoard)
    
    # set the cell at pipePos to blank space
    def resetPosition(self, pipePos):
        # index in board_to_print
        x_PL = self.getRowInBoard(pipePos[0]) 
        y_PL = self.getColumnInBoard(pipePos[1])
        
        for i in range(x_PL, x_PL + self.NUM_OF_ROWS_PER_PIPE):
            for j in range(y_PL, y_PL + self.NUM_OF_COLUMNS_PER_PIPE):
                self.board_to_print[i][j] = " "
    
    # draw coupling with direction to the board
    def setCoupling(self, pipePos, direction):
        # index in board_to_print
        x_PL = self.getRowInBoard(pipePos[0]) 
        y_PL = self.getColumnInBoard(pipePos[1])
        
        if (direction == Direction.RIGHT):
            for j in range(y_PL, y_PL + self.NUM_OF_COLUMNS_PER_PIPE):
                self.board_to_print[x_PL + 1][j] = "-"
                self.board_to_print[x_PL][j] = self.board_to_print[x_PL + 2][j] = " "
        elif (direction == Direction.UP):
            for i in range(x_PL, x_PL + self.NUM_OF_ROWS_PER_PIPE):
                self.board_to_print[i][y_PL + 1] = "|"
                self.board_to_print[i][y_PL] = self.board_to_print[i][y_PL + 2] = " "
    
    # draw end cap with direction to the board
    def setEndCap(self, pipePos, direction):
        # index in board_to_print
        x_PL = self.getRowInBoard(pipePos[0]) 
        y_PL = self.getColumnInBoard(pipePos[1])
        
        self.resetPosition(pipePos)
        
        self.board_to_print[x_PL + 1][y_PL + 1] = "O"
        if (direction == Direction.RIGHT):
            self.board_to_print[x_PL + 1][y_PL + 2] = "-"
        elif (direction == Direction.UP):
            self.board_to_print[x_PL][y_PL + 1] = "|"
        elif (direction == Direction.LEFT):
            self.board_to_print[x_PL + 1][y_PL] = "-"
        elif (direction == Direction.DOWN):
            self.board_to_print[x_PL + 2][y_PL + 1] = "|"
    
    # draw elbow with direction to the board
    def setElbow(self, pipePos, direction):
        # index in board_to_print
        x_PL = self.getRowInBoard(pipePos[0]) 
        y_PL = self.getColumnInBoard(pipePos[1])
        
        self.resetPosition(pipePos)
        
        if (direction == Direction.RIGHT or direction == Direction.DOWN):
            self.board_to_print[x_PL + 1][y_PL + 1] = self.board_to_print[x_PL + 1][y_PL + 2] = "-"
            if (direction == Direction.RIGHT):
                self.board_to_print[x_PL][y_PL + 1] = "|"
            elif (direction == Direction.DOWN):
                self.board_to_print[x_PL + 2][y_PL + 1] = "|"
        elif (direction == Direction.LEFT or direction == Direction.UP):
            self.board_to_print[x_PL + 1][y_PL + 1] = self.board_to_print[x_PL + 1][y_PL] = "-"
            if (direction == Direction.LEFT):
                self.board_to_print[x_PL + 2][y_PL + 1] = "|"
            elif (direction == Direction.UP):
                self.board_to_print[x_PL][y_PL + 1] = "|"
    
    # draw tee with direction to the board
    def setTee(self, pipePos, direction):
        # index in board_to_print
        x_PL = self.getRowInBoard(pipePos[0]) 
        y_PL = self.getColumnInBoard(pipePos[1])
        
        self.resetPosition(pipePos)
        
        if (direction == Direction.RIGHT or direction == Direction.LEFT):
            for j in range(y_PL, y_PL + self.NUM_OF_COLUMNS_PER_PIPE):
                self.board_to_print[x_PL + 1][j] = "-"
            if (direction == Direction.LEFT):
                self.board_to_print[x_PL + 2][y_PL + 1] = "|"
            elif (direction == Direction.RIGHT):
                self.board_to_print[x_PL][y_PL + 1] = "|"
        
        elif (direction == Direction.UP or direction == Direction.DOWN):
            for i in range(x_PL, x_PL + self.NUM_OF_ROWS_PER_PIPE):
                self.board_to_print[i][y_PL + 1] = "|"
            if (direction == Direction.UP):
                self.board_to_print[x_PL + 1][y_PL] = "-"
            elif (direction == Direction.DOWN):
                self.board_to_print[x_PL + 1][y_PL + 2] = "-"
    
    # draw the initial input to the board
    def createBoard(self, pipeDirectionBoard):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.pipeTypeBoard[i][j] == PipeType.COUPLING:
                    self.setCoupling((i,j), pipeDirectionBoard[i][j])
                elif self.pipeTypeBoard[i][j] == PipeType.END_CAP:
                    self.setEndCap((i,j), pipeDirectionBoard[i][j])
                elif self.pipeTypeBoard[i][j] == PipeType.ELBOW:
                    self.setElbow((i,j), pipeDirectionBoard[i][j])
                elif self.pipeTypeBoard[i][j] == PipeType.TEE:
                    self.setTee((i,j), pipeDirectionBoard[i][j])
    
    def printCurrentBoard(self):
        print((self.columns_PL + 3) * "-")
        for counter in range(self.rows_PL):
            for char in self.board_to_print[counter]:
                print(char, end = "")
            print()
            if ((counter + 1) % 3 == 0):
                print((self.columns_PL + 3) * "-")
    
    # pass a list of moves then it prints step-by-step to console                
    def printBoard(self, movesList):
        counter = 1
        print("The input of game:")
        self.printCurrentBoard()
        
        for step in movesList:
            i = step[0][0]
            j = step[0][1]
            direction = step[1]

            input("Press Enter for next step")
            clearScreen()
            print("Step {0}: rotate the pipe at {1}".format(counter, step[0]))
            counter = counter + 1
            
            if self.pipeTypeBoard[i][j] == PipeType.COUPLING:
                self.setCoupling((i,j), direction)
            elif self.pipeTypeBoard[i][j] == PipeType.END_CAP:
                self.setEndCap((i,j), direction)
            elif self.pipeTypeBoard[i][j] == PipeType.ELBOW:
                self.setElbow((i,j), direction)
            elif self.pipeTypeBoard[i][j] == PipeType.TEE:
                self.setTee((i,j), direction) 
            self.printCurrentBoard()