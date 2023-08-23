import argparse
import os
import shutil
from typing import Optional

from winshift.modules.config import add_layout, DEFAULT_CONFIG
from winshift.modules.layout import calculate_layout_screen
from winshift.modules.screen import get_screens_data, locate_point_on_screen
from winshift.modules.window import get_active_window_data, resize_reposition_window


class AppCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Divvy")
        subparsers = self.parser.add_subparsers(dest="command")
        # list_layouts_parser
        subparsers.add_parser("list-layouts", help="List available layouts")
        # change_layout_parser
        change_layout_parser = subparsers.add_parser("change-layout", help="Change layout")
        change_layout_parser.add_argument('--dry-run', action='store_true', help='Do not change layout')
        change_layout_parser.add_argument(
            "layout_name",
            type=str,
            help="Name of the layout to use"
        )
        change_layout_parser.add_argument(
            "--screen-name",
            type=str,
            nargs="?",
            default=None,
            help="Name of the screen to use (optional). if not provided, screen will be chosen automatically",
        )
        # add_layout_parser
        add_layout_parser = subparsers.add_parser("add-layout", help="Add a new layout")
        add_layout_parser.add_argument("--direction", type=str, help="horizontal layout")
        add_layout_parser.add_argument("layout_name", type=str, help="Name of the layout")
        add_layout_parser.add_argument(
            'layout_str',
            type=str,
            help="layout string in the format ({x},{y},{width},{height})"
        )

    def run(self):
        try:
            args = self.parser.parse_args()
            if args.command == "list-layouts":
                self.list_layouts()
            elif args.command == "change-layout":
                self.change_layout(args.layout_name, args.screen_name, args.dry_run)
            elif args.command == "add-layout":
                self.add_layout(args.layout_name, args.layout_str, args.direction)
        except Exception as e:
            print(e)
            self.parser.print_help()

    @staticmethod
    def list_layouts() -> None:
        print("horizontal layouts:")
        for layout in DEFAULT_CONFIG.layouts:
            if layout.direction == "horizontal":
                print(f"  {layout.name}")
        print("vertical layouts:")
        for layout in DEFAULT_CONFIG.layouts:
            if layout.direction == "vertical":
                print(f"  {layout.name}")

    @staticmethod
    def change_layout(layout_name: str, screen_name: Optional[str] = None, dry_run: bool = False) -> None:
        window_data = get_active_window_data()
        screens_data = get_screens_data()

        if screen_name:
            target_screen = next(
                (screen for screen in screens_data if screen.name == screen_name), None
            )
        else:
            target_screen = locate_point_on_screen(screens_data, window_data.x, window_data.y)

        if target_screen is None:
            raise RuntimeError(f"Screen {screen_name} not found")

        layout = next(l for l in DEFAULT_CONFIG.layouts if l.name == layout_name and l.direction == target_screen.direction)

        if not layout:
            raise RuntimeError(f"Layout {layout_name} not found for {target_screen.direction}")

        new_window_layout = calculate_layout_screen(target_screen, layout)
        print('Screen "{}"'.format(target_screen))
        print('Layout "{}" applied to screen "{}"'.format(layout.layout, target_screen.name))
        print('Window "{}"'.format(window_data))

        if dry_run:
            print('Dry run, calculated window layout: {}'.format(new_window_layout))
        else:
            resize_reposition_window(window_data, new_window_layout)
            print('Window resized and repositioned {}'.format(new_window_layout))

    def add_layout(self, layout_name: str, layout_str: str, direction: str) -> None:
        add_layout(self._get_config_path(), layout_name, layout_str, direction)

    @staticmethod
    def _get_config_path():
        return os.path.expanduser("~/.config/winshift/config.toml")


def _check_external_dependencies() -> None:
    _check_external_dependency("xrandr")
    _check_external_dependency("xprop")


def _check_external_dependency(name: str) -> None:
    """Check if an external dependency (command) is installed."""
    if shutil.which(name) is None:
        raise RuntimeError(f"{name} is not installed")


def main() -> None:
    app = AppCLI()
    app.run()


if __name__ == "__main__":
    _check_external_dependencies()
    main()
