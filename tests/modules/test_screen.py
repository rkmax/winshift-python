from pytest_mock import MockFixture
from divvy.modules import screen
from divvy.modules.screen import ScreenData


def test_get_screens_data(mocker: MockFixture) -> None:
    mock_output = (
        "Monitors: 2\n"
        " 0: +*DP-0 3840/600x2160/340+2160+973  DP-0\n"
        " 1: +DP-2 2160/600x3840/340+0+0  DP-2\n"
    ).encode("utf-8")

    mock_process = mocker.Mock()
    mock_process.stdout.read.return_value = mock_output
    mocker.patch("subprocess.Popen", return_value=mock_process)

    result = screen.get_screens_data()

    expected = [
        ScreenData(
            name="DP-0",
            x=2160,
            y=973,
            width=3840,
            height=2160,
            layout="horizontal",
        ),
        ScreenData(
            name="DP-2",
            x=0,
            y=0,
            width=2160,
            height=3840,
            layout="vertical",
        ),
    ]

    assert result == expected
