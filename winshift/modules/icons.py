from typing import Tuple
from PIL import Image, ImageDraw


def create_image(
    image_size: int,
    margin: int,
    screen_dims: Tuple[int, int],
    window_dims: Tuple[int, int, int, int],
    output_path: str,
    screen_color: str,
    screen_border_color: str,
    screen_border_width: int,
    window_color: str,
    window_border_color: str,
    window_border_width: int,
) -> None:
    """
    Creates an image with two rectangles following specified conditions and saves it.

    :param image_size: Side length of the image
    :param margin: Margin around the image
    :param screen_dims: Dimensions of the first rectangle (width, height)
    :param window_dims: Dimensions of the second rectangle (x offset, y offset, width, height)
    :param output_path: Path to save the output image
    :param screen_color: Fill color for the first rectangle
    :param screen_border_color: Border color for the first rectangle
    :param screen_border_width: Border width for the first rectangle
    :param window_color: Fill color for the second rectangle
    :param window_border_color: Border color for the second rectangle
    :param window_border_width: Border width for the second rectangle
    """
    # Create a new image with transparency
    img = Image.new("RGBA", (image_size, image_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Adjust the image size for the margin
    image_size_adjusted = image_size - 2 * margin

    # Find the scale factor to fit the larger rectangle within the N x N image_size
    scale_factor = min(image_size_adjusted / screen_dims[0], image_size_adjusted / screen_dims[1])

    # Scale the dimensions of the rectangles
    screen_dims = tuple(int(d * scale_factor) for d in screen_dims)
    window_dims = (
        int(window_dims[0] * scale_factor),
        int(window_dims[1] * scale_factor),
        int(window_dims[2] * scale_factor),
        int(window_dims[3] * scale_factor),
    )

    # Draw the first rectangle centered
    screen_x: float = margin + (image_size_adjusted - screen_dims[0]) // 2
    screen_y: float = margin + (image_size_adjusted - screen_dims[1]) // 2
    screen_width: float = screen_x + screen_dims[0]
    screen_height: float = screen_y + screen_dims[1]
    draw.rectangle(
        (screen_x, screen_y, screen_width, screen_height),
        outline=screen_border_color,
        width=screen_border_width,
        fill=screen_color,
    )

    # Draw the second rectangle with the offset added to the origin point and with a border
    window_x: float = screen_x + window_dims[0]
    window_y: float = screen_y + window_dims[1]
    window_width: float = window_x + window_dims[2]
    window_height: float = window_y + window_dims[3]
    draw.rectangle(
        (window_x, window_y, window_width, window_height),
        outline=window_border_color,
        width=window_border_width,
        fill=window_color,
    )

    # Save the image
    img.save(output_path, "PNG")
