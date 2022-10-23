'''

Hanchen Zhang
CS5001 - 2021Fall

Final project: All the constants

'''


class Constant:
    '''
    Class - Constant
        All the constants
    '''
    NUM_SQUARES = 8
    SQUARE = 50  # The size of each square in the checkerboard.
    BOARD_SIZE = NUM_SQUARES * SQUARE
    CORNER = -BOARD_SIZE / 2 - 1
    SQUARE_COLORS = ("light gray", "white")
    CIRCLE_COLORS = ("black", "dark red")
    BLACK_CIRCLE_HIGH = 2  # The highest row index of black circle
    RED_CIRCLE_LOW = 5  # The lowest row index of red circle
    RED = "red"
    BLACK = "black"
    EMPTY = "empty"
    RIGHT = "right"
    LEFT = "left"
    BLK_TURN = 0
    RD_TURN = 1
    BLK_KING = "black king"
    RD_KING = "red king"
    BACK_RT = "back right"
    BACK_LFT = "back left"
    KING = "king"

    def __init__(self):
        '''
        Constructor - create an instance of Constant
        Parameter:
            self - an instance of Constant
        '''
        pass
