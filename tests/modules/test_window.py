from pytest_mock import MockFixture

from winshift.modules import window
from winshift.modules.window import WindowData


def test_get_active_window_data(mocker: MockFixture) -> None:
    mock_output = "Window 123731979\n" "  Position: 3953,1833 (screen: 0)\n" "  Geometry: 2160x960\n".encode("utf-8")

    mock_process = mocker.MagicMock()
    mock_process.__enter__.return_value.stdout.read.return_value = mock_output
    mocker.patch("subprocess.Popen", return_value=mock_process)

    result = window.get_active_window_data()

    expected = WindowData(name="123731979", x=3953, y=1833, width=2160, height=960)

    assert result == expected
