Installation
------------

.. code-block:: bash

    $ pip install openapi-type


Using CLI tool
--------------

Once installed, ``openapi-type`` provides you with a CLI tool that allows you to generate a
Python client derived from a JSON/YAML specification.

For example, try the following snippet in your shell:

.. code-block:: bash

    $ curl -s https://<specs-location> | openapi-type gen -o <new-client-dir>
