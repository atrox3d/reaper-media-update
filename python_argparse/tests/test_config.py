import json
from typing import Generator
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

import config


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


def test_defaults():
    assert config.SECRETS_PATH == (Path(__file__).parent.parent / '.secrets')
    assert config.DEFAULT_JSON_PATH == (Path(__file__).parent.parent / '.secrets/config.json')


def test_init():
    ac = config.AutoConfig(x=5)
    assert ac.asdict() == {'x': 5}


def test_init_set():
    ac = config.AutoConfig(x=5)
    assert ac.asdict() == {'x': 5}
    
    ac.set(y=10)
    assert ac.asdict() == {'x': 5, 'y': 10}


def test_save(tempjsonpath):
    ac = config.AutoConfig()
    ac.x = 5
    
    ac.save(tempjsonpath)
    with open(tempjsonpath, 'r') as fp:
        assert json.load(fp) == {'x': 5}


def test_load(tempjsonpath):
    data = {'x': 5}
    with open(tempjsonpath, 'w') as fp:
        json.dump(data, fp)
    
    ac = config.AutoConfig.load(tempjsonpath)
    assert list(ac.asdict().keys()) == ['x']
    assert ac.x == 5
    assert ac.asdict() == data


