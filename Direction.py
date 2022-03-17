import enum

class Direction(enum.Enum): # clockwise
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3
    
    def getOppositeDirection(direction):
        directionNum = direction.value
        return Direction((directionNum + 2) % len(Direction))
    
    def getNextDirection_clockwise(direction):
        directionNum = direction.value
        return Direction((directionNum + 1) % len(Direction))
    
    def getNextDirection_anticlockwise(direction):
        directionNum = direction.value
        return Direction((directionNum - 1) % len(Direction))       