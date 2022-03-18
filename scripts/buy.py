from web3 import Web3
import asyncio
from brownie import config, Contract, network, accounts
import time
from scripts.abi import uni_abi, uni_factory_abi
from scripts.helpful_scripts import get_account


w3 = Web3(Web3.HTTPProvider(
    config["networks"][network.show_active()]["WEB3_INFURA_URL"]))
uni_factory_contract = w3.eth.contract(
    address=config["networks"][network.show_active()]["uni_factory"], abi=uni_factory_abi)
uni_router = Contract.from_abi(
    "UniswapV2Router02", config["networks"][network.show_active()]["uni_router"], uni_abi)


time_until_revert = (int(time.time()) + 10000)
token_to_spend = config["networks"][network.show_active()]["weth"]
token_to_buy = config["networks"][network.show_active()]["test_token"]
amount_eth_to_spend = Web3.toWei(0.001, 'ether')


def buy():
    account = get_account()
    path = [token_to_spend, token_to_buy]
    tx = uni_router.swapExactETHForTokens(0, path, account, time_until_revert, {
        'from': account, 'value': amount_eth_to_spend})
    tx.wait(1)
    print(
        f"Swap Confirmed...bought: {token_to_buy} using: {token_to_spend}...{tx}")


def main():
    buy()
