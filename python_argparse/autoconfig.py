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

from typing import TypeVar, Type

# Create a generic variable that can be 'Parent', or any subclass.
T = TypeVar('T', bound='AutoConfig')

@dataclass
class AutoConfig:

    @classmethod
    def from_json(cls:Type[T], jsonpath=DEFAULT_JSON_PATH) -> T:
        config = _load(jsonpath)
        return cls(**config)
    
    
    def to_json(self, jsonpath=DEFAULT_JSON_PATH) -> None:
        config = vars(self)
        _save(config, jsonpath)
