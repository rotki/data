from collections import defaultdict
from decimal import Decimal, getcontext
from http import HTTPStatus
import json
from typing import Any, Callable
import urllib3

import warnings


def validate_rpc(rpc: dict[str, Any], method: str, validator: Callable[[dict[str, Any]], None]) -> None:
    """Validate RPC endpoint with specified method and validation function"""
    try:
        resp = urllib3.request(
            method='POST',
            url=(url := rpc['endpoint']),
            json={'method': method, 'params': [], 'id': 1, 'jsonrpc': '2.0'},
            retries=1,
            timeout=5,
        )
    except urllib3.exceptions.HTTPError as e:
        warnings.warn(f'Failed to connect to {url} due to {e}')
        return

    if resp.status in (HTTPStatus.TOO_MANY_REQUESTS, HTTPStatus.GATEWAY_TIMEOUT):
        warnings.warn(f'Failed to connect to {url} due to {resp.status}')
        return
    
    try:
        assert validator(resp.json()) is True
    except (json.decoder.JSONDecodeError, KeyError) as e:
        warnings.warn(f'Failed to decode JSON response from {url} due to {e}')


def test_nodes() -> None:
    """Check that all the chains have nodes with weight summing 1"""
    
    with open('updates/info.json') as index_file:
        index_data = json.load(index_file)
        latest_nodes = index_data['rpc_nodes']['latest']

    getcontext().prec = 6
    evm_chains_mapping = {
        1: 'ETH',
        10: 'OPTIMISM', 
        56: 'BINANCE_SC',
        100: 'GNOSIS',
        137: 'POLYGON_POS',
        8453: 'BASE',
        42161: 'ARBITRUM_ONE',
        534352: 'SCROLL',
    }
    for i in range(1,latest_nodes + 1):
        per_chain_weight = defaultdict(Decimal)
        with open(f'updates/rpc_nodes/v{i}.json', 'r') as f:
            for rpc in json.load(f)['rpc_nodes']:
                per_chain_weight[rpc['blockchain']] += Decimal(rpc['weight'])
                
                if i == latest_nodes:
                    if len(rpc['endpoint']) == 0:
                        continue
                    
                    if rpc['blockchain'] == 'SOLANA':
                        validate_rpc(
                            rpc=rpc,
                            method='getHealth',
                            validator=lambda resp: resp['result'] == 'ok',
                        )
                    else:
                        validate_rpc(
                            rpc=rpc,
                            method='eth_chainId',
                            validator=lambda resp: evm_chains_mapping[int(resp['result'], 0)] == rpc['blockchain'],
                        )

        assert all(weight == 1 for weight in per_chain_weight.values()), f'Weights do not add for v{i}: {per_chain_weight=}'
