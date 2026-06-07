# AutoMojo Interfaces Package - Design Document

## Overview

The AutoMojo Interfaces package is a foundational Python library that provides a collection of protocol-based interfaces for automation and testing frameworks. This package follows Python's Protocol typing system to define contracts for various automation components, enabling loose coupling and enhanced testability.

## Package Structure

```
source/packages/ccai/
└── interfaces/
    ├── __init__.py
    ├── ibasiccredential.py
    ├── iexcludefilter.py
    ├── ihint.py
    ├── iincludefilter.py
    ├── iserializable.py
    └── itestjob.py
```

## Core Interfaces

### 1. IBasicCredential

**Purpose**: Defines the contract for basic authentication credentials.

**Key Properties**:
- `username`: String property for the credential username
- `password`: String property for the credential password

**Use Cases**:
- Authentication systems
- Credential management
- Security testing frameworks

### 2. IExcludeFilter

**Purpose**: Provides a standardized interface for filtering objects based on exclusion criteria.

**Key Methods**:
- `should_exclude(check_object: Any) -> bool`: Determines if an object should be excluded
- `filter(input_list: List[Any]) -> List[Any]`: Filters a list by excluding matching objects

**Use Cases**:
- Test case filtering
- Device selection in automation
- Resource management

### 3. IIncludeFilter

**Purpose**: Provides a standardized interface for filtering objects based on inclusion criteria.

**Key Methods**:
- `should_include(check_object: Any) -> bool`: Determines if an object should be included
- `filter(input_list: List[Any]) -> List[Any]`: Filters a list by including matching objects

**Use Cases**:
- Test case selection
- Resource filtering
- Configuration management

### 4. IHint

**Purpose**: Defines a contract for objects that can provide identification hints and matching capabilities.

**Key Methods**:
- `get_hint() -> str`: Returns a hint string for object identification
- `matches(obj: Any) -> bool`: Checks if the hint matches a given object

**Use Cases**:
- Object identification systems
- Dynamic matching algorithms
- Configuration resolution

### 5. ISerializable

**Purpose**: Establishes a contract for objects that can be serialized to and from dictionary representations.

**Key Methods**:
- `from_dict(cls, data: Dict[str, Any])`: Class method to create instances from dictionaries
- `as_dict() -> Dict[str, Any]`: Instance method to convert objects to dictionaries

**Use Cases**:
- Configuration persistence
- API data exchange
- Test data management

### 6. ITestJob

**Purpose**: Defines the contract for test job execution and management.

**Key Properties & Methods**:
- `importerrors`: Property containing import errors during job loading
- `begin()`: Initializes test job execution
- `execute() -> int`: Executes the test job, returns 0 for success
- `finalize()`: Cleanup and result processing
- `query(query: str, format: int=0) -> List[Any]`: Queries job information and requirements

**Use Cases**:
- Test framework integration
- Job scheduling systems
- Test execution pipelines

## Design Principles

### 1. Protocol-Based Design
All interfaces use Python's `Protocol` typing system, enabling structural subtyping and duck typing while maintaining type safety.

### 2. Separation of Concerns
Each interface focuses on a specific aspect of automation functionality:
- Authentication (IBasicCredential)
- Filtering (IExcludeFilter, IIncludeFilter)
- Identification (IHint)
- Serialization (ISerializable)
- Test Execution (ITestJob)

### 3. Flexibility and Extensibility
Interfaces are designed to be implementation-agnostic, allowing for multiple concrete implementations without breaking existing code.

### 4. Type Safety
All interfaces leverage Python's type hints to provide clear contracts and enable static type checking.

## Implementation Guidelines

### For Interface Implementers

1. **Implement all required methods**: Each protocol defines mandatory methods that must be implemented
2. **Follow type contracts**: Ensure return types and parameter types match the interface specifications
3. **Handle edge cases**: Implement proper error handling for invalid inputs
4. **Document behavior**: Provide clear documentation for implementation-specific behavior

### For Interface Consumers

1. **Use type hints**: Leverage the protocol types for better IDE support and type checking
2. **Handle return values**: Always check return values, especially for methods like `execute()` that return status codes
3. **Error handling**: Implement proper exception handling for interface method calls

## Dependencies

- **Python**: >=3.10,<4.0
- **Typing**: Built-in typing module for Protocol support

## Testing Strategy

Following the repository's unittest framework conventions:

1. **Unit Tests**: Each interface should have corresponding test cases
2. **Mock Implementations**: Create mock classes implementing each protocol for testing
3. **Integration Tests**: Test interface interactions in realistic scenarios
4. **Type Checking**: Use mypy or similar tools to validate type correctness

## Future Considerations

### Potential Extensions

1. **IAsyncTestJob**: Asynchronous version of ITestJob for concurrent test execution
2. **IAdvancedCredential**: Extended credential interface supporting tokens, certificates
3. **IConfigurable**: Interface for objects that can be configured dynamically
4. **ILoggable**: Interface for objects that support structured logging

### Backward Compatibility

- All interface changes should maintain backward compatibility
- New methods should have default implementations when possible
- Deprecation warnings should precede interface changes

## Conclusion

The AutoMojo Interfaces package provides a solid foundation for building modular, testable automation systems. By defining clear contracts through protocols, it enables loose coupling between components while maintaining type safety and clear expectations for implementers.