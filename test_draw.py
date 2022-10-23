from draw import Draw


def test_position_calc():
    d = Draw()
    assert d.position_calc(2) == -101
