.. _badges:

.. image:: https://github.com/avanov/openapi-type/workflows/CI/badge.svg?branch=develop
    :target: https://github.com/avanov/openapi-type/actions?query=branch%3Adevelop

.. image:: https://coveralls.io/repos/github/avanov/openapi-type/badge.svg?branch=develop
    :target: https://coveralls.io/github/avanov/openapi-type?branch=develop

.. image:: https://requires.io/github/avanov/openapi-type/requirements.svg?branch=master
    :target: https://requires.io/github/avanov/openapi-type/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://readthedocs.org/projects/openapi-type/badge/?version=latest
    :target: https://openapi-type.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: http://img.shields.io/pypi/v/openapi-type.svg
    :target: https://pypi.python.org/pypi/openapi-type
    :alt: Latest PyPI Release


OpenAPI Type
============

OpenAPI specification represented as a Python type. Use it to parse specifications written in JSON and YAML formats.

.. code:: bash

    pip install openapi-type


.. code:: python

    from openapi_type import OpenAPI, parse_spec, serialize_spec


    spec: OpenAPI = parse_spec({
        "your OpenAPI Spec as Python dictionary": "will be parsed into a proper Python type"
    })
    assert parse_spec(serialize_spec(spec)) == spec

.. code:: bash

    $ curl -s https://petstore3.swagger.io/api/v3/openapi.json | openapi-type check
    Successfully parsed.


Codegen
-------

If you are looking for a complete client code generator, consider `openapi-client-generator <https://github.com/avanov/openapi-client-generator>`_
that uses this library under the hood.

Cloning this repo
-----------------

The proper way to clone this repo is:

.. code-block:: bash

    git clone --recurse-submodules <repo-url> <local-project-root>
    cd <local-project-root>

    # for showing submodule status with `git status`
    git config status.submodulesummary 1

    # for logging submodule diff with `git diff`
    git config diff.submodule log


Documentation
-------------

Documentation is hosted on ReadTheDocs: https://openapi-type.readthedocs.io/en/develop/


Test framework
--------------

The project uses `Nix <https://nixos.org/>`_ for bootstrapping its dev environment.

You can run existing test suite with

.. code:: bash

   nix-shell --run "make test"


Changelog
---------

See `CHANGELOG <https://github.com/avanov/openapi-type/blob/master/CHANGELOG.rst>`_.
