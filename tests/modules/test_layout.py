from typing import Optional

import pytest
from divvy.modules import layout
from divvy.modules.layout import CalculatedLayout, BarHeight
from divvy.modules.screen import ScreenData


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
                layout="horizontal",
            ),
            "0,0,{width},{height}",
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
                layout="horizontal",
            ),
            "0,0,{width}/2,{height}",
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
                layout="horizontal",
            ),
            "0,0,{width},{height}",
            BarHeight(10, 10, 10, 10),
            CalculatedLayout(
                x=10,
                y=10,
                width=1900,
                height=1060,
            ),
        ),
    ],
)
def test_calculate_layout_screen(
    screen_data: ScreenData,
    layout_str: str,
    bar_height: Optional[BarHeight],
    expected: CalculatedLayout,
):
    result = layout.calculate_layout_screen(
        screen_data,
        layout_str,
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
                layout="horizontal",
            ),
            layout_str,
            None,
        )
