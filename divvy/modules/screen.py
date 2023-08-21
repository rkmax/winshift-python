from dataclasses import dataclass
import subprocess
from typing import List, Optional


@dataclass
class ScreenData:
    name: str
    x: int
    y: int
    width: int
    height: int
    layout: str


def _parse_screen_data(screen_data: List[str]) -> ScreenData:
    """Return screen data from xrandr output."""

    name = screen_data[3]
    x = int(screen_data[2].split("+")[1])
    y = int(screen_data[2].split("+")[2])
    width = int(screen_data[2].split("+")[0].split("x")[0].split("/")[0])
    height = int(screen_data[2].split("+")[0].split("x")[1].split("/")[0])
    layout = "horizontal" if width > height else "vertical"

    return ScreenData(name, x, y, width, height, layout)


def get_screens_data() -> List[ScreenData]:
    """Return screen data using xrandr."""
    xrandr = subprocess.Popen(
        ["xrandr", "--listactivemonitors"], stdout=subprocess.PIPE
    )
    monitors = xrandr.stdout.read().decode("utf-8").split("\n")[1:-1]
    return [_parse_screen_data(monitor.split()) for monitor in monitors]


def get_screen_of_window(
    screens_data: List[ScreenData], window_data: dict
) -> Optional[ScreenData]:
    """Return the screen where the window is located using x,y of the window."""
    for screen in screens_data:
        screen_width = screen["width"] + screen["x"]
        screen_height = screen["height"] + screen["y"]
        window_is_x_in_screen = screen["x"] < window_data["x"] + 1 < screen_width
        window_is_y_in_screen = screen["y"] < window_data["y"] + 1 < screen_height
        if window_is_y_in_screen and window_is_x_in_screen:
            return screen
