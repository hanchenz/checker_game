'''

Hanchen Zhang
CS5001 - 2021Fall

Final project: Gamestate class

'''

import turtle
import random
from draw import Draw
from constant import Constant


class GameState:
    '''
    Class - GameState
        Handle user's click and the following change of the board
    Attributes:
        c - an instance of Constant
        draw - an instance of Draw
        pen - an instance of turtle
        screen - the turtle screen
        squares - a 8 x 8 list that store all checkers' position
        turn - either black or red turn
        prerow - the selected checker's row
        precol - the selected checker's column
        row - the row where the selected checker wants to move to
        col - the column where the selected checker wants to move to
        multiple - if the checker can perform multiple capture moves
        cap_lst - all the possible positions the checker can move to after
        performing capture move
        move_lst - all the possible positions the checker can move to
        possible_cap_lst - all checkers that can perform capture move
        possible_move_lst - all checkers that can perform non-capture move
        game_end - whether the game ends
        color - color of the side that is taking actions this turn
    Methods:
        init_square - initiate the square list
        click_handler - everything happen in this method
        invalid_click - check if the click is valid
        board_lines - generate a list of board line coordinate that should not
        be clicked on
        before_click - all the calculation before user clicks
        identify_color - check which color's turn it is
        red_turn - check if it's red's turn
        black_turn - check if it's black's turn
        possible_cap - creats a list of checkers that can make capture moves
        capture_lst - create a list of positions that a checkers can move to
        after capture move
        can_capture - check if a capture move can be performed
        validate_index - check if the moves are out of the board
        is_king - check if a piece is king
        possible_move - creats a list of checkers that can make non-capture
        moves
        move_lst - create a list of positions that a checkers can move to
        can_move - check if a non-capture move can be performed
        calc_row_col - calculate row/column based on the click's coordinate
        first_click - all the actions taken when the user select a checker
        valid_selection - check if the checker selection is valid
        save_coordinate - save the row and column
        second_click - all actions taken when the user select the position that
        they want to move the checker
        change_square - change the square list based on the move
        change_king - change checker into king
        change_turn - change the turn
        remove_checker - remove the checker that is captured
        computer_turn - the red side's turn that is controlled by computer
        after_click - change all variables' value to none or empty
        click - the function that is passed to main to detect user's click
    '''

    def __init__(self):
        '''
        Constructor - create an instance of Draw
        Parameter:
            self - the current Draw object
        '''
        self.c = Constant()
        self.draw = Draw()
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.penup()
        self.screen = turtle.Screen()
        self.squares = []
        self.init_square()
        self.turn = self.c.BLK_TURN
        self.prerow = None
        self.precol = None
        self.row = None
        self.col = None
        self.multiple = False
        self.cap_lst = []
        self.move_lst = []
        self.possible_cap_lst = []
        self.possible_move_piece = []
        self.game_end = False

    def init_square(self):
        '''
        Method - init_square
            Initiate the 8 x 8 squares list. The list contains 8 list and
            each list has eight items, just like the board. Checkers position
            will be stored as their colors and empty slot will be stored as
            empty.
        Parameter:
            self - a GameState object
        Return:
            Nothing. Create a square list that represents the initial board
        '''
        for i in range(8):
            self.squares.append([""] * 8)
        for col in range(self.c.NUM_SQUARES):
            for row in range(self.c.NUM_SQUARES):
                if col % 2 != row % 2:
                    if row <= self.c.BLACK_CIRCLE_HIGH:
                        self.squares[row][col] = self.c.BLACK
                    elif row >= self.c.RED_CIRCLE_LOW:
                        self.squares[row][col] = self.c.RED
                    else:
                        self.squares[row][col] = self.c.EMPTY
                else:
                    self.squares[row][col] = self.c.EMPTY

    def click_handler(self, x, y):
        '''
        Method - click_handler
            Called when a click occurs. Draw before move graphs when a
            valid checker is selected and move the checker to a new selected
            spot.
        Parameters:
            self - a GameState object
            x - X coordinate of the click.
            y - Y coordinate of the click.
        Returns:
            Nothing. Perform different tasks in different conditions.
        '''
        if self.invalid_click(x, y):
            print("Invalid click. Clicked at ", x, y)
        else:
            self.before_click()
            if self.black_turn():
                new_col = self.calc_row_col(x)
                new_row = self.calc_row_col(y)
            if self.col is None and not self.multiple:
                self.first_click(new_row, new_col)
            else:
                self.second_click(new_row, new_col)
                if self.red_turn():
                    self.before_click()
                    if not self.game_end:
                        self.computer_turn()
                        self.before_click()  # Check if black looses
                if not self.multiple and not self.game_end:
                    self.after_click()

    def invalid_click(self, x, y):
        '''
        Function - invalid_click
            Check if the click is within the board and not on the
            boundary of the small squares of the board.
        Parameters:
            self - a GameState object
            x - X coordinate of the click.
            y - Y coordinate of the click.
        Return:
            True if the click is invalid and False if otherwise
        '''
        invalid_lst = self.board_lines()
        return abs(x) >= self.c.BOARD_SIZE / 2\
            or abs(y) >= self.c.BOARD_SIZE / 2\
            or x in invalid_lst or y in invalid_lst

    def board_lines(self):
        '''
        Function - board_lines
            Find the coordinate of each small square's boundary (board lines).
            It will be used to validate x and y coordinate of the user's click.
        Parameter:
            self - a GameState object
        Return:
            A list that contains all the coordinates that user should not
            click on.
        '''
        invalid_lst = [self.c.CORNER]
        for i in range(self.c.NUM_SQUARES):
            invalid_lst.append(invalid_lst[-1] + self.c.SQUARE)
        return invalid_lst

    def before_click(self):
        '''
        Method - before_click
            Helper method. Check which color's turn it is and create
            a list of all possible checker that can move or capture.
            If both lists are empty for one color, that color looses since
            no action can be taken.
        Parameter:
            self - a GameState object
        Return:
            Nothing. Identify color, creat move and capture list and check
            if one side loose.
        '''
        self.color = self.identify_color()
        self.possible_cap_lst = self.possible_cap(self.color)
        self.possible_move_piece = self.possible_move(self.color)
        if (len(self.possible_cap_lst) == 0 and
                len(self.possible_move_piece) == 0):
            if self.red_turn():
                print("You win!")
            elif self.black_turn():
                print("You loose!")
            self.game_end = True
            turtle.bye()

    def identify_color(self):
        '''
        Method - identify_color
            Check whose turn it is and return the corresponding color
        Paratemer:
            self - a GameState object
        Return:
            red if it's red's turn and black if it's black's turn
        '''
        if self.red_turn():
            return self.c.RED
        elif self.black_turn():
            return self.c.BLACK

    def red_turn(self):
        '''
        Method - red_turn
            Check if it's red's turn
        Parameter:
            self - a GameState object
        Return:
            True if it's red's turn and False if otherwise
        '''
        return self.turn == self.c.RD_TURN

    def black_turn(self):
        '''
        Method - black_turn
            Check if it's black's turn
        Parameter:
            self - a GameState object
        Return:
            True if it's black's turn and False if otherwise
        '''
        return self.turn == self.c.BLK_TURN

    def possible_cap(self, color):
        '''
        Method - possible_cap
            Creat a list of all checkers that can capture
        Parameter:
            self - a GameState object
            color - color of the side that is taking actions this turn
        Return:
            A list of positions of checkers that can make capture moves.
            The position is presented as [row, column] of the checker on
            the board
        '''
        possible_cap_lst = []
        for row in range(self.c.NUM_SQUARES):
            for col in range(self.c.NUM_SQUARES):
                if (self.squares[row][col][:3] == color
                        or self.squares[row][col][:5] == color):
                    cap_lst = self.capture_lst(row, col, color)
                    if len(cap_lst) > 0:
                        possible_cap_lst.append([row, col])
        return possible_cap_lst

    def capture_lst(self, row, col, color):
        '''
        Method - capture_lst
            Create a list of possible positions that a checker can move to in
            order to perform capture move
        Parameters:
            self - a GameState object
            row - the row of the selected checker
            col - the column of the selected checker
            color - color of the side that is taking actions this turn
        Return:
            A list of all possible capture moves for a checker
        '''
        UP = 1  # one square above the checker
        DN = -1  # one square below the checker
        RT = 1  # one square right to the checker
        LT = -1  # one square left to the checker
        UP2 = 2  # two square above the checker
        DN2 = -2  # two square below the checker
        RT2 = 2  # two square right to the checker
        LT2 = -2  # two square left to the checker

        capture_lst = []
        if color == self.c.BLACK:
            cap = self.c.RED
            if self.can_capture(row, col, UP, RT, UP2, RT2, cap):
                capture_lst.append([row + UP2, col + RT2])  # right
            if self.can_capture(row, col, UP, LT, UP2, LT2, cap):
                capture_lst.append([row + UP2, col + LT2])  # left
            if self.is_king(row, col):
                if self.can_capture(row, col, DN, RT, DN2, RT2, cap):
                    capture_lst.append([row + DN2, col + RT2])  # backright
                if self.can_capture(row, col, DN, LT, DN2, LT2, cap):
                    capture_lst.append([row + DN2, col + LT2])  # backleft
        elif color == self.c.RED:
            cap = self.c.BLACK
            if self.can_capture(row, col, DN, RT, DN2, RT2, cap):
                capture_lst.append([row + DN2, col + RT2])  # right
            if self.can_capture(row, col, DN, LT, DN2, LT2, cap):
                capture_lst.append([row + DN2, col + LT2])  # left
            if self.is_king(row, col):
                if self.can_capture(row, col, UP, RT, UP2, RT2, cap):
                    capture_lst.append([row + UP2, col + RT2])  # backright
                if self.can_capture(row, col, UP, LT, UP2, LT2, cap):
                    capture_lst.append([row + UP2, col + LT2])  # back left
        return capture_lst

    def can_capture(self, row, col, diff_1, diff_2, diff_3, diff_4, cap):
        '''
        Method - can_capture
            Helper method. Check if a checker can perform capture move by
            checking if the checker being captured is the opposite color
            and if the position after capturing is empty
        Parameters:
            self - a GameState object
            row - the row of the selected checker
            col - the column of the selected checker
            diff_1 - one square up or down
            diff_2 - one square right or left
            diff_3 - two squares up or down
            diff_4 - two squares right or left
            cap - the opposite color of the checker selected
        Return:
            True if the checker can perform the particular capture move
            and False if otherwise
        '''
        try:
            self.validate_index(row + diff_3, col + diff_4)
            if cap == self.c.RED:
                return (self.squares[row + diff_1][col + diff_2][:3] == cap and
                        self.squares[row + diff_3][col + diff_4]
                        == self.c.EMPTY)
            elif cap == self.c.BLACK:
                return (self.squares[row + diff_1][col + diff_2][:5] == cap and
                        self.squares[row + diff_3][col + diff_4]
                        == self.c.EMPTY)
        except IndexError:
            return False

    def validate_index(self, row, col):
        '''
        Method - validate_index
            Check if the inputed row and column is valid
        Parameters:
            self - a GameState object
            row - a row
            col - a column
        Return:
            Raise IndexError if either parameter is smaller
            than 0
        '''
        if row < 0 or col < 0:
            raise IndexError

    def is_king(self, row, col):
        '''
        Method - is_king
            Check if the selected piece is king
        Parameters:
            self - a GameState object
            row - the selected piece's row
            col - the selected piece's column
        Return:
            True if the piece is a king and False if otherwise
        '''
        return self.squares[row][col][-4:] == self.c.KING

    def possible_move(self, color):
        '''
        Method - possible_move
            Create a list of all checkers that can move
        Parameter:
            self - a GameState object
            color - color of the side that is taking actions this turn
        Return:
            The list of rows and columns of all checkers that can move
            this turn
        '''
        possible_move_piece = []
        for row in range(self.c.NUM_SQUARES):
            for col in range(self.c.NUM_SQUARES):
                if (self.squares[row][col][:3] == color
                        or self.squares[row][col][:5] == color):
                    move_lst = self.move_list(row, col, color)
                    if len(move_lst) > 0:
                        possible_move_piece.append([row, col])
        return possible_move_piece

    def move_list(self, new_row, new_col, color):
        '''
        Method - move_list
            Create a list of all posible non-capture moves of a
            selected checker
        Parameters:
            self - a GameState object
            new_row - the selected piece's row
            new_col - the selected piece's column
            color - color of the side that is taking actions this turn
        Return:
            The list of all possible non-capture moves positions
        '''
        UP = 1  # one square above the checker
        DN = -1  # one square below the checker
        RT = 1  # one square right to the checker
        LT = -1  # one square left to the checker
        move_lst = []
        blk_move = [[UP, RT], [UP, LT]]
        rd_move = [[DN, RT], [DN, LT]]
        king_move = blk_move + rd_move
        if self.is_king(new_row, new_col):
            for move in king_move:
                if self.can_move(new_row, new_col, move[0], move[1]):
                    move_lst.append([new_row + move[0], new_col + move[1]])
        elif color == self.c.BLACK:
            for move in blk_move:
                if self.can_move(new_row, new_col, move[0], move[1]):
                    move_lst.append([new_row + move[0], new_col + move[1]])
        elif color == self.c.RED:
            for move in rd_move:
                if self.can_move(new_row, new_col, move[0], move[1]):
                    move_lst.append([new_row + move[0], new_col + move[1]])
        return move_lst

    def can_move(self, row, col, row_diff, col_diff):
        '''
        Method - can_move
            Helper method. Check if the position that the checker wants
            to move to is empty and not out of the board.
        Parameters:
            self - a GameState object
            row - the row of the selected checker
            col - the column of the selected checker
            row_diff - one square above or below the selected checker
            col_diff - one square on the right or left of the selected
            checker
        Return:
            True if the checker can move to the indicated position and False
            if otherwise
        '''
        try:
            self.validate_index(row + row_diff, col + col_diff)
            return self.squares[row + row_diff][col + col_diff] == self.c.EMPTY
        except IndexError:
            return False

    def calc_row_col(self, coordinate):
        '''
        Method - calc_row_col
            Calculate the row and column based on the coordinate
        Parametes:
            self - a GameState object
            coordinate - x or y of user's click
        Return:
            The row and column based on the coordinate
        '''
        return int((coordinate - self.c.CORNER) // self.c.SQUARE)

    def first_click(self, new_row, new_col):
        '''
        Method - first_click
            All the response of the board when users select a checker
        Parameters:
            self - a GameState object
            new_row - the row of the user's selected checker
            new_col - the column of the user's selected checker
        Return:
            Nothing. Check if the selection is valid and draw the blue and red
            squares before moving the checker. Save the selected checker's
            column and row.
        '''
        if self.valid_selection(new_row, new_col, self.color):
            if len(self.possible_cap_lst) == 0:
                self.move_lst = self.move_list(new_row, new_col, self.color)
                for move in self.move_lst:
                    self.draw.before_move(self.pen, new_row, new_col,
                                          move[0], move[1])
            else:
                self.cap_lst = self.capture_lst(new_row, new_col, self.color)
                for direction in self.cap_lst:
                    self.draw.before_move(self.pen, new_row, new_col,
                                          direction[0], direction[1])
            self.save_coordinate(new_col, new_row)

    def valid_selection(self, row, col, color):
        '''
        Method - valid_selection
            Check if the checker selection is valid. The color
            of the checker has to be same as the player's color.
            When the possible capture list is not empty the selected
            piece must be in the list. If it's empty then the selected
            cheker must be in possible move list.
        Parameters:
            self - a GameState object
            row - the selected piece's row
            col - the selected piece's column
            color - color of the side that is taking actions this turn
        Return:
            True if the selected piece follows the above rule and False if
            otherwise
        '''
        if (self.squares[row][col][:3] == color
                or self.squares[row][col][:5] == color):
            if len(self.possible_cap_lst) > 0:
                return [row, col] in self.possible_cap_lst
            return [row, col] in self.possible_move_piece
        return False

    def save_coordinate(self, new_col, new_row):
        '''
        Method - save_coordinate
            During the first click when col and row are None,
            save the row and column of the selected checker to col
            and row. During the second click, save the row and column
            of selected checker to prerow and precol and save the row
            and column of position that the checker wants to move to to
            col and row
        Parameters:
            self - a GameState object
            new_col - the column of the selected checker or
            where the checker wants to move to
            new_row - the row of the selected checker or
            where the checker wants to move to
        Return:
            Nothing. Save the two positions
        '''
        self.precol = self.col
        self.col = new_col
        self.prerow = self.row
        self.row = new_row

    def second_click(self, new_row, new_col):
        '''
        Method - second_click
            All the reaction when the user click the second time to move
            the selected checker. Either perform non-capture move, capture
            move or multiple capture moves.
        Parameters:
            self - a GameState object
            new_col - the column where the checker wants to move to
            new_row - the row where the checker wants to move to
        Return:
            Nothing. Redraw the board based on the user's click
        '''
        go_place = [new_row, new_col]
        if go_place in self.move_lst:
            self.save_coordinate(new_col, new_row)
            self.change_square(new_row, new_col)
            self.change_turn()
        if go_place in self.cap_lst:
            self.save_coordinate(new_col, new_row)
            remove_row = self.prerow + ((new_row - self.prerow) // 2)
            remove_col = self.precol + ((new_col - self.precol) // 2)
            self.remove_checker(remove_row, remove_col)
            self.change_square(new_row, new_col)
            self.draw.reset_window(self.pen, self.squares)
            self.cap_lst = self.capture_lst(new_row, new_col, self.color)
            if len(self.cap_lst) != 0:
                self.multiple = True
                for direction in self.cap_lst:
                    self.draw.before_move(self.pen, new_row, new_col,
                                          direction[0], direction[1])
            else:
                self.change_turn()
                self.multiple = False

    def change_square(self, new_row, new_col):
        '''
        Method - change_square
            Move the checker on square list
        Parameters:
            self - a GameState object
            new_col - the column where the checker wants to move to
            new_row - the row where the checker wants to move to
        Return:
            Nothing. Change the square list based on the move
        '''
        self.squares[new_row][new_col] = self.squares[self.prerow][self.precol]
        self.squares[self.prerow][self.precol] = self.c.EMPTY
        self.change_king(new_row, new_col)

    def change_king(self, row, col):
        '''
        Method - change_king
            Check if any checker can be changed into king
        Parameters:
            self - a GameState object
            row - the row where the checker wants to move to
            col - the column where the checker wants to move to
        Return:
            Nothing. Change the check's name into red king or
            black king in the square list
        '''
        if (self.squares[row][col] == self.c.BLACK
                and self.squares[row][col] in self.squares[7]):
            self.squares[row][col] = self.c.BLK_KING
        elif (self.squares[row][col] == self.c.RED
              and self.squares[row][col] in self.squares[0]):
            self.squares[row][col] = self.c.RD_KING

    def change_turn(self):
        '''
        Method - change_turn
            Change player's turn
        Parameter:
            self - a GameState object
        Return:
            Nothing. Change turn to the opposite color.
        '''
        if self.black_turn():
            self.turn = self.c.RD_TURN
        elif self.red_turn():
            self.turn = self.c.BLK_TURN

    def remove_checker(self, row, col):
        '''
        Method - remove_checker
            Remove the checker that is being captured
        Parameters:
            self - a GameState object
            row - the row of of the captured checker
            col - the column of the captued checker
        Return:
            Nothing. Change the captured checker into
            empty in the square list
        '''
        self.squares[row][col] = self.c.EMPTY

    def computer_turn(self):
        '''
        Method - computer_turn
            Randomly select a checker. The checker must be
            in possible capture list if the list is not empty.
            Then the selected checker will be randomly moved to
            a valid spot, either performing capture, multiple capture
            or non-capture move
        Parameter:
            self - a GameState object
        Return:
            Nothing. Computer makes its move.
        '''
        if len(self.possible_cap_lst) > 0:
            col_row = random.choice(self.possible_cap_lst)
        else:
            col_row = random.choice(self.possible_move_piece)
        self.first_click(col_row[0], col_row[1])
        if len(self.possible_cap_lst) == 0:
            col_row = random.choice(self.move_lst)
            self.second_click(col_row[0], col_row[1])
        else:
            self.multiple = True
            while self.red_turn() and self.multiple:
                col_row = random.choice(self.cap_lst)
                self.second_click(col_row[0], col_row[1])

    def after_click(self):
        '''
        Method - after_click
            Set everything to None or empty and redraw everything
        Parameters:
            self - a GameState object
        Return:
            Nothing. Set all variable to empty and redraw the board
        '''
        self.save_coordinate(None, None)
        self.draw.reset_window(self.pen, self.squares)
        self.color = None
        self.cap_lst = []
        self.move_lst = []

    def click(self):
        '''
        Method - click
            Make click handler works and detect user's click
        Parameter:
            self - a GameState object
        Return:
            Nothing. Help detect user's click
        '''
        self.screen.onclick(self.click_handler)
