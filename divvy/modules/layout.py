from dataclasses import asdict, dataclass
from typing import Dict, Optional

from divvy.modules.screen import ScreenData


@dataclass
class BarHeight:
    top: int
    bottom: int
    left: int
    right: int


@dataclass
class LayoutData:
    horizontal: Dict[str, str]
    vertical: Dict[str, str]


@dataclass
class CalculatedLayout:
    x: int
    y: int
    width: int
    height: int


DEFAULT_LAYOUT = LayoutData(
    horizontal={
        "full-size": "0,0,{width},{height}",
        "half-left": "0,0,{width}/2,{height}",
        "half-right": "{width}/2,0,{width}/2,{height}",
        "top-left": "0,0,{width}/2,{height}/2",
        "top-right": "{width}/2,0,{width}/2,{height}/2",
        "bottom-left": "0,{height}/2,{width}/2,{height}/2",
        "bottom-right": "{width}/2,{height}/2,{width}/2,{height}/2",
        "two-thirds-left": "0,0,{width}*2/3,{height}",
        "two-thirds-right": "{width}/3,0,{width}*2/3,{height}",
        "one-third-left": "0,0,{width}/3,{height}",
        "one-third-right": "{width}*2/3,0,{width}/3,{height}",
        "one-third-top-right": "{width}*2/3,0,{width}/3,{height}/2",
        "one-third-bottom-right": "{width}*2/3,{height}/2,{width}/3,{height}/2",
        "centered-left": "50,{height}*1/6,{width}*3/5,{height}*2/3",
    },
    vertical={
        "full-size": "0,0,{width},{height}",
        "half-top": "0,0,{width},{height}/2",
        "half-bottom": "0,{height}/2,{width},{height}/2",
        "first-quarter": "0,0,{width},{height}/4",
        "second-quarter": "0,{height}/4,{width},{height}/4",
        "third-quarter": "0,{height}/2,{width},{height}/4",
        "fourth-quarter": "0,{height}*3/4,{width},{height}/4",
    },
)


def calculate_layout_screen(
    screen_data: ScreenData, layout: str, bar_height: Optional[BarHeight] = None
) -> CalculatedLayout:
    """Return the calculated layout for the given screen."""

    bar_height = bar_height or BarHeight(0, 0, 0, 0)
    screen_data_dict = asdict(screen_data)
    screen_data_dict["x"] += bar_height.left
    screen_data_dict["y"] += bar_height.top
    screen_data_dict["width"] -= bar_height.left + bar_height.right
    screen_data_dict["height"] -= bar_height.top + bar_height.bottom

    calculated_layout = layout.format(**screen_data_dict)

    result = CalculatedLayout(
        *[int(eval(value)) for value in calculated_layout.split(",")]
    )
    # ensure the result is within the screen bounds
    result.x += bar_height.left
    result.y += bar_height.top

    return result
