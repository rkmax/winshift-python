import subprocess
from dataclasses import dataclass
from typing import List

from divvy.modules.layout import CalculatedLayout


@dataclass
class WindowData:
    name: str
    x: int
    y: int
    width: int
    height: int


def _parse_window_data(window_data: List[str]) -> WindowData:
    """Return window data from xdotool output."""
    name = window_data[0].split(" ")[1]
    x = int(window_data[1].split()[1].split(",")[0])
    y = int(window_data[1].split()[1].split(",")[1])
    width = int(window_data[2].split()[1].split("x")[0])
    height = int(window_data[2].split()[1].split("x")[1])
    return WindowData(name, x, y, width, height)


def get_active_window_data():
    """Return active window data using xdotool."""
    xdotool = subprocess.Popen(
        ["xdotool", "getactivewindow", "getwindowgeometry"], stdout=subprocess.PIPE
    )
    window_info = xdotool.stdout.read().decode("utf-8").split("\n")
    return _parse_window_data(window_info)


def resize_reposition_window(window_data: WindowData, layout_data: CalculatedLayout):
    """Resize and reposition the window."""
    subprocess.call(
        [
            "xdotool",
            "windowsize",
            window_data.name,
            str(layout_data.width),
            str(layout_data.height),
        ]
    )
    subprocess.call(
        [
            "xdotool",
            "windowmove",
            window_data.name,
            str(layout_data.x),
            str(layout_data.y),
        ]
    )
