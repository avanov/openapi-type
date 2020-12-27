.. openapi-type documentation master file, created by
   sphinx-quickstart.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

OpenAPI Type for Python
=======================

**openapi-type** provides the `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification>`_ as a Python type.

.. code-block:: bash

    pip install openapi-type


.. code-block:: python

    from openapi_type import OpenAPI, parse_spec, serialize_spec


    spec: OpenAPI = parse_spec({
        "your OpenAPI Spec as Python dictionary": "will be parsed into a proper Python type"
    })
    assert parse_spec(serialize_spec(spec)) == spec


Quickstart Guide
================

.. toctree::
   :maxdepth: 2

   quickstart_guide.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

