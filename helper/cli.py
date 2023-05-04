import click

from . import cardano, indigo


@click.group()
def indy() -> None:
    pass


@indy.group()
def staking() -> None:
    pass


@indy.group()
def stability() -> None:
    pass


@staking.command(name="account")
@click.argument("address")
def staking_account(address: str) -> None:
    stake_address = cardano.get_stake_address(address)
    addresses = cardano.get_addresses(stake_address)

    account = indigo.StakingAccount.find_account(addresses)
    if account.account:
        print(f"{account.account}: {account.balance}")

    else:
        print(f"{stake_address} is not staked")


@stability.command(name="account")
@click.argument("address")
def stability_account(address: str) -> None:
    stake_address = cardano.get_stake_address(address)
    addresses = cardano.get_addresses(stake_address)

    account = indigo.StabilityAccount.find_account(addresses)
    if account.iassets:
        for iasset, balance in account.balances.items():
            print(f"{iasset}: {balance}")

    else:
        print(f"{stake_address} is not staked")
