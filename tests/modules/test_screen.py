from pytest_mock import MockFixture
from divvy.modules import screen


def test_get_screens_data(mocker: MockFixture) -> None:
    mock_output = (
        "Monitors: 2\n"
        " 0: +*DP-2 1920/509x1080/286+0+0  DP-2\n"
        " 1: +DP-1 1920/509x1080/286+1920+0  DP-1\n"
    ).encode("utf-8")

    mock_process = mocker.Mock()
    mock_process.stdout.read.return_value = mock_output
    mocker.patch("subprocess.Popen", return_value=mock_process)

    result = screen.get_screens_data()

    expected = [
        {
            "name": "DP-2",
            "x": 0,
            "y": 0,
            "width": 1920,
            "height": 1080,
            "layout": "horizontal",
        },
        {
            "name": "DP-1",
            "x": 1920,
            "y": 0,
            "width": 1920,
            "height": 1080,
            "layout": "horizontal",
        },
    ]

    assert result == expected
