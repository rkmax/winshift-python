import pytest
from pytest_mock import MockFixture

from winshift.modules import config
from winshift.modules.config import ConfigData
from winshift.modules.direction import Direction
from winshift.modules.layout import Layout


@pytest.mark.parametrize(
    "config_str, path_exists, expected",
    [
        (
            # no config content, use default config
             '[bar_heights]\n\n[layouts]\n',
            True,
            config.DEFAULT_CONFIG
        ),
        (
            # no file exists, use default config
            '[layouts.centered-left]\n'
            'name = "centered-left"\n'
            'layout = "100,{height}*1/6,{width}*3/5,{height}*2/3"\n'
            'direction = "horizontal"',
            False,
            config.DEFAULT_CONFIG
        ),
        (
            # file exists, use default config + config file
            '[layouts.centered-left]\n'
            'name = "centered-left"\n'
            'layout = "100,{height}*1/6,{width}*3/5,{height}*2/3"\n'
            'direction = "horizontal"',
            True,
            ConfigData(
                bar_heights=[],
                layouts=[Layout(
                    name="centered-left",
                    layout="100,{height}*1/6,{width}*3/5,{height}*2/3",
                    direction=Direction.HORIZONTAL,
                )] + config.DEFAULT_CONFIG.layouts
            )
        ),
        (
            # override default config when name is the same
            '[layouts.full-size]\n'
            'name = "full-size"\n'
            'layout = "0,0,{width},{height}"\n'
            'direction = "horizontal"',
            True,
            ConfigData(
                bar_heights=[],
                layouts=config.DEFAULT_CONFIG.layouts
            )
        )
    ]
)
def test_load_config(mocker: MockFixture, config_str: str, path_exists: bool, expected: ConfigData) -> None:
    mock_open = mocker.mock_open(read_data=config_str)
    mocker.patch('builtins.open', mock_open)
    mocker.patch('os.path.exists', return_value=path_exists)

    result = config.load_config()

    if path_exists:
        mock_open.assert_called_once_with(config.DEFAULT_CONFIG_PATH, encoding='utf-8')
    assert result == expected
