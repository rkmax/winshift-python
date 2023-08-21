import argparse
import shutil
from typing import Optional

from divvy.modules.layout import calculate_layout_screen, DEFAULT_LAYOUTS_DATA
from divvy.modules.screen import get_screens_data, locate_point_on_screen, ScreenData
from divvy.modules.window import get_active_window_data, resize_reposition_window


def _check_external_dependencies():
    _check_external_dependency("xrandr")
    _check_external_dependency("xprop")


def _check_external_dependency(name: str):
    """Check if an external dependency (command) is installed."""
    if shutil.which(name) is None:
        raise RuntimeError(f"{name} is not installed")


def main():
    parser = argparse.ArgumentParser(description="Divvy")

    parser.add_argument("layout_name", type=str, help="Name of the layout to use")
    parser.add_argument(
        "screen_name",
        type=str,
        nargs="?",
        default=None,
        help="Name of the screen to use (optional). if not provided, screen will be chosen automatically",
    )

    args = parser.parse_args()
    window_data = get_active_window_data()
    screens_data = get_screens_data()

    if args.screen_name:
        target_screen = next(
            (screen for screen in screens_data if screen.name == args.screen_name), None
        )
    else:
        target_screen = locate_point_on_screen(screens_data, window_data.x, window_data.y)

    if target_screen is None:
        raise RuntimeError(f"Screen {args.screen_name} not found")

    if args.layout_name in DEFAULT_LAYOUTS_DATA.horizontal:
        layout_str = DEFAULT_LAYOUTS_DATA.horizontal[args.layout_name]
    elif args.layout_name in DEFAULT_LAYOUTS_DATA.vertical:
        layout_str = DEFAULT_LAYOUTS_DATA.vertical[args.layout_name]
    else:
        raise RuntimeError(f"Layout {args.layout_name} not found for {target_screen.layout}")

    new_window_layout = calculate_layout_screen(target_screen, layout_str)
    resize_reposition_window(window_data, new_window_layout)
    print('Screen "{}"'.format(target_screen))
    print('Layout "{}" applied to screen "{}"'.format(layout_str, target_screen.name))
    print('Window resized and repositioned {}'.format(new_window_layout))


if __name__ == "__main__":
    _check_external_dependencies()
    main()
