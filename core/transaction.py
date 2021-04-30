import json
from typing import Dict, List


class Investment(object):
    def __init__(self, fund) -> None:
        super().__init__()
        self.fund = fund
        self.transcations = self._load_transactions()

        self.units = sum(x['units'] for x in self.transcations)
        self.invested_amount = sum(x['price'] * x['units']
                                   for x in self.transcations)

    def _load_transactions(self) -> List[Dict]:
        with open("transactions.json", "r") as file:
            return json.load(file).get(self.fund, [])
