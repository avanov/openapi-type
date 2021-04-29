=========
CHANGELOG
=========

0.1.0
======

* ``ContentTypeFormat`` is redefined as a new type of ``str`` (used to be a strict Enum)
  for allowing non-common yet valid type representations.

0.0.19
======

* Support for ``#/components/responses``
* Support for ``#/components/headers``
* Support for ``#/components/parameters``
* ``ObjectWithAdditionalProperties`` supports boolean value
* Support for header schemas referenced through ``$ref``

0.0.6
=====

* Support for Content Media Type with charset.

0.0.2
=====

* Attributes use pythonic ``snake_case``.

0.0.1
=====

* Initial Release
