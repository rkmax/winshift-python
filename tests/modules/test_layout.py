from divvy.modules import layout
from divvy.modules.screen import ScreenData


def test_calculate_layout_screen():
    result = layout.calculate_layout_screen(
        ScreenData(
            name="DP-0",
            x=0,
            y=0,
            width=1920,
            height=1080,
            layout="horizontal",
        ),
        "full-size",
    )

    expected = {
        "x": 0,
        "y": 0,
        "width": 1920,
        "height": 1080,
    }

    assert result == expected
