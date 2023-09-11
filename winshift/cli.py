import argparse
import shutil
from typing import Optional

from winshift.modules.config import add_layout, load_config, ConfigData
from winshift.modules.direction import Direction
from winshift.modules.layout import calculate_layout_screen, Layout
from winshift.modules.screen import get_screens_data, locate_point_on_screen
from winshift.modules.window import get_active_window_data, resize_reposition_window


class AppCLI:
    config: ConfigData

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Divvy")
        subparsers = self.parser.add_subparsers(dest="command")
        # list_layouts_parser
        subparsers.add_parser("list-layouts", help="List available layouts")
        # change_layout_parser
        change_layout_parser = subparsers.add_parser("change-layout", help="Change layout")
        change_layout_parser.add_argument("--dry-run", action="store_true", help="Do not change layout")
        change_layout_parser.add_argument("layout_name", type=str, help="Name of the layout to use")
        change_layout_parser.add_argument(
            "--screen-name",
            type=str,
            nargs="?",
            default=None,
            help="Name of the screen to use (optional). if not provided, screen will be chosen automatically",
        )
        # add_layout_parser
        add_layout_parser = subparsers.add_parser("add-layout", help="Add a new layout")
        add_layout_parser.add_argument("--direction", type=str, help="Screen direction (horizontal or vertical)")
        add_layout_parser.add_argument("layout_name", type=str, help="Name of the layout")
        add_layout_parser.add_argument(
            "layout_str",
            type=str,
            help="layout string in the format ({x},{y},{width},{height})",
        )

    def run(self):
        try:
            args = self.parser.parse_args()
            self.config = load_config()
            if args.command == "list-layouts":
                self.list_layouts()
            elif args.command == "change-layout":
                self.change_layout(args.layout_name, args.screen_name, args.dry_run)
            elif args.command == "add-layout":
                add_layout(Layout(
                    name=args.layout_name,
                    layout=args.layout_str,
                    direction=Direction(args.direction),
                ))
            else:
                self.parser.print_help()
        except Exception as e:
            print(e)
            self.parser.print_help()

    def list_layouts(self) -> None:
        for direction in [Direction.HORIZONTAL, Direction.VERTICAL]:
            dir_layouts = []
            for layout in self.config.layouts:
                if layout.direction == direction:
                    dir_layouts.append(layout)
            if dir_layouts:
                print(f"layouts {direction.value} screens:")
                for layout in dir_layouts:
                    print(f"  {layout.name}")

    def change_layout(self, layout_name: str, screen_name: Optional[str] = None, dry_run: bool = False) -> None:
        window_data = get_active_window_data()
        screens_data = get_screens_data()

        if screen_name:
            target_screen = next((screen for screen in screens_data if screen.name == screen_name), None)
        else:
            target_screen = locate_point_on_screen(screens_data, window_data.x, window_data.y)

        if target_screen is None:
            raise RuntimeError(f"Screen {screen_name} not found")

        layout = next(
            layout_listed
            for layout_listed in self.config.layouts
            if layout_listed.name == layout_name and layout_listed.direction == target_screen.direction
        )

        if not layout:
            raise RuntimeError(f"Layout {layout_name} not found for {target_screen.direction}")

        new_window_layout = calculate_layout_screen(target_screen, layout)
        print(f'Screen "{target_screen}"')
        print(f'Layout "{layout.layout}" applied to screen "{target_screen.name}"')
        print(f'Window "{window_data}"')

        if dry_run:
            print(f"Dry run, calculated window layout: {new_window_layout}")
        else:
            resize_reposition_window(window_data, new_window_layout)
            print(f"Window resized and repositioned {new_window_layout}")


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
