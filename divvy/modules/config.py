import os

import toml
from divvy.modules.layout import LayoutData, validate_layout


def load_layouts(config_path: str) -> LayoutData:
    """Load the layouts from the config file."""
    with open(config_path) as f:
        config = toml.load(f)

    return LayoutData(
        horizontal=config["horizontal"],
        vertical=config["vertical"],
    )


def _ensure_config_file_exists(config_path: str) -> None:
    """Create the config file if it doesn't exist."""
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            toml.dump({}, f)


def add_layout(config_path: str, layout_name: str, layout_str: str, direction: str) -> None:
    """Add a new layout to the config file."""
    validate_layout(layout_str)
    _ensure_config_file_exists(config_path)

    with open(config_path) as f:
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

    with open(config_path, "w") as f:
        toml.dump(config, f)