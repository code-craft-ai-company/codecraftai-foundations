# AutoMojo Errors Package Design

## Overview

The `automojo.errors` package is a centralized error handling library designed to provide standardized exception types and error management utilities for automation testing frameworks. This package serves as a foundational component that ensures consistent error handling across multiple automation packages by providing:

1. **Standardized Exception Types** - A comprehensive collection of domain-specific exceptions
2. **Error Enhancement Utilities** - Tools for adding context and improving error diagnostics  
3. **HTTP Status Code Mapping** - Automatic exception raising based on HTTP response codes
4. **Enhanced Traceback Formatting** - Improved error reporting with contextual information

## Architecture

The package is organized into four main modules:

```
automojo/errors/
├── __init__.py          # Package initialization
├── exceptions.py        # Exception type definitions
├── raising.py          # HTTP error raising utilities
└── xtraceback.py       # Enhanced traceback and error context
```

## Core Components

### 1. Exception Hierarchy (`exceptions.py`)

The package defines a comprehensive hierarchy of exception types organized by domain:

#### Base Exception Categories
- **ConfigurationError** - Configuration-related issues
- **SemanticError** - Code usage and semantic problems
- **CommandError** - Command execution failures
- **ProtocolError** - Communication protocol errors

#### Specialized Exception Groups

**Flow Control Exceptions:**
- `CancelledError` - Operation cancellation
- `HaltError` - Flow control halting
- `SkipError` - Execution skipping
- `TaskingCancelled` - Task cancellation
- `TaskingGroupCancelled` - Group task cancellation

**Timeout Exceptions:**
- `CompletionTimeout` - Operation completion timeouts
- `ConnectionTimeout` - Connection establishment timeouts
- `InActivityTimeout` - Inactivity-based timeouts

**Command Line Exceptions:**
- `BadOptionUsageError` - Invalid option usage
- `BadParameterError` - Invalid parameter values
- `MissingArgumentError` - Required arguments missing
- `MissingOptionError` - Required options missing
- `NoSuchOptionError` - Unrecognized options
- `TooManyArgumentsError` - Excess arguments

**HTTP Status Code Exceptions:**
- Complete mapping of HTTP 3xx, 4xx, and 5xx status codes
- Hierarchical organization (e.g., `HttpResponse4xxError` base class)
- Specific exceptions for each status code (e.g., `HttpNotFoundError` for 404)

### 2. HTTP Error Raising (`raising.py`)

Provides utilities for automatically raising appropriate HTTP exceptions:

#### Key Functions
- `format_http_error_message()` - Formats HTTP error messages with context
- `raise_for_http_status()` - Automatically raises exceptions based on HTTP status codes

#### Status Code Mapping
- Maintains a lookup table (`STATUS_TO_EXCEPTION_TABLE`) mapping HTTP status codes to exception types
- Supports fallback to generic category exceptions for unmapped codes
- Handles 3xx, 4xx, and 5xx status code ranges

### 3. Enhanced Traceback System (`xtraceback.py`)

Provides advanced error context and traceback formatting capabilities:

#### Core Classes
- `FrameDetail` - Detailed frame information including arguments and source code
- `OriginDetail` - Error origin location information
- `TraceDetail` - Individual trace entry with context
- `TracebackDetail` - Complete traceback information

#### Enhancement Features
- **EnhancedErrorMixIn** - Mixin class for adding context to exceptions
- **Context Management** - Associate contextual information with specific function calls
- **Source Code Integration** - Include actual source code in tracebacks
- **Argument Inspection** - Display function arguments at each stack frame

#### Formatting Policies
- `TracebackFormatPolicy.Brief` - Minimal traceback information
- `TracebackFormatPolicy.Full` - Complete traceback with source code
- `TracebackFormatPolicy.Hide` - Suppress traceback information

#### Key Functions
- `enhance_exception()` - Add context to existing exceptions
- `create_traceback_detail()` - Generate detailed traceback information
- `format_exception()` - Format exceptions with enhanced information
- `collect_stack_frames()` - Gather comprehensive stack frame details

## Design Principles

### 1. Centralized Error Types
All exception types are defined in a single location to ensure consistency across packages that depend on this library. This prevents duplicate exception definitions and ensures that error handling code can rely on specific exception types.

### 2. Hierarchical Organization
Exceptions are organized in a logical hierarchy that allows for both specific and general exception handling. Base classes like `ConfigurationError` allow catching broad categories, while specific exceptions like `MissingConfigurationError` enable precise error handling.

### 3. Rich Context Information
The enhanced traceback system provides significantly more information than standard Python tracebacks, including:
- Function arguments at each stack frame
- Source code context around error locations
- Custom context information added by developers
- Configurable formatting policies

### 4. HTTP Integration
Seamless integration with HTTP-based operations through automatic exception mapping and formatting utilities that handle the complexity of HTTP status code interpretation.

### 5. Debuggability Focus
Following the project's principle of prioritizing debuggability over performance, the package provides extensive diagnostic information to help developers quickly identify and resolve issues.

## Usage Patterns

### Exception Raising
```python
from automojo.errors.exceptions import ConfigurationError
raise ConfigurationError("Invalid configuration parameter")
```

### HTTP Error Handling
```python
from automojo.errors.raising import raise_for_http_status
raise_for_http_status(404, "Not Found", context="API endpoint lookup")
```

### Exception Enhancement
```python
from automojo.errors.xtraceback import enhance_exception
try:
    risky_operation()
except Exception as ex:
    enhance_exception(ex, "Additional context about the operation")
    raise
```

### Enhanced Traceback
```python
from automojo.errors.xtraceback import format_exception
try:
    failing_operation()
except Exception as ex:
    formatted_lines = format_exception(ex)
    for line in formatted_lines:
        print(line)
```

## Integration Points

This package is designed to be imported and used by other automation packages that need:
- Consistent exception types for error handling
- HTTP status code to exception mapping
- Enhanced error reporting and debugging capabilities
- Standardized error context management

The package follows the project's naming conventions and code organization standards, making it a foundational component for the broader automation testing ecosystem.