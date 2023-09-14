from dataclasses import asdict, dataclass
from typing import Dict, Optional
from simpleeval import simple_eval

from winshift.modules.direction import Direction
from winshift.modules.screen import ScreenData


@dataclass
class BarHeight:
    screen_name: str
    top: int
    bottom: int
    left: int
    right: int


@dataclass
class Layout:
    name: str
    layout: str
    direction: Direction


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


def calculate_layout_screen(
    screen_data: ScreenData, layout: Layout, bar_height: Optional[BarHeight] = None
) -> CalculatedLayout:
    """Return the calculated layout for the given screen."""
    validate_layout(layout.layout)
    screen_data_dict = asdict(screen_data)

    calculated_layout = layout.layout.format(**screen_data_dict)

    result = CalculatedLayout(*[simple_eval(value) for value in calculated_layout.split(",")])

    # ensure to apply bar_height and screen offsets
    bar_height = bar_height or BarHeight(top=0, bottom=0, left=0, right=0, screen_name=screen_data.name)

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
        simple_eval(x)
        simple_eval(y)
        simple_eval(width)
        simple_eval(height)
    except Exception as exc:
        raise ValueError(
            "Invalid layout format. int,int,int,int expected. {width} and {height} are available."
        ) from exc