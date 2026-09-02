# Code Craft AI Waiting Package Design Document

## Overview

The `codecraftai-waiting` package provides a robust, flexible waiting and timeout management system for Python applications. It is designed primarily for testing frameworks and automation tools where reliable condition polling and timeout handling are critical.

## Architecture

### Core Components

The package is organized into four main modules:

1. **Constants Module** (`constants.py`) - Defines default values and timeout states
2. **Wait Function Module** (`waitfunction.py`) - Contains the primary `wait_for_it` function
3. **Wait Model Module** (`waitmodel.py`) - Defines context classes and protocols
4. **Package Interface** (`__init__.py`) - Exports public API

### Design Principles

The package follows these key design principles:

- **Debuggability over Performance**: Code prioritizes clear error messages and debugging capabilities
- **Readability over Conciseness**: Verbose, self-documenting code for maintainability
- **Isolation and Testability**: Components are designed for unit testing with clear separation of concerns

## Core Functionality

### Wait Function (`wait_for_it`)

The central function provides a polling mechanism with configurable timeout, interval, and delay parameters.

**Signature:**
```python
def wait_for_it(looper: WaitCallback, *largs, what_for: Optional[str]=None, 
                delay: float=DEFAULT_WAIT_DELAY, interval: float=DEFAULT_WAIT_INTERVAL, 
                timeout: float=DEFAULT_WAIT_TIMEOUT, lkwargs: Optional[Dict[Any, Any]]=None, 
                wctx: Optional[WaitContext]=None)
```

**Key Features:**
- Accepts a callback function that returns `True` when condition is met
- Configurable delay before starting, interval between checks, and total timeout
- Provides a final attempt mechanism for last-chance condition checking
- Rich timeout error reporting with timing details
- Optional custom `WaitContext` for advanced scenarios

### Context Management

#### TimeoutContext
Base class providing timeout tracking functionality:
- Tracks start time, end time, and current time
- Manages timeout states (NotStarted, Running, Completed, TimedOut)
- Provides timeout calculation and error message formatting
- Supports timeout extension and delay reduction

#### WaitContext
Extends `TimeoutContext` specifically for wait operations. Currently identical to base class but allows for future wait-specific enhancements.

### Synchronization Primitives

#### WaitGate
Wrapper around `threading.Event` with timeout metadata:
- Encapsulates event with associated timeout and error message
- Provides timeout-aware waiting with optional exception raising
- Supports gate clearing, setting, and status checking

#### WaitingScope
Context manager for coordinating multiple gates:
- Clears all managed gates on entry
- Provides collective waiting for all gates to be set
- Ensures proper cleanup on scope exit

### Constants and Configuration

Default timing values:
- `DEFAULT_WAIT_DELAY = 0` (no initial delay)
- `DEFAULT_WAIT_INTERVAL = 5` (5-second polling interval)
- `DEFAULT_WAIT_TIMEOUT = 60` (60-second total timeout)

Timeout states enumeration for tracking wait progress.

## Usage Patterns

### Basic Polling
```python
def condition_check(wctx):
    return some_condition_is_met()

wait_for_it(condition_check, what_for="service to be ready")
```

### Final Attempt Handling
```python
def condition_with_final_attempt(wctx):
    if wctx.final_attempt:
        # Last chance logic
        return perform_final_check()
    return regular_check()
```

### Custom Timing
```python
wait_for_it(condition_check, delay=2, interval=1, timeout=30)
```

### Gate Synchronization
```python
gate = WaitGate(threading.Event(), "process completion", timeout=30)
# ... in another thread: gate.set()
gate.wait(raise_timeout=True)
```

## Error Handling

The package provides detailed timeout error reporting including:
- Human-readable description of what was being waited for
- Precise timing information (start, end, current times)
- Time difference calculations
- Optional additional detail lines

Error messages follow the format:
```
Timeout waiting for {what_for}:
    timeout={timeout} start_time={start} end_time={end} now_time={now} time_diff={diff}
```

## Testing Strategy

The package uses Python's `unittest` framework with focus on:
- **Granular Testing**: Each test verifies a single aspect of functionality
- **Isolation**: Tests use `setUp`/`tearDown` for proper test separation
- **Concurrent Testing**: Uses `ThreadPoolExecutor` to test timing-dependent behavior
- **Final Attempt Verification**: Ensures final attempt mechanism works correctly
- **Timeout Validation**: Confirms proper timeout error raising and handling

## Thread Safety

The package is designed to be thread-safe:
- `WaitGate` wraps `threading.Event` which is thread-safe
- `WaitingScope` coordinates multiple gates safely
- Context objects track timing using thread-safe `datetime` operations

## Extension Points

The design allows for future enhancements:
- `WaitCallback` protocol enables custom callback implementations
- `WaitContext` can be extended for specialized wait scenarios
- `TimeoutContext` provides base functionality for other timeout-related classes
- Modular design allows adding new synchronization primitives

## Dependencies

The package has minimal external dependencies:
- Standard library modules: `time`, `datetime`, `threading`, `os`, `types`
- Type hints using `typing` module for better IDE support and documentation

## Performance Considerations

While performance is secondary to debuggability, the design includes:
- Efficient polling with configurable intervals
- Minimal object creation during wait loops
- Direct use of `threading.Event` for synchronization primitives
- Lazy error message formatting (only when timeouts occur)

## Future Enhancements

Potential areas for expansion:
- Exponential backoff polling strategies
- Condition composition (AND/OR operations on multiple conditions)
- Metrics collection for wait performance analysis
- Integration with logging frameworks for wait operation tracking
- Support for async/await patterns