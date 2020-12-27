import pytest as pt

from openapi_type import serialize_spec, parse_spec, OpenAPI

from .utils import load_spec
from .paths import SPECS


@pt.mark.parametrize('name, spec_file', SPECS)
def test_parsing(name, spec_file):
    try:
        oapi = load_spec(spec_file)
    except Exception as e:
        print(list(e))
        raise

    assert isinstance(oapi, OpenAPI)
    assert parse_spec(serialize_spec(oapi)) == oapi
