# coding:utf-8

from decimal import Decimal

from webapi import get_tx_unspent, get_address_received
from bitcoindrpc import getbalance, importprivkey, listunspent, createrawtransaction, validateaddress, \
    signrawtransaction, sendrawtransaction


# def test_webapi():
#     testaddress = 'mwxhfCfwUacrpGCyymWLEiqxRdmUFh6bFK'
#     balances = get_address_received(testaddress)
#     # print balances[0]
#     print(u'已经确认的余额：' + balances[0])
#     print(u'尚未确认的余额：' + balances[1])
#     testlist = get_tx_unspent(testaddress)
#     for _ in testlist:
#         print _


class WalletAccount(object):
    def __init__(self):
        self._public_key = ''
        self._pravite_key = ''
        self._bitcoin_addresses = []

    def is_validate_address(self, address):
        return validateaddress(address)

    def get_balance(self, account_name=None):
        return getbalance(account_name)

    def import_privkey(self, mykey):
        importprivkey(mykey)

    def get_unspents_list(self, account_name=None, reverse=False, address=None):
        result = listunspent(account_name=account_name, reverse=reverse)
        if address is None:
            return result
        else:
            return [tx for tx in result if tx['address'] == address]

    def select_utxos(self, utxo_list, value):
        count = 0
        sum_utxo = Decimal('0')
        for utxo in utxo_list:
            sum_utxo += utxo['amount']
            count += 1
            if sum_utxo >= Decimal(value=str(value)):
                break
        print value, sum_utxo
        return utxo_list[:count]

    def create_txins(self, utxos):
        # utxo_list = self.get_unspents_list()
        # utxos = self.select_utxos(utxo_list, value)
        txins = []
        for tx in utxos:
            txins.append({"txid": tx['txid'], "vout": tx['vout']})
        return txins

    def create_txouts(self, address, value):
        pass

    def create_transaction(self, spends, change_address=None, account_name=None, address=None):
        # spends为嵌套列表
        total = 0
        txouts = {}
        fee = 0.0002
        for spend in spends:
            if not validateaddress(spend[0]):
                print('The address of bitcoin which you send to is wrong, please check it.'/n + spend[0])
                return 0
            total += spend[1]
            txouts[spend[0]] = spend[1]

        balance = self.get_balance(account_name)

        if total > balance:
            print("You balance" + balance + " is less than you want to spend" + total)
            return 0


        utxos = self.get_unspents_list(account_name=account_name, address=address)
        txins = self.create_txins(self.select_utxos(utxos, total))
        print txins, txouts
        raw_hex = createrawtransaction(txins, txouts)
        # return raw_hex
        signed_raw = signrawtransaction(raw_hex)
        txid = sendrawtransaction(signed_raw)
        return txid



if __name__ == '__main__':
    # print bitcoindrpc.getinfo()
    # test_webapi()
    starry = WalletAccount()
    print(starry.get_balance())
    for x in starry.get_unspents_list():
        print(x)
    for utxo in starry.select_utxos(starry.get_unspents_list(), 0.00005):
        print(utxo)
    # print starry.is_validate_address('mwxhfCfwUacrpGCyymWLEiqxRdmUFh6bFK')
    # print createrawtransaction([{"txid":"42e09a73ef188fc1244439a220e3f603e3f964af24b1a4c922779789457f0320","vout":1}],{"mzYYfNr4PykNqnzu48Li3NuYKmEYuydaAL":0.3799})
    # spends_test = [['mouck9e1M2KgN2fk16gN1uUjCpfGE1wvNg', 0.00005]]
    # print starry.create_transaction(spends_test)
