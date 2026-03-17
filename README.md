# SAT Solver using Resolution, DP and DPLL

## Description
This project implements a SAT (Boolean Satisfiability) solver using classical algorithms from propositional logic, including:

- Resolution
- Davis-Putnam (DP)
- DPLL (Davis-Putnam-Logemann-Loveland)

The solver determines whether a given set of logical clauses is satisfiable or unsatisfiable.

## Features
- Clause resolution with tautology elimination
- Unit propagation and pure literal elimination
- Recursive backtracking (DPLL)
- Step-by-step proof generation for better understanding

## Technologies
- Python
- Algorithm design
- Logic & reasoning systems

## Example Input
```python
K = [
    {1, -2, 3},
    {-1, 3, 4},
    {3, -6},
    {-3, -4, 1},
    {-2, -5},
    {-2, 5},
    {-3, 6}
]
