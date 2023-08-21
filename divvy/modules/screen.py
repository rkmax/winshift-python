import subprocess

from divvy.modules.layout import get_screen_layout


def _get_screen_data_map(monitoring_data):
    """Return a dictionary of screen data."""
    info = {
        "name": monitoring_data[3],
        "x": int(monitoring_data[2].split("+")[1]),
        "y": int(monitoring_data[2].split("+")[2]),
        "width": int(monitoring_data[2].split("+")[0].split("x")[0].split("/")[0]),
        "height": int(monitoring_data[2].split("+")[0].split("x")[1].split("/")[0]),
    }

    info["layout"] = get_screen_layout(info)
    return info


def get_screens_data():
    """Return screen data using xrandr."""
    xrandr = subprocess.Popen(
        ["xrandr", "--listactivemonitors"], stdout=subprocess.PIPE
    )
    monitors = xrandr.stdout.read().decode("utf-8").split("\n")[1:-1]
    return [_get_screen_data_map(monitor.split()) for monitor in monitors]


def get_screen_of_window(screens_data, window_data):
    """Return the screen where the window is located using x,y of the window."""
    for screen in screens_data:
        screen_width = screen["width"] + screen["x"]
        screen_height = screen["height"] + screen["y"]
        window_is_x_in_screen = screen["x"] < window_data["x"] + 1 < screen_width
        window_is_y_in_screen = screen["y"] < window_data["y"] + 1 < screen_height
        if window_is_y_in_screen and window_is_x_in_screen:
            return screen
