# Circuit Satisfiability in CNF Form

## What is CNF?
Conjunctive Normal Form (CNF) is a standardized way of writing Boolean formulas. In CNF, the formula is always structured as:
1. A chain of clauses connected by AND (∧)
2. Each clause is exactly three literals connected by OR (∨)
3. Each literal is either a variable or its negation

The structure is always: (a ∨ b ∨ c) ∧ (d ∨ e ∨ f) ∧ (g ∨ h ∨ i) ∧ ...
where a, b, c, d, e, f, g, h, i are either variables (x₁, x₂, etc.) or their negations (¬x₁, ¬x₂, etc.)

### CNF Structure Rules:
- The TOP level is always AND (∧) operations
- The INNER level is always OR (∨) operations with exactly 3 literals
- Negations (¬) can only appear on individual variables
- No other arrangement or nesting of operations is allowed

### Example:
```
(x₁ ∨ x₂ ∨ x₃) ∧ (¬x₁ ∨ x₂ ∨ x₄) ∧ (x₂ ∨ ¬x₃ ∨ ¬x₄)
```

This formula has:
- 3 clauses connected by AND (∧)
- Each clause has exactly 3 literals connected by OR (∨)
- Uses variables x₁, x₂, x₃, x₄ and their negations

## Properties of CNF SAT:
1. Each variable can appear multiple times across different clauses
2. Each variable can appear only once per clause (no `(x₁ ∨ x₁ ∨ x₂)`)
3. A variable and its negation can appear in the same clause (like `(x₁ ∨ ¬x₁ ∨ x₂)`)
4. The formula is satisfiable if there exists an assignment of TRUE/FALSE to the variables that makes the entire formula TRUE

## Why CNF for Circuit SAT?
1. CNF is a standard form that can express any Boolean formula
2. The 3-SAT problem in CNF form is NP-complete
3. Many efficient SAT solvers are designed to work with CNF formulas
4. The fixed structure (AND of ORs) makes it easier to process and analyze 

## Why is 3-CNF SAT NP-Hard?
3-CNF SAT is NP-hard because:

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
   - 3-CNF SAT is a canonical NP-complete problem
   - All other NP problems can be reduced to 3-CNF SAT
   - If we could solve 3-CNF SAT efficiently, we could solve all NP problems efficiently
   - No polynomial-time solution is known

4. **Example of Complexity**:
   For the formula: (x₁ ∨ x₂ ∨ x₃) ∧ (¬x₁ ∨ x₂ ∨ x₄) ∧ (x₂ ∨ ¬x₃ ∨ ¬x₄)
   - Setting x₁=TRUE satisfies first clause
   - This affects how we might satisfy the second clause
   - These dependencies create complex constraint satisfaction problems 