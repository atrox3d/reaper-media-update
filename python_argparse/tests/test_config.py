from dataclasses import dataclass
import json
from typing import Generator, Self, Type, reveal_type
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory


import autoconfig   # !!! pytest.ini: pythonpath = python_argparse


@pytest.fixture
def tempdir() -> Generator[str, None, None]:
    with TemporaryDirectory() as td:
        assert Path(td).exists()
        yield td
    assert not Path(td).exists()


@pytest.fixture
def tempjsonpath(tempdir) -> Generator[str, None, None]:
    jsonpath = Path(tempdir, 'config.json')
    return jsonpath


@pytest.fixture
def testattr() -> str:
    return 'attr'


@pytest.fixture
def testvalue() -> str:
    return 'value'


@pytest.fixture
def tempdata(testattr, testvalue) -> dict:
    return {testattr: testvalue}


@pytest.fixture
def tempjson(tempjsonpath, tempdata):
    with open(tempjsonpath, 'w') as fp:
        json.dump(tempdata, fp, indent=4)
    return tempjsonpath


@dataclass
class Config(autoconfig.AutoConfig):
    attr: str = None


@pytest.fixture
def TestConfig() -> type[Config]:
    return Config


def test_defaults():
    assert autoconfig.SECRETS_PATH == (Path(__file__).parent.parent / '.secrets')
    assert autoconfig.DEFAULT_JSON_PATH == (Path(__file__).parent.parent / '.secrets/config.json')


def test_from_json_attribute_error(tempjson):
    with pytest.raises(TypeError):
        ac = autoconfig.AutoConfig.from_json(tempjson)


def test_from_json(tempjson, TestConfig, testvalue):
    ac = TestConfig.from_json(tempjson)
    assert ac.attr == testvalue


def test_to_json(tempjsonpath):
    ac = autoconfig.AutoConfig()
    ac.x = 5
    
    ac.to_json(tempjsonpath)
    with open(tempjsonpath, 'r') as fp:
        assert json.load(fp) == {'x': 5}


def _test_load(tempjsonpath):
    data = {'x': 5}
    with open(tempjsonpath, 'w') as fp:
        json.dump(data, fp)
    
    ac = autoconfig.AutoConfig.from_json(tempjsonpath)
    assert ac.x == 5


