'''

Hanchen Zhang
CS5001 - 2021Fall

Final project: The drawing class

'''

import turtle
from constant import Constant


class Draw:
    '''
    Class - Draw
        All the drawing components
    Methods:
        position_calc - calculate where to set the turtle's position
        on the screen
        draw_squares - draw a square
        draw_circle - draw a circle
        before_move - draw the blue and red squares when a checker is
        selected and ready to move or capture
        reset_window - draw the board and chekers based on the squares list
    '''

    def __init__(self):
        '''
        Constructor - create an instance of Draw
        Parameter:
            self - the current Draw object
        '''
        self.c = Constant()

    def position_calc(self, position):
        '''
        Method - position_calc
            Helper function. Calculate where to set the turtle's position
            based on the row/column
        Parameter:
            self - the current Draw object
            position - a row or a column
        Return:
            The position where turtle should be set before it starts drawing
        '''
        return self.c.CORNER + self.c.SQUARE * position

    def draw_square(self, a_turtle, size):
        '''
        Method - draw_square
            Draw a square of a given size.
        Parameters:
            self - the current Draw object
            a_turtle -- an instance of Turtle
            size -- the length of each side of the square
        Returns:
            Nothing. Draws a square in the graphics window.
        '''
        RIGHT_ANGLE = 90
        a_turtle.pendown()
        for i in range(4):
            a_turtle.forward(size)
            a_turtle.left(RIGHT_ANGLE)
        a_turtle.penup()

    def draw_circle(self, a_turtle, radius):
        '''
        Method - draw_circle
            Draw a circle with the givern radius
        Parameters:
            self - the current Draw object
            a_turtle - an instance of Turtle
            radius = The radius of the circle
        Return:
            Northing. Draw a circle in the graphics window.
        '''
        a_turtle.begin_fill()
        a_turtle.pendown()
        a_turtle.circle(radius)
        a_turtle.end_fill()
        a_turtle.penup()

    def before_move(self, a_turtle, sel_row, sel_col, go_row, go_col):
        '''
        Method - before_move
            Draw blue square around the selected piece and red square on the
            positions where the piece can go to, either move or capture
        Parameters:
            self - the current Draw object
            a_turtle - an instance of Turtle
            sel_row - the row of the selected piece
            sel_col - the column of the selected piece
            go_row - the row where the piece can go to
            go_col - the column where the piece can go to
        Return:
            Nothing. Draw the blue and red squares.
        '''
        a_turtle.setposition(self.position_calc(sel_col),
                             self.position_calc(sel_row))
        a_turtle.color("blue")
        self.draw_square(a_turtle, self.c.SQUARE)
        a_turtle.color("red")
        a_turtle.setposition(self.position_calc(go_col),
                             self.position_calc(go_row))
        self.draw_square(a_turtle, self.c.SQUARE)

    def reset_window(self, a_turtle, squares):
        '''
        Method - reset_window
            Set up the window, draw the board and checker pieces based on the
            squares.
        Parameters:
            self - the current Draw object
            a_turtle - an instance of Turtle
            squares - the list that represent the position of checkers on the
                      board
        Return:
            Nothing. Draw the board and checkers.
        '''
        window_size = self.c.BOARD_SIZE + self.c.SQUARE
        turtle.setup(window_size, window_size)
        turtle.screensize(self.c.BOARD_SIZE, self.c.BOARD_SIZE)
        turtle.bgcolor("white")
        turtle.tracer(0, 0)
        a_turtle.penup()
        a_turtle.color("black", "white")
        a_turtle.setposition(self.c.CORNER, self.c.CORNER)
        self.draw_square(a_turtle, self.c.BOARD_SIZE)
        radius = self.c.SQUARE / 2
        for col in range(self.c.NUM_SQUARES):
            for row in range(self.c.NUM_SQUARES):
                if col % 2 != row % 2:
                    a_turtle.setposition(self.position_calc(col),
                                         self.position_calc(row))
                    a_turtle.color("black", self.c.SQUARE_COLORS[0])
                    a_turtle.begin_fill()
                    self.draw_square(a_turtle, self.c.SQUARE)
                    a_turtle.end_fill()
                if squares[row][col][:5] == self.c.BLACK:
                    a_turtle.setposition(self.position_calc(col)
                                         + self.c.SQUARE / 2,
                                         self.position_calc(row))
                    a_turtle.color(self.c.CIRCLE_COLORS[0],
                                   self.c.CIRCLE_COLORS[0])
                    self.draw_circle(a_turtle, radius)
                if squares[row][col][:3] == self.c.RED:
                    a_turtle.setposition(self.position_calc(col)
                                         + self.c.SQUARE / 2,
                                         self.position_calc(row))
                    a_turtle.color(self.c.CIRCLE_COLORS[1],
                                   self.c.CIRCLE_COLORS[1])
                    self.draw_circle(a_turtle, radius)
                if squares[row][col][-4:] == self.c.KING:
                    a_turtle.setposition(self.position_calc(col)
                                         + self.c.SQUARE / 2,
                                         self.position_calc(row)
                                         + self.c.SQUARE / 4)
                    a_turtle.pendown()
                    a_turtle.color("white")
                    a_turtle.circle(radius - self.c.SQUARE / 4)
                    a_turtle.penup()
