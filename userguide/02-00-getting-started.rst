.. _02-00-getting-started:

***************
Getting Started
***************

Installation
============

Other ``codecraftai-*`` packages depend on ``codecraftai-foundations``, which installs from PyPI:

.. code-block:: toml

    [project]
    dependencies = [
        "codecraftai-foundations>=1.0.0,<2.0.0",
    ]

For local development from a checkout:

.. code-block:: bash

    ./repository-setup/rehome-repository
    ./development/setup-environment
    .venv/bin/python-env -m unittest discover -s source/tests -p "test_*.py"

Raising a contextual error
==========================

.. code-block:: python

    from ccai.errors.exceptions import ConfigurationError

    raise ConfigurationError("The landscape file is missing a 'devices' section.")

Waiting for a condition
=======================

.. code-block:: python

    from ccai.waiting import WaitContext, wait_for_it

    def service_is_up(wctx: WaitContext):
        up = check_service()
        if not up and wctx.final_attempt:
            raise wctx.create_timeout("the service to answer on port 9040")
        return up

    wait_for_it(service_is_up, interval=0.5, timeout=30)

Deriving a domain aspects class
===============================

.. code-block:: python

    from ccai.aspects.aspects import Aspects

    class AspectsMyService(Aspects):
        def __init__(self, *, request_timeout: float = 30.0, **base):
            super().__init__(**base)
            self.request_timeout = request_timeout

Freezing a shared constant
==========================

.. code-block:: python

    from ccai.bases.freezable import Freezable

    class Settings(Freezable):
        def __init__(self, retries: int):
            super().__init__()
            self.retries = retries
            self.freeze()

    DEFAULT_SETTINGS = Settings(retries=3)
    DEFAULT_SETTINGS.retries = 5   # raises AttributeError
