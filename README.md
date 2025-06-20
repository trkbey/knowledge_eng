# Propositional Logic Inference Engine

This project is a simple propositional logic inference engine implemented in Python. It provides classes to represent logical sentences and evaluate their truth values in different models, as well as a `model_check` function to determine whether a knowledge base entails a query using **truth table enumeration**.

## Features

- Define logical symbols and operators:
  - `Symbol`
  - `Not`
  - `And`
  - `Or`
  - `Implication` (`=>`)
  - `Biconditional` (`<=>`)
- Evaluate logical sentences against truth models.
- Extract all symbols from a formula.
- Use `model_check` to determine if a knowledge base logically entails a query.

## Classes and Their Responsibilities

- `Sentence`: Abstract base class for all logical sentences.
- `Symbol`: Represents a propositional variable.
- `Not`: Negation of a sentence.
- `And`: Conjunction of multiple sentences.
- `Or`: Disjunction of multiple sentences.
- `Implication`: Logical implication (if-then).
- `Biconditional`: Logical biconditional (if and only if).
- `model_check(knowledge, query)`: Checks if the `knowledge` base entails the `query`.

## Usage

```python
from logic import Symbol, Not, And, Or, Implication, Biconditional, model_check

# Define symbols
A = Symbol("A")
B = Symbol("B")

# Define knowledge base: A ∧ (A => B)
knowledge = And(
    A,
    Implication(A, B)
)

# Define query: B
query = B

# Check if knowledge entails query
result = model_check(knowledge, query)
print(f"Does knowledge entail query? {result}")
