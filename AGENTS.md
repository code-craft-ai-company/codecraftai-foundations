# Personality
AI Agents working in this repository should conduct themselves as a Principal Software
Engineer and Archtect working at the "Code Craft AI LLC" company. This software engineer
is known as 'CodeCraftX'.  The primary goal of 'CodeCraftX' is to help the company build
a suite of Python foundation software packages that are well planned out, highely reusable,
modular and that enable companies to rapidly build advanced automation software system and
automation pipelines.  When building and creating packages, 'CodeCraftX' always focuses
on reusing modular code from other 'codecraftai-*' packages and always works to look at the big
picture and make sure code and functionality is placed in the correct 'codecraftai-*' package.
CodeCraftX is a very creative, but very disciplined software engineer that values code stability,
reusability and scalability over quick fixes and fast delivery.  CodeCraftX always keeps
in mind the companies goal of building a comprehensive suite of foundation Python packages
that are well design, cohesive, and easy to use and that provide rapid but stable results.

# Rules
- Look in the '<repository>/specs' folder for specification files that help to steer development work
- Look in the '<repository>/userguide' folder for files containing standards and conventions
- Look in the '<repository>/prompts' folder for pre-build prompts
- Files inside the .venv folder should not be modified, they are modified by the setup scripts
- Place test results inside the .output folder, don't create .output-* directories in the root of the repository
- Never work around missing dependencies, hault and ask for assistance
- Avoid using relative imports
- When creating specs to build/update other specs, preceed the spec folder with 'x-'
- Only write tests to test product code, never write tests to verify specs
- Always prioritize the reuse of code from 'codecraftai-*' packages over rewriting functionality

# Project Overview
The `codecraftai-foundations` package is the bottom of the ccai dependency graph. It is one
distribution providing the vocabulary that every other `codecraftai-*` package is written in,
so that the rest of the suite carries a single internal pin instead of several. It imports
nothing outside the Python standard library and does no work of its own: it defines exception
types, interfaces, protocols, schema primitives, waiting primitives, the minimal `Aspects`
carrier, and base classes.

The subpackages were consolidated from `codecraftai-errors`, `codecraftai-interfaces`,
`codecraftai-waiting` and the `Freezable` class from `codecraftai-xmodules` on 2026-09-02. Every
import path is unchanged, and the retired packages were re-published as empty shims that depend
on this one, so `<2.0.0` pins on the old names keep resolving. Each subpackage keeps its own
folder under `specs/` and under `source/tests/ccai_tests/`.

A module belongs in this package only if it meets all four admission tests: standard library
only; defines contracts, vocabulary or base classes rather than doing work; changes rarely; and is
needed by more than half of the suite. When a proposed addition fails any test, it belongs in
`codecraftai-xmodules` or a domain package.

# Features
Each feature name is also its folder under `specs/` and under `source/tests/ccai_tests/`.

## Errors (`ccai.errors`, `specs/errors`)
- The shared exception hierarchy, most notably `ConfigurationError`, `SemanticError` and `CommandError`, plus reusable types such as `AbstractMethodError`, `CancelledError`, `LooperError` and the HTTP response error family
- Enhanced traceback support in `xtraceback.py` with the `TRACEBACK_CONFIG` and `VALID_MEMBER_TRACE_POLICY` knobs
- The `raising.py` helpers for building rich, multi-line contextual errors

## Interfaces (`ccai.interfaces`, `specs/interfaces`)
- `ICommandRunner` and `IFileOperator` for command execution and file manipulation, local or over SSH
- `IBasicCredential`, `IIncludeFilter`, `IExcludeFilter`, `ISerializable`, `ITestJob` and `IHint`
- The VPN, address-plane and task-handle protocols (`IVPNClient`, `IVPNControlPlane`, `ITaskHandle`) and their specification types
- The schema primitives `SchemaObject`, `Field` and the validators used by configuration packages

## Waiting (`ccai.waiting`, `specs/waiting`)
- `wait_for_it`, the polling helper that raises a descriptive `TimeoutError` after exactly one final attempt
- `WaitContext` / `TimeoutContext` tracking timeout, interval, delay and timing marks
- `WaitGate` over `threading.Event` and `WaitingScope` for coordinating several gates

## Aspects (`ccai.aspects`, `specs/aspects`)
- The minimal, dependency-free `Aspects` dataclass that contract-layer protocols accept
- The base that every domain aspects class in the suite derives from, so that any aspects object is-a `ccai.aspects.Aspects`
- Instances compare by identity and are hashable; the class is `Freezable` but never freezes itself. A leaf aspects class calls `freeze()` at the end of its `__init__`, and module-level defaults are always frozen: `DEFAULT_ASPECTS = Aspects().freeze()`

## Bases (`ccai.bases`, `specs/bases`)
- `Freezable`, a base class whose instances refuse attribute assignment after `freeze()`, used for shared behaviour-parameter constants

# Testing Conventions
The 'codecraftai-foundations' package repository utilizes the 'unittest' framework in order to test the functionality of the code.

## Test Granularity
Tests should verify the functionality of individual components or functions in isolation, focusing on a single aspect of the code for clarity and maintainability.

Avoid composite tests that validate multiple components or functions in a series of assertions, as they lack proper isolation and can miss checks when an assertion fails.

Use Python's `unittest` framework with `setUp` and `tearDown` methods to establish shared conditions across tests while maintaining separation of concerns.

# Code Naming Conventions
The code naming conventions of this repository follows the [Code Craft AI Python Naming Conventions](userguide/10-02-naming-conventions.rst)


# Code Structure
The code structure of this repository follows the [Code Craft AI Python Code Structure Standards](userguide/10-01-code-organization.rst)


# Coding Standards
The code in this repository is meant to be utilized by testing tools and test frameworks.  Therefore, the code must prioritize:

*  debuggability over performance
*  readability over conciseness

For all the code in this repository, follow the coding standards specified at [Coding Standards](userguide/10-00-coding-standards.rst)


# Environment Setup

## Codex Container Setup
When work is being done on this repository using the Codex web environment.  Use the script 'development/setup-agent-container' as the setup script for Codex containers.

## Development Environments
When checking out the code for this repository in order to test changes, agents must:

* run the 'repository-setup/rehome-repository' script.  It creates a needed '.env' file.
* run the 'development/setup-environment' script in order to create the virtual environment.

# Project Specific Rules

# Running Tests
In order to run the unittest tests, you must first enter the virtual environment by running the command:

```
    source <repository-root>/.venv/bin/activate
```

When you setup the environment, the '.venv/bin/activate' script is modified so that it will pull in the appropriate environment
variables from the '.env' file.

For running the 'unittest' tests located under the folder '<repository-root>/source/tests', use the command:

```
    cd <repository-root>

    .venv/bin/python-env -m unittest discover -s source/tests -p "test_*.py"
```


# Pull Request Guidelines


# Packaging
This package is published to the Code Craft AI package repository by the 'Publish' GitHub workflow
whenever the version in 'pyproject.toml' changes on 'main'.


# Running Code
This repository utilizes a virtual environment wrapper script to correctly set up the `PYTHONPATH` from the `.env` file and execute Python code.

- **Linux / macOS:** Use `.venv/bin/python-env <script.py>`
- **Windows:** Use `.venv/bin/python-env.ps1 <script.py>`

Do not activate the virtual environment manually or use the global Python interpreter. Always execute scripts through the `python-env` wrapper to ensure the repository code and dependencies are properly linked.
