import json
import os
from dataclasses import dataclass
from pathlib import Path


# DEFAULT_JSON_PATH = f'{os.getcwd()}/config.json'
SECRETS_PATH = Path(__file__).parent / '.secrets'
DEFAULT_JSON_PATH = SECRETS_PATH / 'config.json'
INDENT = 4


def _load(jsonpath:str) -> dict:
        with open(jsonpath, 'r') as fp:
            return json.load(fp)


def _makepath(jsonpath:str):
    Path(jsonpath).parent.mkdir(exist_ok=True)


def _save(data:dict, jsonpath:str, indent=INDENT) -> dict:
        _makepath(jsonpath)
        with open(jsonpath, 'w') as fp:
            return json.dump(data, fp, indent=indent)


class AutoConfig:

    @classmethod
    def fromjson(cls, jsonpath=DEFAULT_JSON_PATH) -> 'AutoConfig':
        config = _load(jsonpath)
        return cls(**config)
    
    
    def __init__(self, *, source:'AutoConfig'=None ,**kwargs):
        if source is not None:
            self.set(**source.asdict())
        self.set(**kwargs)
    
    
    def set(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    
    def update(self, fromdict:dict):
        self.set(**fromdict)
    
    
    def update_fromjson(self, jsonpath:str=DEFAULT_JSON_PATH):
        config = _load(jsonpath)
        self.update(config)
    
    
    def save(self, jsonpath=DEFAULT_JSON_PATH, indent=INDENT):
        out = {k: str(v) for k, v in self.asdict().items()}
        _save(out, jsonpath, indent)
    
    
    def asdict(self) -> dict:
        return vars(self)
