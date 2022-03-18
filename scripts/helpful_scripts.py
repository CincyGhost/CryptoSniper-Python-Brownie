
from brownie import network, accounts, config
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development", "ganache-local", "mainnet-fork"]


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_account2():
    return accounts.add(config["wallets"]["from_key2"])
