import argparse
import json
import sys
from pathlib import Path
from typing import Mapping
from itertools import islice

from openapi_type import parse_spec


def is_empty_dir(p: Path) -> bool:
    return p.is_dir() and not bool(list(islice(p.iterdir(), 1)))


def setup(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    sub = subparsers.add_parser('check', help='Check whether a provided schema (JSON, YAML) can be parsed.')
    sub.add_argument('-s', '--source', help="Path to a spec (JSON, YAML). "
                                            "If not specified, then the data will be read from stdin.")
    sub.set_defaults(run_cmd=main)
    return sub


def main(args: argparse.Namespace, in_channel=sys.stdin, out_channel=sys.stdout) -> None:
    """ $ <cmd-prefix> gen <source> <target>
    """
    try:
        with Path(args.source).open('r') as f:
            python_data = _read_data(f)
    except TypeError:
        # source is None, read from stdin
        python_data = _read_data(in_channel)

    _spec = parse_spec(python_data)

    out_channel.write('Successfully parsed.\n')


def _read_data(fd) -> Mapping:
    buf = fd.read()  # because stdin does not support seek and we want to try both json and yaml parsing
    try:
        struct = json.loads(buf)
    except ValueError:
        try:
            import yaml
        except ImportError:
            raise RuntimeError(
                "Could not parse data as JSON, and could not locate PyYAML library "
                "to try to parse the data as YAML. You can either install PyYAML as a separate "
                "dependency, or use the `third_party` extra tag:\n\n"
                "$ pip install openapi-client-generator[third_party]"
            )
        struct = yaml.full_load(buf)
    return struct
