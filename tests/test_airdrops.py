import csv
import json
import os
import pytest
import requests
from eth_utils import is_checksum_address
from jsonschema import validate


ROTKI_REPO_BASE = 'https://raw.githubusercontent.com/rotki/rotki/develop'


def test_airdrops_metadata():
    with open('airdrops/index_v1.json', 'r') as f:
        airdrop_index = json.load(f)
    with open('tests/airdrop_index_v1_schema.json', 'r') as f:
        index_schema = json.load(f)

    validate(instance=airdrop_index, schema=index_schema)
    
    # check that the new files exists on their given path
    for airdrop in airdrop_index['airdrops'].values():
        assert os.path.exists(airdrop['csv_path'])
        if requests.get(f'{ROTKI_REPO_BASE}/frontend/app/public/assets/images/protocols/{airdrop["icon"]}').status_code != 200:
            assert 'icon_path' in airdrop, f'{airdrop["name"]} airdrop missing icon in the rotki repository, icon_path should be provided'
            assert os.path.exists(airdrop['icon_path'])


def test_csvs():
    with open('airdrops/index_v1.json', 'r') as f:
        airdrop_index = json.load(f)

    for airdrop in airdrop_index['airdrops'].values():
        with open(airdrop['csv_path']) as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            assert 'address' in reader.fieldnames, f'{airdrop["csv_path"]} airdrop missing `address` header'
            assert 'amount' in reader.fieldnames, f'{airdrop["csv_path"]} airdrop missing `amount` header'
            for row in reader:  # test that all addresses are checksummed
                assert is_checksum_address(row['address']), f'{airdrop["name"]} airdrop address {row["address"]} is not checksummed'


@pytest.mark.skip('It makes too many requests')
def test_data_migration():
    old_airdrop_urls = {
        'uniswap': 'https://gist.githubusercontent.com/LefterisJP/d883cb7187a7c4fcf98c7a62f45568e7/raw/3718c95d572a29b9c3906d7c64726d3bd7524bfd/uniswap.csv',
        '1inch': 'https://gist.githubusercontent.com/LefterisJP/8f41d1511bf354d7e56810188116a410/raw/87d967e86e1435aa3a9ddb97ce20531e4e52dbad/1inch.csv',
        'tornado': 'https://raw.githubusercontent.com/rotki/data/main/airdrops/tornado.csv',
        'cornichon': 'https://gist.githubusercontent.com/LefterisJP/5199d8bc6caa3253c343cd5084489088/raw/7e9ca4c4772fc50780bfe9997e1c43525e1b7445/cornichon_airdrop.csv',
        'grain': 'https://gist.githubusercontent.com/LefterisJP/08d7a5b28876741b300c944650c89280/raw/987ab4a92d5363fdbe262f639565732bd1fd3921/grain_iou.csv',
        'furucombo': 'https://gist.githubusercontent.com/LefterisJP/69612e155e8063fd6b3422d4efbf22a3/raw/b9023960ab1c478ee2620c456e208e5124115c19/furucombo_airdrop.csv',
        'lido': 'https://gist.githubusercontent.com/LefterisJP/57a8d65280a482fed6f3e2cc00c0e540/raw/e6ebac56c438cc8a882585c5f5bfba64eb57c424/lido_airdrop.csv',
        'curve': 'https://gist.githubusercontent.com/LefterisJP/9a37e5342ddb6219a805a82bcd3d63fe/raw/71e89f0e95ea8ef5503fb1ac569447fea63f1ede/curve_airdrop.csv',
        'convex': 'https://gist.githubusercontent.com/LefterisJP/fd0ebccbc645f7de2b142907bd207363/raw/0613689dd5212b81788ed1a108c751b29b2ce93a/convex_airdrop.csv',
        'shapeshift': 'https://raw.githubusercontent.com/rotki/data/main/airdrops/shapeshift.csv',
        'ens': 'https://raw.githubusercontent.com/rotki/data/main/airdrops/ens.csv',
        'psp': 'https://raw.githubusercontent.com/rotki/data/main/airdrops/psp.csv',
        'sdl': 'https://raw.githubusercontent.com/rotki/data/main/airdrops/saddle_finance.csv',
        'cow_mainnet': 'https://raw.githubusercontent.com/rotki/data/main/airdrops/cow_mainnet.csv',
        'cow_gnosis': 'https://raw.githubusercontent.com/rotki/data/main/airdrops/cow_gnosis.csv',
        'diva': 'https://raw.githubusercontent.com/rotki/data/main/airdrops/diva.csv',
        'shutter': 'https://raw.githubusercontent.com/rotki/data/develop/airdrops/shutter.csv',
    }
    old_poap_airdrop_urls = {
        'aave_v2_pioneers': 'https://gist.githubusercontent.com/LefterisJP/569992ba1536474f97f7c74104e66354/raw/a8c5bfb91c8328f8a9d2b6f853a0a55328458ed7/poap_aave_v2_pioneers.json',
        'beacon_chain_first_1024': 'https://gist.githubusercontent.com/LefterisJP/73469098efe0b12965e5752899be00fe/raw/2ee02c22b68b90333359e2f1d24ff5d460dba092/poap_beacon_chain_first_1024.json',
        'beacon_chain_first_32769': 'https://gist.githubusercontent.com/LefterisJP/6302f4e6da6c1488427fbb8b6207222e/raw/1e2e6ebc8c29ba75c2189a5780c132da4ed8530c/poap_beacon_chain_first_32769.json',
        'coingecko_yield_farming': 'https://gist.githubusercontent.com/LefterisJP/58d23332afc6e9fe701ecc80fcc864f6/raw/25ee4153498e9a4c709542d6f541cc9ab76997d8/poap_coingecko_yield_farming.json',
        'eth2_genesis': 'https://gist.githubusercontent.com/LefterisJP/7ce2c343de427c9fe6f54dc9bd6d1a0c/raw/e55baebe6657c11c73b6b808cb269fab31c02da8/poap_eth2_genesis.json',
        'half_rekt': 'https://gist.githubusercontent.com/LefterisJP/429e9c9b3948499cfe793cea75a3b0d6/raw/a0a09372d5bf01285490108661a7c223c1a7de8d/poap_half_rekt.json',
        'keep_stakers': 'https://gist.githubusercontent.com/LefterisJP/b794526fb996cb85dfb825ee5f814e4f/raw/69ed0700a9f7432d783148c89872b86f1d0ee3dd/poap_keep_stakers.json',
        'lumberjackers': 'https://gist.githubusercontent.com/LefterisJP/802359b6825472ee0081580dbe1a1c82/raw/a456fcd1eb1ddedac1cf4b6dd4bbb2d57371f028/poap_lumberjackers.json',
        'medalla': 'https://gist.githubusercontent.com/LefterisJP/1a293bf46b388f709df84ff98c5c5cc6/raw/196ccb50451d908d71cca4bc43731d6547b2276b/poap_medalla.json',
        'muir_glacier': 'https://gist.githubusercontent.com/LefterisJP/d135745cf9f4f3143555e0f6a8f0d804/raw/d34c93087100168cac0dfd0ab46254b4a82ff0b8/poap_muir_glacier.json',
        'proof_of_gucci': 'https://gist.githubusercontent.com/LefterisJP/43b2c4bb73923d7bb3eaf3b329f7f7a1/raw/e5adb753a3a86f0a50bf93137e2c4adc61548293/poap_proof_of_gucci.json',
        'proof_of_gucci_design_competition': 'https://gist.githubusercontent.com/LefterisJP/40c6b2a94d4b8d7f442522b099e5e258/raw/a0851ce92ca2f668e17a97c9df982bc3e12f9bb3/poap_proof_of_gucci_design_competition.json',
        'resuscitators': 'https://gist.githubusercontent.com/LefterisJP/0ac0216f82f16453b74a40529384a152/raw/f003083090efd834bcee1d0d1fe4e218380aa0cf/poap_resucitators.json',
        'yam': 'https://gist.githubusercontent.com/LefterisJP/d676e1f3db8df96928c2501c6be434ac/raw/fa0a603117f6e3e807a49491924aaaa2bc89179a/poap_yam.json',
        'ycover': 'https://gist.githubusercontent.com/LefterisJP/727c05f3a9cab79059258528595c102e/raw/59ff367bd532f632ce94e69900709155a55de82a/poap_ycover.json',
        'yfi_og': 'https://gist.githubusercontent.com/LefterisJP/58862ec2b398c770d60c24e50e18e50c/raw/3292995f530baedcdacde02526c6b2bd1de0e110/poap_yfi_og.json',
    }

    with open('airdrops/index_v1.json', 'r') as f:
        new_index = json.load(f)

    for airdrop_name, airdrop_url in old_airdrop_urls.items():
        assert airdrop_name in new_index['airdrops']
        with open(new_index['airdrops'][airdrop_name]['csv_path'], 'r') as f:
            assert requests.get(airdrop_url).text.strip() == f.read().strip()

    for airdrop_name, airdrop_url in old_poap_airdrop_urls.items():
        assert airdrop_name in new_index['poap_airdrops']
        with open(new_index['poap_airdrops'][airdrop_name][0], 'r') as f:
            assert requests.get(airdrop_url).text.strip() == f.read().strip()
