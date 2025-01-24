import json
# import os
# from dataclasses import dataclass
from pathlib import Path
import logging


logger = logging.getLogger(__name__)

# DEFAULT_JSON_PATH = f'{os.getcwd()}/config.json'
SECRETS_PATH = Path(__file__).parent / '.secrets'
DEFAULT_JSON_PATH = SECRETS_PATH / 'config.json'


def _load(jsonpath:str) -> dict:
        logger.debug(f'loading {jsonpath}')
        with open(jsonpath, 'r') as fp:
            return json.load(fp)


def _save(data:dict, jsonpath:str) -> dict:
        logger.debug(f'saving {jsonpath}')
        with open(jsonpath, 'w') as fp:
            return json.dump(data, fp)


# @dataclass
# class Config:

#     template_path: str
#     year_format: str
#     day_format: str

#     @classmethod
#     def from_json(cls, jsonpath=DEFAULT_JSON_PATH):
#         config = _load(jsonpath)
#         return cls(**config)

from typing import Self
class JsonConfig(dict):

    @classmethod
    def from_json(cls:Self, jsonpath=DEFAULT_JSON_PATH) -> Self:
        logger.debug(f'loading data from {jsonpath}')
        data = _load(jsonpath)
        config = cls()
        logger.debug(f'creating JsonConfig with {data}')
        config.update(data)
        return config
    
    
    def load(self, jsonpath=DEFAULT_JSON_PATH):
        data = _load(jsonpath)
        logger.debug(f'updating from {jsonpath}')
        for k, v in data.items():
            logger.debug(f'    setting {k:15} = {v}')
        self.update(data)
        return self
    
    
    def save(self, jsonpath=DEFAULT_JSON_PATH):
        logger.debug(f'updating {jsonpath}')
        for k, v in self.items():
            logger.debug(f'    saving {k}={v}')
        _save(self, jsonpath)
        return self