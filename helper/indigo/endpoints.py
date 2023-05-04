from typing import Final

API_ENDPOINT: Final[str] = "https://analytics.indigoprotocol.io/api"
STABILITY_POOLS_ENDPOINT: Final[
    str
] = f"{API_ENDPOINT}/stability-pools-accounts"
STAKING_POOLS_STATE_ENDPOINT: Final[str] = f"{API_ENDPOINT}/stability-pools"
STAKING_POSITIONS_ENDPOINT: Final[str] = f"{API_ENDPOINT}/staking-positions"
