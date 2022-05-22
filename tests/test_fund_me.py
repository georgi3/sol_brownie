from scripts.supporting_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest



def test_can_fund_withdraw():
    account = get_account()
    fundme = deploy_fund_me()
    entrance_fee = fundme.getEntranceFee()
    tx = fundme.fund({'from': account, 'value': entrance_fee})
    tx.wait(1)
    assert fundme.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fundme.withdraw({'from': account})
    tx2.wait(1)
    assert fundme.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip('Only for local testing')
    fundme = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fundme.withdraw({'from': bad_actor})



