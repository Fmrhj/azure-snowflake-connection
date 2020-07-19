from typing import Dict

import yaml


def parse_configuration(path: str = None) -> Dict:
    loader = yaml.SafeLoader

    with open(path) as config_data:
        return yaml.load(config_data, Loader=loader)
