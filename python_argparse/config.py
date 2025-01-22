import json
import os
from dataclasses import dataclass
from pathlib import Path


# DEFAULT_JSON_PATH = f'{os.getcwd()}/config.json'
SECRETS_PATH = Path(__file__).parent / '.secrets'
DEFAULT_JSON_PATH = SECRETS_PATH / 'config.json'


def _load(jsonpath:str) -> dict:
        with open(jsonpath, 'r') as fp:
            return json.load(fp)


def _save(data:dict, jsonpath:str) -> dict:
        with open(jsonpath, 'w') as fp:
            return json.dump(data, fp)


@dataclass
class Config:

    template_path: str
    year_format: str
    day_format: str

    @classmethod
    def from_json(cls, jsonpath=DEFAULT_JSON_PATH):
        config = _load(jsonpath)
        return cls(**config)


class AutoConfig:

    @classmethod
    def from_json(cls, jsonpath=DEFAULT_JSON_PATH) -> 'AutoConfig':
        config = _load(jsonpath)
        autoconfig = cls()
        for k, v in config.items():
            setattr(autoconfig, k, v)
        return autoconfig
    
    
    def to_json(self, jsonpath=DEFAULT_JSON_PATH):
        config = vars(self)
        _save(config, jsonpath)
