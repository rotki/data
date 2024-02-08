import json
from jsonschema import validate


def test_airdrops_metadata():
    airdrop_index = json.load(open('airdrops/index_v1.json'))
    index_schema = json.load(open('tests/airdrop_index_v1_schema.json'))
    validate(instance=airdrop_index, schema=index_schema)
