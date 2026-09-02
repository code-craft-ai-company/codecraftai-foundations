=====================================================
Code Craft AI Foundations - codecraftai-foundations
=====================================================

The ``codecraftai-foundations`` package is the bottom of the ccai dependency graph. It is one
distribution that provides the vocabulary every other ``codecraftai-*`` package is written in:

- ``ccai.errors`` - the shared exception hierarchy and enhanced traceback support.
- ``ccai.interfaces`` - the abstract interfaces and small protocol and schema classes that packages
  implement or accept, so that they never import each other for the sake of a type hint.
- ``ccai.waiting`` - context based waiting primitives with rich timeout diagnostics.
- ``ccai.aspects`` - the minimal ``Aspects`` carrier for behaviour-modifying call parameters.
- ``ccai.bases`` - base classes such as ``Freezable`` that implementation packages derive from.

Every import path is unchanged from the packages these subpackages came from
(``codecraftai-errors``, ``codecraftai-interfaces``, ``codecraftai-waiting`` and, for
``Freezable``, ``codecraftai-xmodules``). Consumers depend on this one package instead of three.

Admission Rule
==============

A module belongs here only if it meets all four tests:

1. It imports nothing outside the Python standard library.
2. It defines contracts, vocabulary or base classes rather than doing work.
3. It changes rarely.
4. More than half of the suite needs it.

Utility code that does work belongs in ``codecraftai-xmodules`` or a domain package, even when it
happens to be standard library only.

Code Organization
=================

* ``.vscode`` - Common tasks
* ``development`` - This is where the runtime environment scripts are located
* ``prompts`` - Pre-built prompts for agent driven work such as bug bashes
* ``repository-setup`` - Scripts for homing your repository and to your checkout and machine setup
* ``specs`` - One folder per subpackage with its requirements, design and task specifications
* ``userguide`` - The user guide and the coding standards for the repository
* ``source/packages`` - The ``ccai`` namespace subpackages
* ``source/tests`` - The ``unittest`` based tests, one folder per subpackage under ``ccai_tests``
* ``workspaces`` - This is where you add VSCode workspaces templates and where workspaces show up when homed.

References
==========

- `User Guide <userguide/userguide.rst>`_
- `Coding Standards <userguide/10-00-coding-standards.rst>`_
