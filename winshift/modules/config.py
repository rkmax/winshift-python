import os
from dataclasses import dataclass
from typing import List

import toml

from winshift.modules.direction import Direction
from winshift.modules.layout import LayoutData, validate_layout, BarHeight, Layout


@dataclass
class ConfigData:
    bar_height: List[BarHeight]
    layouts: List[Layout]


DEFAULT_CONFIG = ConfigData(
    bar_height=[
        BarHeight(top=0, bottom=45, left=0, right=0, screen_name="DP-0")
    ],
    layouts=[
        Layout(
            name="full-size",
            layout="0,0,{width},{height}",
            direction=Direction.HORIZONTAL,
        ),
        Layout(
            name="half-left",
            layout="0,0,{width}/2,{height}",
            direction=Direction.HORIZONTAL,
        ),
        Layout(
            name="half-right",
            layout="{width}/2,0,{width}/2,{height}",
            direction=Direction.HORIZONTAL,
        ),
    ]
)


def load_layouts(config_path: str) -> LayoutData:
    """Load the layouts from the config file."""
    with open(config_path, encoding='utf-8') as f:
        config = toml.load(f)

    return LayoutData(
        horizontal=config["horizontal"],
        vertical=config["vertical"],
    )


def _ensure_config_file_exists(config_path: str) -> None:
    """Create the config file if it doesn't exist."""
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w", encoding='utf-8') as f:
            toml.dump({}, f)


def add_layout(config_path: str, layout_name: str, layout_str: str, direction: str) -> None:
    """Add a new layout to the config file."""
    validate_layout(layout_str)
    _ensure_config_file_exists(config_path)

    with open(config_path, encoding='utf-8') as f:
        config = toml.load(f)

    if direction == "horizontal":
        if "horizontal" not in config:
            config["horizontal"] = {}
        config["horizontal"][layout_name] = layout_str
    elif direction == "vertical":
        if "vertical" not in config:
            config["vertical"] = {}
        config["vertical"][layout_name] = layout_str
    else:
        raise RuntimeError(f"Unknown direction {direction}")

    with open(config_path, "w", encoding='utf-8') as f:
        toml.dump(config, f)
