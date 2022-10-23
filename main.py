'''

Hanchen Zhang
CS5001 - 2021Fall

Final Project
Make a checker game. One side is controlled by computer and the other
is controlled by user.

'''

import turtle
from game_state import GameState
from draw import Draw


def main():
    pen = turtle.Turtle()
    pen.hideturtle()
    game = GameState()
    draw = Draw()
    draw.reset_window(pen, game.squares)
    game.click()
    turtle.done()  # Stops the window from closing.


if __name__ == "__main__":
    main()
