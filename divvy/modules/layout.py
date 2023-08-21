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


DEFAULT_LAYOUTS_DATA = LayoutData(
    horizontal={
        "full-size": "{x},{y},{width},{height}",
        "half-left": "{x},{y},{width}/2,{height}",
        "half-right": "{width}/2,{y},{width}/2,{height}",
        "top-left": "{x},{y},{width}/2,{height}/2",
        "top-right": "{width}/2,{y},{width}/2,{height}/2",
        "bottom-left": "{x},{height}/2,{width}/2,{height}/2",
        "bottom-right": "{width}/2,{height}/2,{width}/2,{height}/2",
        "two-thirds-left": "{x},{y},{width}*2/3,{height}",
        "two-thirds-right": "{width}/3,{y},{width}*2/3,{height}",
        "one-third-left": "{x},{y},{width}/3,{height}",
        "one-third-right": "{width}*2/3,{y},{width}/3,{height}",
        "one-third-top-right": "{width}*2/3,{y},{width}/3,{height}/2",
        "one-third-bottom-right": "{width}*2/3,{height}/2,{width}/3,{height}/2",
        "centered-left": "50,{height}*1/6,{width}*3/5,{height}*2/3",
    },
    vertical={
        "full-size": "{x},{y},{width},{height}",
        "half-top": "{x},{y},{width},{height}/2",
        "half-bottom": "{x},{height}/2,{width},{height}/2",
        "first-quarter": "{x},{y},{width},{height}/4",
        "second-quarter": "{x},{height}/4,{width},{height}/4",
        "third-quarter": "{x},{height}/2,{width},{height}/4",
        "fourth-quarter": "{x},{height}*3/4,{width},{height}/4",
    },
)


def calculate_layout_screen(
    screen_data: ScreenData, layout: str, bar_height: Optional[BarHeight] = None
) -> CalculatedLayout:
    """Return the calculated layout for the given screen."""

    if not _validate_layout(layout):
        raise ValueError(
            "Invalid layout format. int,int,int,int expected. {width} and {height} are available."
        )

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

    return result


def _validate_layout(layout: str) -> bool:
    """Return True if the layout is valid int,int,int,int str format"""
    try:
        x, y, width, height = layout.format(
            **{
                "x": 0,
                "y": 0,
                "width": 1920,
                "height": 1080,
            }
        ).split(",")
        int(eval(x))
        int(eval(y))
        int(eval(width))
        int(eval(height))
        return True
    except ValueError:
        return False
    except NameError:
        return False
