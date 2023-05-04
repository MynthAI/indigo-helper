import decimal
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Type

import requests

from .. import cardano
from .endpoints import STAKING_POSITIONS_ENDPOINT


@dataclass
class StakingAccount:
    account: str
    _position: Dict[str, Any]

    @property
    def balance(self) -> float:
        if not self._position:
            return 0

        return float(
            (
                decimal.Decimal(self._position["staked_indy"]) / 1000000
            ).quantize(decimal.Decimal(".000001"), rounding=decimal.ROUND_DOWN)
        )

    @classmethod
    def find_account(
        cls: Type["StakingAccount"], addresses: Iterable[str]
    ) -> "StakingAccount":
        accounts = {
            position["owner"]: position
            for position in requests.get(STAKING_POSITIONS_ENDPOINT).json()
        }

        for address in addresses:
            spending_hash = cardano.get_spending_hash(address)
            if spending_hash in accounts:
                return cls(spending_hash, accounts[spending_hash])

        return cls("", {})
