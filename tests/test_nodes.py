from collections import defaultdict
from decimal import Decimal, getcontext
from http import HTTPStatus
import json
import urllib3

import warnings


def test_nodes():
    """Check that all the chains have nodes with weight summing 1"""
    
    with open('updates/info.json') as index_file:
        index_data = json.load(index_file)
        latest_nodes = index_data['rpc_nodes']['latest']

    getcontext().prec = 6
    for i in range(1,latest_nodes + 1):
        per_chain_weight = defaultdict(Decimal)
        with open(f'updates/rpc_nodes/v{i}.json', 'r') as f:
            for rpc in json.load(f)['rpc_nodes']:
                per_chain_weight[rpc['blockchain']] += Decimal(rpc['weight'])
                
                if i == latest_nodes:
                    if len(rpc['endpoint']) == 0:
                        continue
                    
                    try:
                        resp = urllib3.request(
                            "POST",
                            rpc['endpoint'],
                            json={"method":"eth_chainId","params":[],"id":1,"jsonrpc":"2.0"},
                            retries=1,
                            timeout=5,
                        )
                    except urllib3.exceptions.MaxRetryError as e:
                        warnings.warn(f'Failed to connect to {rpc["endpoint"]} due to {e}')

                    if resp.status == (HTTPStatus.TOO_MANY_REQUESTS, HTTPStatus.GATEWAY_TIMEOUT):
                        warnings.warn(f'Failed to connect to {rpc["endpoint"]} due to {resp.status}')
                        continue
                    
                    try:
                        chain = int(resp.json()['result'], 0)
                    except (json.decoder.JSONDecodeError, KeyError) as e:
                        warnings.warn(f'Failed to read response from {rpc["endpoint"]} due to {e}')
                        continue

                    match chain:
                        case 1:
                            assert rpc['blockchain'] == 'ETH'
                        case 10:
                            assert rpc['blockchain'] == 'OPTIMISM'
                        case 100:
                            assert rpc['blockchain'] == 'GNOSIS'
                        case 42161:
                            assert rpc['blockchain'] == 'ARBITRUM_ONE'
                        case 534352:
                            assert rpc['blockchain'] == 'SCROLL'
                        case 137:
                            assert rpc['blockchain'] == 'POLYGON_POS'
                        case 137:
                            assert rpc['blockchain'] == 'POLYGON_POS'
                        case 8453:
                            assert rpc['blockchain'] == 'BASE'
                        case _:
                            raise Exception(f'Unexpected chain version for {rpc}')

        assert all(weight == 1 for weight in per_chain_weight.values()), f'Weights do not add for v{i}: {per_chain_weight=}'
