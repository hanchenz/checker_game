from game_state import GameState
from constant import Constant
from pytest import raises

c = Constant()


def test_init():
    g = GameState()
    assert g.turn == c.BLK_TURN
    assert g.cap_lst == []
    assert g.move_lst == []
    assert g.possible_cap_lst == []
    assert g.possible_move_piece == []
    assert len(g.squares) == 8
    assert g.prerow is None
    assert g.precol is None
    assert g.row is None
    assert g.col is None
    assert not g.multiple
    assert not g.game_end


def test_invalid_click():
    g = GameState()
    assert g.invalid_click(201, 180)
    assert g.invalid_click(100, -220)
    assert g.invalid_click(-151, 100)


def test_identify_color_red_black_turn():
    g = GameState()
    assert g.identify_color() == c.BLACK
    assert g.black_turn()
    g.change_turn()
    assert g.identify_color() == c.RED
    assert g.red_turn()


def test_validate_index():
    g = GameState()
    with raises(IndexError):
        g.validate_index(-2, 7)
    with raises(IndexError):
        g.validate_index(0, -1)


def test_is_king():
    g = GameState()
    g.squares[1][1] = c.KING
    assert g.is_king(1, 1)


def test_can_move():
    g = GameState()
    assert g.can_move(2, 1, 1, 1)


def test_cal_row_col():
    g = GameState()
    assert g.calc_row_col(10) == 4


def test_valid_selection():
    g = GameState()
    g.before_click()
    assert g.valid_selection(2, 1, c.BLACK)
    g.change_turn()
    g.before_click()
    assert g.valid_selection(5, 0, c.RED)


def test_save_coordinate():
    g = GameState()
    g.save_coordinate(5, 2)
    assert g.row == 2
    assert g.col == 5
    assert g.prerow is None
    assert g.precol is None
    g.save_coordinate(6, 3)
    assert g.row == 3
    assert g.col == 6
    assert g.prerow == 2
    assert g.precol == 5
    g.change_square(3, 6)
    assert g.squares[3][6] == c.BLACK
    g.after_click()
    assert g.row is None
    assert g.col is None


def test_change_king():
    g = GameState()
    g.squares[0][1] = c.RED
    g.change_king(0, 1)
    assert g.squares[0][1] == c.RD_KING
