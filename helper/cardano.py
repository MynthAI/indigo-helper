import json
import os
import subprocess

from blockfrost import BlockFrostApi  # type: ignore


def get_stake_address(payment_address: str) -> str:
    bech32_stake_address = (
        "e1"
        + subprocess.run(
            ["bech32"],
            stdout=subprocess.PIPE,
            input=payment_address.strip() + "\n",
            encoding="ascii",
        ).stdout.strip()[-56:]
    )

    return subprocess.run(
        ["bech32", "stake"],
        stdout=subprocess.PIPE,
        input=bech32_stake_address + "\n",
        encoding="ascii",
    ).stdout.strip()


def get_addresses(stake_address: str) -> list[str]:
    api = BlockFrostApi(os.environ["BLOCKFROST_API_KEY"])
    return [a.address for a in api.account_addresses(stake_address)]


def get_spending_hash(address: str) -> str:
    result = subprocess.run(
        ["cardano-address", "address", "inspect"],
        stdout=subprocess.PIPE,
        input=address + "\n",
        encoding="ascii",
    ).stdout.strip()
    return json.loads(result)["spending_key_hash"]
