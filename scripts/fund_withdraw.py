from brownie import FundMe
from scripts.supporting_scripts import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(f'The current entry fee is {entrance_fee}')
    fund_me.fund({'from': account, 'value': entrance_fee})


def withdraw():
    fundme = FundMe[-1]
    account = get_account()
    fundme.withdraw({'from': account})


def main():
    fund()
    withdraw()
