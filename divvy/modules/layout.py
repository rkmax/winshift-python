from dataclasses import asdict

from divvy.modules.screen import ScreenData

SCREEN_LAYOUT = {
    "horizontal": {
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
    "vertical": {
        "full-size": "0,0,{width},{height}",
        "half-top": "0,0,{width},{height}/2",
        "half-bottom": "0,{height}/2,{width},{height}/2",
        "first-quarter": "0,0,{width},{height}/4",
        "second-quarter": "0,{height}/4,{width},{height}/4",
        "third-quarter": "0,{height}/2,{width},{height}/4",
        "fourth-quarter": "0,{height}*3/4,{width},{height}/4",
    },
}

# Some screens have a bar at the top or bottom
# define the screen name and where to put space for the bar
BAR_HEIGHT = {
    "DP-0": {  # ✋ Change this to match your screen name
        "top": 0,
        "bottom": 0,  # ✋ Change this t match you bar height
        "left": 0,
        "right": 0,
    }
}


def calculate_layout_screen(screen_data: ScreenData, layout_name: str) -> dict:
    screen_data = asdict(screen_data)
    """Return the layout of the screen."""
    if screen_data["name"] in BAR_HEIGHT:
        bar = BAR_HEIGHT[screen_data["name"]]
        screen_data["x"] += bar["left"]
        screen_data["y"] += bar["top"]
        screen_data["width"] -= bar["left"] + bar["right"]
        screen_data["height"] -= bar["top"] + bar["bottom"]

    calc_layout = SCREEN_LAYOUT[screen_data["layout"]][layout_name].format(
        **screen_data
    )

    return {
        "x": eval(calc_layout.split(",")[0]) + screen_data["x"],
        "y": eval(calc_layout.split(",")[1]) + screen_data["y"],
        "width": eval(calc_layout.split(",")[2]),
        "height": eval(calc_layout.split(",")[3]),
    }
