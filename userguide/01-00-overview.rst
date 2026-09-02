.. _01-00-overview:

********
Overview
********

The ``codecraftai-foundations`` package is a single distribution providing five ``ccai``
subpackages that the rest of the suite is written in terms of. It imports nothing outside the
Python standard library and does no work of its own.

- ``ccai.errors`` - the shared exception hierarchy, enhanced tracebacks and error-raising helpers.
- ``ccai.interfaces`` - abstract interfaces, protocols and schema primitives that packages implement
  or accept.
- ``ccai.waiting`` - ``wait_for_it``, ``WaitContext``, ``WaitGate`` and ``WaitingScope`` for
  context based waiting with descriptive timeouts.
- ``ccai.aspects`` - the minimal ``Aspects`` carrier for behaviour-modifying call parameters.
- ``ccai.bases`` - base classes such as ``Freezable``.

Each subpackage came from a standalone package (``codecraftai-errors``, ``codecraftai-interfaces``,
``codecraftai-waiting`` and, for ``Freezable``, ``codecraftai-xmodules``). Import paths did not
change. The specs for each subpackage are under ``specs/<subpackage>/`` and the tests under
``source/tests/ccai_tests/<subpackage>/``.

See :ref:`02-00-getting-started` for usage examples.
