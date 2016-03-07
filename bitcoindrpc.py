# coding:utf-8
from __future__ import print_function
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = 'bitcoinrpc'
rpc_password = '5ad337108491d38a8285a7048987148a'
rpc_port = 18332  # 测试网络的端口是18332，正式网络的端口是8332
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s" % (rpc_user, rpc_password, str(rpc_port)))


def getinfo():
    return rpc_connection.getinfo()


def getbalance(account_name=None):
    if account_name is None:
        return rpc_connection.getbalance()
    else:
        return rpc_connection.getbalance(account_name)


def importprivkey(bitcoinprivkey):
    rpc_connection.importprivkey(bitcoinprivkey)


def listunspent(account_name=None, reverse=False):
    unspents_list = []
    if account_name is None:
        unspents_list = rpc_connection.listunspent()
    else:
        unspents_list = rpc_connection.listunspent(account_name)
    result = []
    for tx in unspents_list:
        result.append({'vout': tx['vout'],
                       'txid': tx['txid'],
                       'amount': tx['amount'],
                       'address': tx['address']
                       })
    # print(result)
    return sorted(result, key=lambda x: x['amount'], reverse=reverse)

def createrawtransaction(txins, txouts):
    return rpc_connection.createrawtransaction(txins, txouts)

def validateaddress(address):
    return rpc_connection.validateaddress(address)['isvalid']

def signrawtransaction(raw_tx_hex):
    return rpc_connection.signrawtransaction(raw_tx_hex)['hex']

def sendrawtransaction(signed_tx_hex):
    return rpc_connection.sendrawtransaction(signed_tx_hex)


if __name__ == '__main__':
    best_block_hash = rpc_connection.getbestblockhash()
    print(best_block_hash)
    print(rpc_connection.getblock(best_block_hash))
    print(rpc_connection.getinfo())
    print(rpc_connection.getbestblockhash())
    # batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
    commands = [["getblockhash", height] for height in range(100)]
    block_hashes = rpc_connection.batch_(commands)
    blocks = rpc_connection.batch_([["getblock", h] for h in block_hashes])
    block_times = [block["time"] for block in blocks]
    print(block_times)
