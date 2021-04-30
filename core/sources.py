from abc import ABC
from typing import List
import requests
from collections import namedtuple
from datetime import date, datetime


class Simfonia:
    NAME = 'simfonia'
    URL = 'https://brdam.ro/assets/json/istorics.json'


class Diverso:
    NAME = 'diverso'
    URL = 'https://brdam.ro/assets/json/istoricd.json'


class Source(ABC):
    def __init__(self) -> None:
        super().__init__()

    def get_data(self):
        pass


Point = namedtuple('Point', ['date', 'value'])


class BRDSource(Source):
    def __init__(self, name, url) -> None:
        super().__init__()
        self.name = name
        self.url = url

    def get_data(self) -> List[Point]:
        r = requests.get(self.url)
        if r.status_code != 200:
            return None

        self.data = [Point(datetime.strptime(d['Data'], '%Y-%m-%d').date(),
                      float(d['VUAN'])) for d in r.json()]

        return self.data

