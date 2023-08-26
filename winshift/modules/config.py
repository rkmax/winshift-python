import os
from dataclasses import dataclass
from typing import List

import toml

from winshift.modules.direction import Direction
from winshift.modules.layout import validate_layout, BarHeight, Layout




@dataclass
class ConfigData:
    bar_heights: List[BarHeight]
    layouts: List[Layout]

    def as_dict(self) -> dict:
        return {
            "bar_heights": {b.screen_name: _bar_height_as_dict(b) for b in self.bar_heights},
            "layouts": {layout.name: _layout_as_dict(layout) for layout in self.layouts},
        }

    @staticmethod
    def from_dict(data: dict) -> 'ConfigData':
        if 'bar_heights' not in data:
            data['bar_heights'] = {}
        if 'layouts' not in data:
            data['layouts'] = {}
        return ConfigData(
            bar_heights=[_bar_height_from_dict(b) for b in data["bar_heights"].values()],
            layouts=[_layout_from_dict(l) for l in data["layouts"].values()],
        )


def _bar_height_as_dict(bar_height: BarHeight) -> dict:
    return {
        "screen_name": bar_height.screen_name,
        "top": bar_height.top,
        "bottom": bar_height.bottom,
        "right": bar_height.right,
        "left": bar_height.left,
    }


def _bar_height_from_dict(data: dict) -> BarHeight:
    return BarHeight(
        screen_name=data["screen_name"],
        top=data["top"],
        bottom=data["bottom"],
        right=data["right"],
        left=data["left"],
    )


def _layout_as_dict(layout: Layout) -> dict:
    return {
        "name": layout.name,
        "layout": layout.layout,
        "direction": layout.direction.value,
    }


def _layout_from_dict(data: dict) -> Layout:
    return Layout(
        name=data["name"],
        layout=data["layout"],
        direction=Direction(data["direction"]),
    )


DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/winshift/config.toml")
DEFAULT_CONFIG = ConfigData(
    bar_heights=[],
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
    ],
)


def _write_config(config_path: str, config: ConfigData) -> None:
    """Create the config file if it doesn't exist."""
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        toml.dump(config.as_dict(), f)


def _read_config(config_path: str) -> ConfigData:
    """Read the config file."""
    if not os.path.exists(config_path):
        return ConfigData(
            bar_heights=[],
            layouts=[],
        )
    with open(config_path, encoding="utf-8") as f:
        return ConfigData.from_dict(toml.load(f))


def load_config() -> ConfigData:
    """Load the config file, user config overrides default."""
    config = _read_config(DEFAULT_CONFIG_PATH)

    user_config_layouts = [l.name for l in config.layouts]
    default_layouts = [l for l in DEFAULT_CONFIG.layouts if l.name not in user_config_layouts]
    config.layouts.extend(default_layouts)

    user_config_bar_heights = [b.screen_name for b in config.bar_heights]
    default_bar_heights = [b for b in DEFAULT_CONFIG.bar_heights if b.screen_name not in user_config_bar_heights]
    config.bar_heights.extend(default_bar_heights)

    return config


def add_layout(layout: Layout) -> None:
    """Add a new layout to the config file."""
    validate_layout(layout.layout)
    config = _read_config(DEFAULT_CONFIG_PATH)
    config.layouts.append(layout)
    _write_config(DEFAULT_CONFIG_PATH, config)


def add_bar_height(bar_height: BarHeight) -> None:
    """Add a new bar height to the config file."""
    config = _read_config(DEFAULT_CONFIG_PATH)
    config.bar_heights.append(bar_height)
    _write_config(DEFAULT_CONFIG_PATH, config)