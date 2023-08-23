from dataclasses import dataclass
import subprocess
from typing import List, Optional

from winshift.modules.direction import Direction


@dataclass
class ScreenData:
    name: str
    x: int
    y: int
    width: int
    height: int
    direction: Direction


def _parse_screen_data(screen_data: List[str]) -> ScreenData:
    """Return screen data from xrandr output."""

    name = screen_data[3]
    x = int(screen_data[2].split("+")[1])
    y = int(screen_data[2].split("+")[2])
    width = int(screen_data[2].split("+")[0].split("x")[0].split("/")[0])
    height = int(screen_data[2].split("+")[0].split("x")[1].split("/")[0])
    direction = Direction.HORIZONTAL if width > height else Direction.VERTICAL

    return ScreenData(name, x, y, width, height, direction)


def get_screens_data() -> List[ScreenData]:
    """Return screen data using xrandr."""
    args = ["xrandr", "--listactivemonitors"]
    with subprocess.Popen(args, stdout=subprocess.PIPE) as xrandr:
        monitors = xrandr.stdout.read().decode("utf-8").split("\n")[1:-1]
        return [_parse_screen_data(monitor.split()) for monitor in monitors]


def locate_point_on_screen(screens: List[ScreenData], x: int, y: int) -> Optional[ScreenData]:
    """Return the screen where the point is located."""
    horizontal_matches = []
    vertical_matches = []
    # try to match both horizontal and vertical
    for screen in screens:
        screen_left = screen.x
        screen_top = screen.y
        screen_right = screen.x + screen.width
        screen_bottom = screen.y + screen.height

        if screen_left <= x <= screen_right:
            horizontal_matches.append(screen)
        if screen_top <= y <= screen_bottom:
            vertical_matches.append(screen)

        if screen_left <= x <= screen_right and screen_top <= y <= screen_bottom:
            return screen

    # if no match, try to match only horizontal or vertical
    if horizontal_matches:
        return horizontal_matches[0]
    if vertical_matches:
        return vertical_matches[0]

    return None
