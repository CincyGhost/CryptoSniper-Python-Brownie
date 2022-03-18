
from web3 import Web3
import asyncio
from brownie import config, Contract, network, accounts
import time
from scripts.abi import uni_abi, uni_factory_abi
from scripts.helpful_scripts import get_account
from scripts.buy import buy


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
event_list = []


def handle_event(event):
    Web3.toJSON(event)
    print(event)
    token0 = str(Web3.toJSON(event['args']['token1']))
    token1 = str(Web3.toJSON(event['args']['token0']))
    print("Token0: " + token0)
    print("Token1: " + token1)
    if(token0.upper().strip('"') == token_to_spend.upper() and token1.upper().strip('"') == token_to_buy.upper()):
        print("New Pair Created...")
        event_list.append(event)
        time.sleep(15)
        buy()
    elif(token0.upper().strip('"') == token_to_buy.upper() and token1.upper().strip('"') == token_to_spend.upper()):
        print("New Pair Created...")
        event_list.append(event)
        time.sleep(15)
        buy()
    else:
        print("Searching For Next Pair...")


async def log_loop(event_filter):
    while True:
        print("Searching...")
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(2)


def main():
    event_filter = uni_factory_contract.events.PairCreated.createFilter(
        fromBlock='latest')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(log_loop(event_filter)))
    loop.close()
