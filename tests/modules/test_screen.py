import pytest
from pytest_mock import MockFixture
from winshift.modules import screen
from winshift.modules.direction import Direction
from winshift.modules.screen import ScreenData


def test_get_screens_data(mocker: MockFixture) -> None:
    mock_output = (
        "Monitors: 2\n" " 0: +*DP-0 3840/600x2160/340+2160+973  DP-0\n" " 1: +DP-2 2160/600x3840/340+0+0  DP-2\n"
    ).encode("utf-8")

    mock_process = mocker.MagicMock()
    mock_process.__enter__.return_value.stdout.read.return_value = mock_output

    mocker.patch("subprocess.Popen", return_value=mock_process)

    result = screen.get_screens_data()

    expected = [
        ScreenData(
            name="DP-0",
            x=2160,
            y=973,
            width=3840,
            height=2160,
            direction=Direction.HORIZONTAL,
        ),
        ScreenData(
            name="DP-2",
            x=0,
            y=0,
            width=2160,
            height=3840,
            direction=Direction.VERTICAL,
        ),
    ]

    assert result == expected


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (3840, 0, "DP-0"),
        (2160, 973, "DP-0"),
        (49, 1093, "DP-2"),
        (2160, 2031, "DP-0"),
    ],
)
def test_locate_point_on_screen(x: int, y: int, expected: str) -> None:
    screens = [
        ScreenData(
            name="DP-0",
            x=2160,
            y=973,
            width=3840,
            height=2160,
            direction=Direction.HORIZONTAL,
        ),
        ScreenData(
            name="DP-2",
            x=0,
            y=0,
            width=2160,
            height=3840,
            direction=Direction.VERTICAL,
        ),
    ]

    result = screen.locate_point_on_screen(screens, x, y)

    assert result.name == expected
