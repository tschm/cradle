from unittest import mock

import pytest

from cvx.cli.weather import cli


def test_weather():
    temperature = cli(metric="temperature")
    print(temperature)
    assert isinstance(temperature, float)
    assert temperature > -50
    assert temperature < 50


def test_missing_metric():
    with pytest.raises(ValueError):
        cli(metric="maffay")


def test_server_down():
    with mock.patch("requests.get", return_value=mock.Mock(status_code=500)):
        with pytest.raises(ConnectionError):
            cli("temperature")
