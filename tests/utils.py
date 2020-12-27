import json
from pathlib import Path

from openapi_type import OpenAPI, parse_spec


def load_spec(s: Path) -> OpenAPI:
    with s.open() as fd:
        return parse_spec(json.load(fd))
