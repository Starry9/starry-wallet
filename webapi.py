# coding:utf-8
import requests

# 选择网络
NETWORK = 'BTCTEST'
API_PREFIX = 'https://chain.so/api/v2/'


def get_address_received(address):
    api_url = API_PREFIX + 'get_address_received/' + NETWORK + '/' + address
    response = requests.get(api_url)

    if response.status_code == 200:
        # everything went swimmingly
        # parse the response as JSON
        content = response.json()

        return [content['data']['confirmed_received_value'], content['data']['unconfirmed_received_value']]

def get_tx_unspent(address):
    api_url = API_PREFIX + 'get_tx_unspent/' + NETWORK + '/' + address
    response = requests.get(api_url)
    utxo_list = []

    if response.status_code == 200:
        # everything went swimmingly
        # parse the response as JSON
        content = response.json()
        for tx in content['data']['txs']:
            utxo_list.append({'txid':tx['txid'], 'value':float(tx['value'])})

    return sorted(utxo_list, key=lambda x:x['value'])