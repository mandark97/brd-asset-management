from typing import NamedTuple


class Plot(NamedTuple):
    max_pixels: int
    start_color: str
    end_color: str


class Portfolio(NamedTuple):
    name: str
    data: list
    gain: int
    max_gain: int
    latest_date: str
    plot: Plot
