import subprocess


def get_active_window_data():
    """Return active window data using xdotool."""
    xdotool = subprocess.Popen(
        ["xdotool", "getactivewindow", "getwindowgeometry"], stdout=subprocess.PIPE
    )
    window_info = xdotool.stdout.read().decode("utf-8").split("\n")
    name = window_info[0].split(" ")[1]
    x = int(window_info[1].split()[1].split(",")[0])
    y = int(window_info[1].split()[1].split(",")[1])
    width = int(window_info[2].split()[1].split("x")[0])
    height = int(window_info[2].split()[1].split("x")[1])
    return {
        "name": name,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
    }


def resize_reposition_window(window_data, layout_data):
    """Resize and reposition the window."""
    subprocess.call(
        [
            "xdotool",
            "windowsize",
            window_data["name"],
            str(layout_data["width"]),
            str(layout_data["height"]),
        ]
    )
    subprocess.call(
        [
            "xdotool",
            "windowmove",
            window_data["name"],
            str(layout_data["x"]),
            str(layout_data["y"]),
        ]
    )
