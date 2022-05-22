from brownie import network, accounts, MockV3Aggregator
from web3 import Web3


FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache-local']
DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.load('acc2')  # added thru cli


def deploy_mocks():
    print(f'Active network is {network.show_active()}')
    print(f'Deploying mocks...')
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE,
                                {'from': get_account(), 'gas_price': 70000000})
    print('Mocks deployed')
    price_feed_address = MockV3Aggregator[-1].address
    print(f"price_feed_address, {price_feed_address}")
    print(f'Mock {MockV3Aggregator[-1]}')
