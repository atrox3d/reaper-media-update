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


def test_save(tempjsonpath):
    ac = config.JsonConfig()
    ac['x'] = 5
    
    ac.to_json(tempjsonpath)
    with open(tempjsonpath, 'r') as fp:
        assert json.load(fp) == {'x': 5}


def test_load(tempjsonpath):
    data = {'x': 5}
    with open(tempjsonpath, 'w') as fp:
        json.dump(data, fp)
    
    ac = config.JsonConfig.from_json(tempjsonpath)
    assert ac['x'] == 5


