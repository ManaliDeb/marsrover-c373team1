 # ADR 1: Use Python as Implementation Language

## Context
We need to select a programming language for implementing the Mars Rover kata. The project requires:

Support for object-oriented design patterns (Command, Strategy)
Good testing infrastructure
Clear separation of concerns
Easy-to-read code for educational purposes (COMP 373)
Quick development cycle for a course project
Support for protocols/interfaces for dependency injection

The team members have varying levels of experience with different languages, but all are comfortable with Python.

## Decision
We will use Python 3.10+ as our implementation language for the Mars Rover project.
We will leverage Python's features including:

* dataclasses for immutable domain objects
* Protocol from typing for interface definitions
* Enum for type-safe heading directions
* Type hints throughout for better IDE support and documentation
pytest for testing framework

## Consequences
### Positive

Rapid development: Python's concise syntax allows us to focus on design patterns rather than boilerplate
Excellent testing tools: pytest provides clean, readable tests with minimal setup
Protocol support: Python 3.8+ Protocols provide structural subtyping without inheritance
Strong typing available: Type hints + mypy allow us to catch errors while maintaining flexibility
Built-in features: dataclasses, enums, and other standard library features reduce boilerplate
Team familiarity: All team members can contribute effectively
Clear code: Python's readability helps demonstrate design principles for educational purposes
Easy CI/CD: GitHub Actions has excellent Python support

### Negative

Runtime type checking: Type hints are not enforced at runtime (though we can use mypy in CI)
Performance: Not relevant for this kata, but Python is slower than compiled languages
No compile-time guarantees: Errors that would be caught at compile time in Java/C# appear at runtime
GIL limitations: Not relevant for single-threaded kata, but limits true parallelism
Flexibility can lead to inconsistency: Python's dynamic nature requires discipline to maintain patterns


We chose Python because it offers the best balance of expressiveness, team familiarity, testing tools, and educational clarity for demonstrating design patterns.