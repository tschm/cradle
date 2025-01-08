#    Copyright 2023 Stanford University Convex Optimization Group
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import fire  # type: ignore
import requests  # type: ignore


def cli(metric: str, latitude: float = 37.4419, longitude: float = -122.143) -> None:
    """
    Get the current weather for a given metric

    Parameters
    ----------
    metric : str
        The metric to get the current weather for.
        Use time, temperature, windspeed, winddirection or weathercode
        For details: https://open-meteo.com/en/docs
    latitude : float, optional
        The latitude to get the current weather for, by default 37.4419
    longitude : float, optional
        The longitude to get the current weather for, by default -122.143
    """
    url = "https://api.open-meteo.com/v1/forecast"
    url = f"{url}?latitude={str(latitude)}&longitude={str(longitude)}&current_weather=true"
    r = requests.get(url)

    if r.status_code == 200:
        if metric in r.json()["current_weather"]:
            x = r.json()["current_weather"][metric]
            return x
        else:
            raise ValueError("Metric not supported!")
    else:
        raise ConnectionError("Open-Meteo is down!")


def main():  # pragma: no cover
    """
    Run the CLI using Fire
    """
    fire.Fire(cli)
