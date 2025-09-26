import json
from pathlib import Path


def test_info_json_and_update_types():
    """Test that info.json exists and all update types can be retrieved"""
    with Path('updates/info.json').open('r') as f:
        info_data = json.load(f)
    
    for update_type, metadata in info_data.items():
        latest_version = metadata['latest']
        if latest_version == 0:  # skip update types with no versions yet
            continue
            
        # test that all versions from 1 to latest exist and are valid JSON
        for version in range(1, latest_version + 1):
            file_path = Path(f'updates/{update_type}/v{version}.json')
            assert file_path.exists(), f'Version file {file_path} does not exist'
            
            with file_path.open('r') as f:
                json.load(f)