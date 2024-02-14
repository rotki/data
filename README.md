# data

Repo containing various data that can be pulled by the app


## Things to make sure while adding an airdrop
### Airdrops
- It's entry should be added in the `airdrops/index_v1.json` under the `airdrops` field.
- If the token is new and is not expected to exist in the userDB and globalDB then `new_asset_data` should be added in the index.
- It's CSV should be added in `airdrops/` directory, with its path provided in its index entry.
- If the asset's icon is not present in `rotki` repo, it should be added in `airdrops/icons` directory, with its path provided in its airdrop's index entry.
- CSV should have one line header. First column should be `address`, and second column should be the `amount` in the decimal normalised form.
### POAP Airdrops
- It's entry should be added in the `airdrops/index_v1.json` under the `poap_airdrops` field.
- Entry should have three field in the array, first is the JSON URI having addresses and amounts, second is the URL of airdrop, and third is the name.

Note: Ensure that the index is valid using it's schema at `tests/airdrop_index_v1_schema.json`, by running `pytest tests` command.
