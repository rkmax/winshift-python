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
    gap: int


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
    bar_height = bar_height or BarHeight(top=0, bottom=0, left=0, right=0, gap=0, screen_name=screen_data.name)

    # calculate if the result goes beyond the established limits for each side of the screen
    # otherwise we use the gap
    if result.x < bar_height.left:
        diff = bar_height.left - result.x
        result.x += diff
    else:
        result.x += bar_height.gap
    if result.y < bar_height.top:
        diff = bar_height.top - result.y
        result.y += diff
    else:
        result.y += bar_height.gap

    if result.x + result.width > screen_data.width - bar_height.right:
        diff = (result.x + result.width) - (screen_data.width - bar_height.right)
        result.width -= diff
    else:
        result.width -= bar_height.gap

    if result.y + result.height > screen_data.height - bar_height.bottom:
        diff = (result.y + result.height) - (screen_data.height - bar_height.bottom)
        result.height -= diff
    else:
        result.height -= bar_height.gap

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


def validate_layout_name(layout_name: str) -> None:
    if layout_name == "" or layout_name is None:
        raise ValueError("layout_name must not be empty")


def validate_bar_height(bar_height: BarHeight) -> None:
    if bar_height.screen_name == "" or bar_height.screen_name is None:
        raise ValueError("screen_name must not be empty")
