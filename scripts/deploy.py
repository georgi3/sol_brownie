from brownie import FundMe, MockV3Aggregator, config, network
from scripts.supporting_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to fundme contract
    # if we are on persistent network like rinkeby, use the associated address, otherwise deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config['networks'][network.show_active()]['eth_usd_price_feed']
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(price_feed_address,
                            {'from': account, 'gas_price': 700000},
                            publish_source=config['networks'][network.show_active()].get('verify'))

    print(f'FundMe {fund_me}')
    print(f'Contract deployed to {fund_me.address}')
    return fund_me


def main():
    deploy_fund_me()
