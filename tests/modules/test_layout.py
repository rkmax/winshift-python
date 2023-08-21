from divvy.modules import layout


def test_get_screen_layout():
    screen_data = {"width": 1920, "height": 1080}
    assert layout.get_screen_layout(screen_data) == "horizontal"

    screen_data = {"width": 1080, "height": 1920}
    assert layout.get_screen_layout(screen_data) == "vertical"
