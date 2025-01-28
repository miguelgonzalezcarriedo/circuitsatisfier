# Circuit Satisfiability in CNF Form

## What is CNF?
Conjunctive Normal Form (CNF) is a standardized way of writing Boolean formulas. In CNF, the formula is always structured as:
1. A chain of clauses connected by AND (∧)
2. Each clause is exactly two literals connected by OR (∨)
3. Each literal is either a variable or its negation

The structure is always: (a ∨ b) ∧ (c ∨ d) ∧ (e ∨ f) ∧ ...
where a, b, c, d, e, f are either variables (x₁, x₂, etc.) or their negations (¬x₁, ¬x₂, etc.)

### CNF Structure Rules:
- The TOP level is always AND (∧) operations
- The INNER level is always OR (∨) operations
- Negations (¬) can only appear on individual variables
- No other arrangement or nesting of operations is allowed

### Example:
```
(x₁ ∨ x₂) ∧ (¬x₁ ∨ x₃) ∧ (x₂ ∨ ¬x₃)
```

This formula has:
- 3 clauses connected by AND (∧)
- Each clause has exactly 2 literals connected by OR (∨)
- Uses variables x₁, x₂, x₃ and their negations

## Properties of CNF SAT:
1. Each variable can appear multiple times across different clauses
2. Each variable can appear only once per clause (no `(x₁ ∨ x₁)`)
3. A variable and its negation can appear in the same clause (like `(x₁ ∨ ¬x₁)`)
4. The formula is satisfiable if there exists an assignment of TRUE/FALSE to the variables that makes the entire formula TRUE

## Why CNF for Circuit SAT?
1. CNF is a standard form that can express any Boolean formula
2. The SAT problem in CNF form is NP-complete
3. Many efficient SAT solvers are designed to work with CNF formulas
4. The fixed structure (AND of ORs) makes it easier to process and analyze 

## Why is CNF SAT NP-Hard?
CNF SAT is NP-hard because:

1. **Exponential Search Space**: 
   - For n variables, there are 2ⁿ possible truth assignments
   - Each variable can be either TRUE or FALSE
   - Must check combinations until a satisfying assignment is found
   - No known way to avoid checking exponential possibilities in worst case

2. **No Shortcuts from Structure**:
   - Even though CNF has a simple structure (AND of ORs)
   - The interaction between clauses creates complexity
   - Satisfying one clause might force another to be false
   - Local decisions have global impacts

3. **Proof of NP-Hardness**:
   - CNF SAT was the first problem proven to be NP-complete (Cook-Levin theorem)
   - All other NP problems can be reduced to CNF SAT
   - If we could solve CNF SAT efficiently, we could solve all NP problems efficiently
   - No polynomial-time solution is known

4. **Example of Complexity**:
   For the formula: (x₁ ∨ x₂) ∧ (¬x₁ ∨ x₃) ∧ (x₂ ∨ ¬x₃)
   - Setting x₁=TRUE satisfies first clause
   - This forces us to set x₃=TRUE to satisfy second clause
   - But this might conflict with other clauses
   - These dependencies create complex constraint satisfaction problems 