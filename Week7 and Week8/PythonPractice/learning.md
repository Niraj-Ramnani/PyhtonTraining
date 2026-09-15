# Advanced Python Revision

## Generators

Generators are useful when we want to create values one by one instead of storing everything in memory. They use yield.

- Good for large data sets
- Saves memory
- Produces values lazily

Example idea: a generator can print numbers from 1 to 10 without creating a list first.

## Decorators

Decorators are functions that wrap another function and add extra behavior.

- They help reuse logic
- They are common in logging, validation, and access control
- They keep code clean and flexible

Example idea: a decorator can print before and after a function runs.

## Closures

A closure is a function that remembers values from the outer function even after it finishes.

- Useful for data hiding
- Helps create custom functions
- Often used in decorators

## Context Managers

Context managers handle setup and cleanup automatically.

- Used with with
- Good for file handling and database connections
- Keeps code safe and clean

## Asyncio

Asyncio is used for asynchronous programming in Python.

- async defines a coroutine
- await waits for the result without blocking the whole program
- Good for I/O tasks like API calls or file operations

## Threading

Threading helps run multiple tasks at the same time in one process.

- Useful for tasks that are independent
- Good for small parallel work
- Not always the best choice for CPU-heavy work

## Lambda and Comprehensions

These are short and useful Python features.

- lambda creates small anonymous functions
- list comprehension creates lists in a single line
- dictionary and set comprehensions are also useful

## Exception Handling

Python programs should handle errors carefully.

- try handles risky code
- except catches the error
- finally runs no matter what

## 

## 