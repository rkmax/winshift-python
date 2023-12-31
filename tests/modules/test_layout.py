from typing import Optional

import pytest
from winshift.modules import layout
from winshift.modules.direction import Direction
from winshift.modules.layout import CalculatedLayout, BarHeight, Layout
from winshift.modules.screen import ScreenData


BAR_HEIGHTS_SET = [
    (
        BarHeight(top=0, right=0, bottom=0, left=960, screen_name="DP-0"),
        "{width}/2,0,{width}/2,{height}",
        CalculatedLayout(
            x=960,
            y=0,
            width=960,
            height=1080,
        ),
    ),
    (
        BarHeight(top=0, right=960, bottom=0, left=0, screen_name="DP-0"),
        "0,0,{width}/2,{height}",
        CalculatedLayout(
            x=0,
            y=0,
            width=960,
            height=1080,
        ),
    ),
    (
        BarHeight(top=540, right=0, bottom=0, left=0, screen_name="DP-0"),
        "0,{height}/2,{width},{height}/2",
        CalculatedLayout(
            x=0,
            y=540,
            width=1920,
            height=540,
        ),
    ),
    (
        BarHeight(top=0, right=0, bottom=540, left=0, screen_name="DP-0"),
        "0,0,{width},{height}/2",
        CalculatedLayout(
            x=0,
            y=0,
            width=1920,
            height=540,
        ),
    ),
    (
        BarHeight(top=0, right=0, bottom=540, left=0, screen_name="DP-0"),
        "0,0,{width},{height}/2",
        CalculatedLayout(
            x=0,
            y=0,
            width=1920,
            height=540,
        ),
    ),
]


@pytest.mark.parametrize(
    "screen_data, layout_str, bar_height, expected",
    [
        (
            ScreenData(
                name="DP-0",
                x=0,
                y=0,
                width=1920,
                height=1080,
                direction=Direction.HORIZONTAL,
            ),
            "{x},{y},{width},{height}",
            None,
            CalculatedLayout(
                x=0,
                y=0,
                width=1920,
                height=1080,
            ),
        ),
        (
            ScreenData(
                name="DP-0",
                x=0,
                y=0,
                width=1920,
                height=1080,
                direction=Direction.HORIZONTAL,
            ),
            "{x},{y},{width}/2,{height}",
            None,
            CalculatedLayout(
                x=0,
                y=0,
                width=960,
                height=1080,
            ),
        ),
        (
            ScreenData(
                name="DP-0",
                x=0,
                y=0,
                width=1920,
                height=1080,
                direction=Direction.HORIZONTAL,
            ),
            "{x},{y},{width},{height}",
            BarHeight(top=10, right=10, bottom=10, left=10, screen_name="DP-0"),
            CalculatedLayout(
                x=10,
                y=10,
                width=1910,
                height=1070,
            ),
        ),
        (
            ScreenData(
                name="DP-2",
                x=0,
                y=0,
                width=2160,
                height=3840,
                direction=Direction.VERTICAL,
            ),
            "0,{height}*2/3,{width},{height}/3",
            BarHeight(top=45, right=45, bottom=45, left=45, screen_name="DP-2"),
            CalculatedLayout(x=45, y=2560, width=2160 - (2*45), height=1280-45)
        )
    ],
)
def test_calculate_layout_screen(
    screen_data: ScreenData,
    layout_str: str,
    bar_height: Optional[BarHeight],
    expected: CalculatedLayout,
) -> None:
    result = layout.calculate_layout_screen(
        screen_data,
        Layout(
            name="test",
            layout=layout_str,
            direction=Direction.HORIZONTAL,
        ),
        bar_height,
    )

    assert result == expected


@pytest.mark.parametrize("bar_height, layout_str, expected", BAR_HEIGHTS_SET)
def test_calculate_layout_bar_height(bar_height: BarHeight, layout_str: str, expected: CalculatedLayout) -> None:
    """Test that the bar height is applied correctly. considering the screen dimensions."""
    result = layout.calculate_layout_screen(
        ScreenData(
            name="DP-0",
            x=0,
            y=0,
            width=1920,
            height=1080,
            direction=Direction.HORIZONTAL,
        ),
        Layout(
            name="test",
            layout=layout_str,
            direction=Direction.HORIZONTAL,
        ),
        bar_height,
    )

    assert result == expected


@pytest.mark.parametrize(
    "layout_str",
    [
        "0,0,{width}/2",
        "af,0,0,4",
    ],
)
def test_calculate_layout_screen_invalid_layout(layout_str: str) -> None:
    with pytest.raises(ValueError):
        layout.calculate_layout_screen(
            ScreenData(
                name="DP-0",
                x=0,
                y=0,
                width=1920,
                height=1080,
                direction=Direction.HORIZONTAL,
            ),
            Layout(
                name="test",
                layout=layout_str,
                direction=Direction.HORIZONTAL,
            ),
            None,
        )
