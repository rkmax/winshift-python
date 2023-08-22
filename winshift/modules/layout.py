from dataclasses import asdict, dataclass
from typing import Dict, Optional

from winshift.modules.screen import ScreenData


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
    validate_layout(layout)
    screen_data_dict = asdict(screen_data)

    calculated_layout = layout.format(**screen_data_dict)

    result = CalculatedLayout(
        *[int(eval(value)) for value in calculated_layout.split(",")]
    )

    # ensure to apply bar_height and screen offsets
    bar_height = bar_height or BarHeight(0, 0, 0, 0)

    if result.x < bar_height.left:
        # calculate the difference
        diff = bar_height.left - result.x
        # apply the difference to the width
        result.x += diff
    if result.y < bar_height.top:
        # calculate the difference
        diff = bar_height.top - result.y
        # apply the difference to the height
        result.y += diff

    if result.width > screen_data.width - bar_height.right:
        # calculate the difference
        diff = result.width - (screen_data.width - bar_height.right)
        # apply the difference to the width
        result.width -= diff

    if result.height > screen_data.height - bar_height.bottom:
        # calculate the difference
        diff = result.height - (screen_data.height - bar_height.bottom)
        # apply the difference to the height
        result.height -= diff

    # always apply screen offsets
    result.x += screen_data.x
    result.y += screen_data.y

    return result


def validate_layout(layout: str) -> None:
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
    except Exception:
        raise ValueError(
            "Invalid layout format. int,int,int,int expected. {width} and {height} are available."
        )
