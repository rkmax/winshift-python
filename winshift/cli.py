import os
import argparse
import shutil
from typing import Optional

from winshift.modules.config import add_layout, add_bar_height, load_config, ConfigData
from winshift.modules.direction import Direction
from winshift.modules.icons import create_image
from winshift.modules.layout import calculate_layout_screen, Layout, BarHeight
from winshift.modules.screen import get_screens_data, locate_point_on_screen, ScreenData
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
        # list bar heights
        subparsers.add_parser("list-bar-heights", help="List bar heights")
        # add bar height
        add_bar_height_parser = subparsers.add_parser("add-bar-height", help="Add a new bar height")
        add_bar_height_parser.add_argument("--screen-name", type=str, help="Screen name (xrandr name)")
        add_bar_height_parser.add_argument("--left", type=int, nargs="?", default=0, help="Left bar height")
        add_bar_height_parser.add_argument("--right", type=int, nargs="?", default=0, help="Right bar height")
        add_bar_height_parser.add_argument("--top", type=int, nargs="?", default=0, help="Top bar height")
        add_bar_height_parser.add_argument("--bottom", type=int, nargs="?", default=0, help="Bottom bar height")
        # generate layout icons
        generate_layout_icons_parser = subparsers.add_parser("generate-layout-icons", help="Generate layout icons")
        generate_layout_icons_parser.add_argument("output_dir_path", type=str, help="Output directory path")
        generate_layout_icons_parser.add_argument(
            "--screen-color",
            type=str,
            nargs="?",
            default="#6699ff",
            help="Color used for the screen rectangle in the generated icons",
        )
        generate_layout_icons_parser.add_argument(
            "--screen-border-color",
            type=str,
            nargs="?",
            default="#b2b2b2",
            help="Color used for the screen rectangle border in the generated icons (default: #b2b2b2)",
        )
        generate_layout_icons_parser.add_argument(
            "--screen-border-width",
            type=int,
            nargs="?",
            default=0,
            help="Width used for the screen rectangle border in the generated icons (default: 0)",
        )
        generate_layout_icons_parser.add_argument(
            "--window-color",
            type=str,
            nargs="?",
            default="#003399",
            help="Color used for the window rectangle in the generated icons (default: #003399)",
        )
        generate_layout_icons_parser.add_argument(
            "--window-border-color",
            type=str,
            nargs="?",
            default="#b2b2b2",
            help="Color used for the window rectangle border in the generated icons (default: #b2b2b2)",
        )
        generate_layout_icons_parser.add_argument(
            "--window-border-width",
            type=int,
            nargs="?",
            default=1,
            help="Width used for the window rectangle border in the generated icons (default: 1)",
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
                add_layout(
                    Layout(
                        name=args.layout_name,
                        layout=args.layout_str,
                        direction=Direction(args.direction),
                    )
                )
            elif args.command == "list-bar-heights":
                self.list_bar_heights()
            elif args.command == "add-bar-height":
                add_bar_height(
                    BarHeight(
                        screen_name=args.screen_name,
                        top=args.top,
                        bottom=args.bottom,
                        right=args.right,
                        left=args.left,
                    )
                )
            elif args.command == "generate-layout-icons":
                self.generate_layout_icons(
                    args.output_dir_path,
                    args.screen_color,
                    args.screen_border_color,
                    args.screen_border_width,
                    args.window_color,
                    args.window_border_color,
                    args.window_border_width,
                )
            else:
                self.parser.print_help()
        except Exception as e:
            print(e)
            self.parser.print_help()

    def list_layouts(self) -> None:
        for direction in [Direction.HORIZONTAL, Direction.VERTICAL]:
            dir_layouts = []
            max_layout_name_len = 0
            for layout in self.config.layouts:
                if layout.direction == direction:
                    dir_layouts.append(layout)
                    max_layout_name_len = max(max_layout_name_len, len(layout.name))
            if dir_layouts:
                print(f"layouts {direction.value} screens:")
                for layout in dir_layouts:
                    print(f"  {layout.name.ljust(max_layout_name_len)} \t {layout.layout}")

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
            (
                layout_listed
                for layout_listed in self.config.layouts
                if layout_listed.name == layout_name and layout_listed.direction == target_screen.direction
            ),
            None,
        )

        if not layout:
            raise RuntimeError(f"Layout {layout_name} not found for {target_screen.direction}")

        bar_height = next(
            (
                bar_height_listed
                for bar_height_listed in self.config.bar_heights
                if bar_height_listed.screen_name == target_screen.name
            ),
            None,
        )

        new_window_layout = calculate_layout_screen(target_screen, layout, bar_height)
        print(f'Screen "{target_screen}"')
        print(f'Layout "{layout.layout}" applied to screen "{target_screen.name}"')
        print(f'Bar height "{bar_height}" applied to screen "{target_screen.name}"')
        print(f'Window "{window_data}"')

        if dry_run:
            print(f"Dry run, calculated window layout: {new_window_layout}")
        else:
            resize_reposition_window(window_data, new_window_layout)
            print(f"Window resized and repositioned {new_window_layout}")

    def list_bar_heights(self) -> None:
        for bar_height in self.config.bar_heights:
            print(f"{bar_height}")

    def generate_layout_icons(
        self,
        output_dir_path: str,
        screen_color: str,
        screen_border_color: str,
        screen_border_width: int,
        window_color: str,
        window_border_color: str,
        window_border_width: int,
    ) -> None:
        screens_data = get_screens_data()
        if not screens_data:
            raise RuntimeError("No screens found")
        screen_width = screens_data[0].width
        screen_height = screens_data[0].height
        screen_direction = screens_data[0].direction

        for layout in self.config.layouts:
            screen_data = ScreenData(
                name="",
                x=0,
                y=0,
                width=screen_width if layout.direction == screen_direction else screen_height,
                height=screen_height if layout.direction == screen_direction else screen_width,
                direction=layout.direction,
            )

            output_path = os.path.join(output_dir_path, f"{layout.direction.value}-{layout.name}.png")
            window = calculate_layout_screen(screen_data, layout)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            create_image(
                image_size=72,
                margin=6,
                screen_dims=(screen_data.width, screen_data.height),
                window_dims=(window.x, window.y, window.width, window.height),
                output_path=output_path,
                screen_color=screen_color,
                screen_border_color=screen_border_color,
                screen_border_width=screen_border_width,
                window_color=window_color,
                window_border_color=window_border_color,
                window_border_width=window_border_width,
            )
            print(f"Created {output_path}")


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
