from dataclasses import dataclass
from decimal import ROUND_DOWN, Decimal
from typing import Any, Dict, Iterable, List, Type

import requests

from .. import cardano
from .endpoints import STABILITY_POOLS_ENDPOINT, STAKING_POOLS_STATE_ENDPOINT


@dataclass
class StabilityAccount:
    _positions: List[Dict[str, Any]]
    _pools: List[Dict[str, Any]]

    @property
    def iassets(self) -> Iterable[str]:
        return set((position["asset"] for position in self._positions))

    @property
    def balances(self) -> Dict[str, Decimal]:
        return {iasset: self.get_balance(iasset) for iasset in self.iassets}

    def get_balance(self, iasset: str) -> Decimal:
        account = next(
            (
                position
                for position in self._positions
                if position["asset"] == iasset
            )
        )
        a = Decimal(account["snapshotD"])
        b = Decimal(account["snapshotP"])
        c = Decimal(
            next(
                (
                    pool["snapshotP"]
                    for pool in self._pools
                    if pool["asset"] == iasset
                )
            )
        )

        m = a * c / b
        return (m / 10**24).quantize(Decimal(".000001"), rounding=ROUND_DOWN)

    @classmethod
    def find_account(
        cls: Type["StabilityAccount"], addresses: Iterable[str]
    ) -> "StabilityAccount":
        positions = requests.get(STABILITY_POOLS_ENDPOINT).json()
        spending_hashes = [
            cardano.get_spending_hash(address) for address in addresses
        ]

        return cls(
            [
                position
                for position in positions
                if position["owner"] in spending_hashes
            ],
            requests.get(STAKING_POOLS_STATE_ENDPOINT).json(),
        )
