from typing import List, Dict, Set, Tuple, Optional
import itertools
import random
from enum import Enum

class Gate:
    def __init__(self, gate_type: str, inputs: List['Gate'] = None, label: str = None, index: int = None):
        self.gate_type = gate_type
        self.inputs = inputs if inputs else []
        self.label = label
        self.index = index

    def __str__(self):
        if self.gate_type == 'INPUT':
            return f"x₍{self.index}₎"
        elif self.gate_type == 'NOT':
            return f"¬{self.inputs[0]}"
        else:
            op = ' ∧ ' if self.gate_type == 'AND' else ' ∨ '
            return f"({op.join(str(inp) for inp in self.inputs)})"
    
    def evaluate(self, input_values: Dict[int, bool]) -> bool:
        if self.gate_type == 'INPUT':
            return input_values[self.index]
        elif self.gate_type == 'NOT':
            return not self.inputs[0].evaluate(input_values)
        elif self.gate_type == 'AND':
            return all(inp.evaluate(input_values) for inp in self.inputs)
        elif self.gate_type == 'OR':
            return any(inp.evaluate(input_values) for inp in self.inputs)
        raise ValueError(f"Unknown gate type: {self.gate_type}")

def generate_circuit(num_inputs: int, num_clauses: int) -> Gate:
    # Create pool of available input gates
    available_inputs = [Gate('INPUT', label=f'x{i+1}', index=i+1) for i in range(num_inputs)]
    
    # For CNF form, we need:
    # 1. Exactly size number of clauses joined by AND
    # 2. Each clause is variables/negations joined by OR
    
    # Create clauses
    clauses = []
    for _ in range(num_clauses):
        # Each clause has 3 literals (variables or their negations)
        literals = random.sample(available_inputs, 3)
        # Randomly negate some literals
        negated_literals = [
            Gate('NOT', [lit]) if random.random() < 0.5 else lit 
            for lit in literals
        ]
        clause = Gate('OR', negated_literals)
        clauses.append(clause)
    
    # Join all clauses with AND
    return Gate('AND', clauses)

def gate_to_cnf_clauses(circuit: Gate) -> List[Tuple[List[int], List[int]]]:
    """Convert a Gate circuit to CNF clause representation."""
    if circuit.gate_type != 'AND':
        raise ValueError("Top level gate must be AND for CNF form")
    
    clauses = []
    for clause in circuit.inputs:
        if clause.gate_type != 'OR':
            raise ValueError("Second level gates must be OR for CNF form")
        
        positive_literals = []
        negative_literals = []
        
        for literal in clause.inputs:
            if literal.gate_type == 'INPUT':
                positive_literals.append(literal.index)
            elif literal.gate_type == 'NOT':
                if literal.inputs[0].gate_type != 'INPUT':
                    raise ValueError("Negation can only be applied to input variables in CNF")
                negative_literals.append(literal.inputs[0].index)
            else:
                raise ValueError("Invalid literal type in CNF clause")
        
        clauses.append((positive_literals, negative_literals))
    
    return clauses

class VarState(Enum):
    UNKNOWN = 0  # Can be either True or False
    MUST_TRUE = 1
    MUST_FALSE = 2
    CONFLICT = 3  # Variable has conflicting requirements

class ConstraintSet:
    def __init__(self):
        self.var_states: Dict[int, VarState] = {}
    
    def copy(self) -> 'ConstraintSet':
        new_set = ConstraintSet()
        new_set.var_states = self.var_states.copy()
        return new_set
    
    def get_state(self, var: int) -> VarState:
        return self.var_states.get(var, VarState.UNKNOWN)
    
    def set_state(self, var: int, state: VarState) -> bool:
        """Set variable state. Returns False if this creates a conflict."""
        current = self.get_state(var)
        
        if current == state or current == VarState.UNKNOWN:
            self.var_states[var] = state
            return True
        
        # If we get here, we have a conflict
        self.var_states[var] = VarState.CONFLICT
        return False
    
    def to_assignment(self) -> Optional[Dict[int, bool]]:
        """Convert constraints to a satisfying assignment if possible."""
        result = {}
        for var, state in sorted(self.var_states.items()):
            if state == VarState.CONFLICT:
                return None
            elif state == VarState.MUST_TRUE:
                result[var] = True
            elif state == VarState.MUST_FALSE:
                result[var] = False
            else:  # UNKNOWN - we can choose either value
                result[var] = True  # Default to True for unknowns
        return result

def propagate_clause(clause: Tuple[List[int], List[int]], constraints: ConstraintSet) -> List[ConstraintSet]:
    """
    Propagate constraints from a clause.
    Returns list of possible constraint sets that satisfy this clause.
    """
    pos_lits, neg_lits = clause
    current_state = constraints.copy()
    
    # First check if clause is already satisfied by current constraints
    for var in pos_lits:
        if current_state.get_state(var) == VarState.MUST_TRUE:
            return [current_state]
    for var in neg_lits:
        if current_state.get_state(var) == VarState.MUST_FALSE:
            return [current_state]
    
    # If not satisfied, we need to try all possible ways to satisfy it
    result = []
    
    # Try satisfying with each positive literal
    for var in pos_lits:
        if current_state.get_state(var) != VarState.MUST_FALSE:
            new_state = current_state.copy()
            if new_state.set_state(var, VarState.MUST_TRUE):
                result.append(new_state)
    
    # Try satisfying with each negative literal
    for var in neg_lits:
        if current_state.get_state(var) != VarState.MUST_TRUE:
            new_state = current_state.copy()
            if new_state.set_state(var, VarState.MUST_FALSE):
                result.append(new_state)
    
    return result

def satisfy_cnf(clauses: List[Tuple[List[int], List[int]]]) -> Dict[int, bool]:
    """
    Try to satisfy a CNF formula using constraint propagation.
    Returns a satisfying assignment if one exists, None otherwise.
    """
    if not clauses:
        return {}
    
    # Start with empty constraint set
    possible_constraints = [ConstraintSet()]
    
    # Process each clause
    for i, clause in enumerate(clauses):
        new_constraints = []
        
        # For each existing set of constraints
        for constraints in possible_constraints:
            # Propagate the new clause
            new_sets = propagate_clause(clause, constraints)
            new_constraints.extend(new_sets)
        
        possible_constraints = new_constraints
        
        # Display current state
        print(f"\nAfter clause {i + 1}:")
        print(f"Number of possible constraint sets: {len(possible_constraints)}")
        if possible_constraints:
            print("Example constraint set:")
            for var, state in sorted(possible_constraints[0].var_states.items()):
                print(f"x₍{var}₎: {state.name}")
        
        # If no possible constraints left, formula is unsatisfiable
        if not possible_constraints:
            return None
    
    # Convert first satisfying constraint set to assignment
    return possible_constraints[0].to_assignment()

def format_truth_table(assignments: List[Dict[int, bool]], clause_num: int) -> str:
    """Format a list of assignments as a readable truth table."""
    if not assignments:
        return "No satisfying assignments"
    
    # Get all variables used
    variables = set()
    for assignment in assignments:
        variables.update(assignment.keys())
    variables = sorted(variables)
    
    # Create header
    header = " | ".join(f"x₍{var}₎" for var in variables)
    separator = "-" * len(header)
    
    # Create rows
    rows = []
    for assignment in assignments:
        row = " | ".join("T" if assignment.get(var, False) else "F" for var in variables)
        rows.append(row)
    
    return f"\nTruth table after clause {clause_num}:\n{header}\n{separator}\n" + "\n".join(rows)

def format_assignment(assignment: Dict[int, bool]) -> str:
    """Format an assignment as a readable string."""
    if assignment is None:
        return "No solution exists"
    
    return ", ".join(f"x₍{var}₎ = {value}" for var, value in sorted(assignment.items()))

def collect_circuit_variables(circuit: Gate) -> Set[int]:
    """Collect all variable indices used in the circuit."""
    variables = set()
    
    def gather_vars(gate: Gate):
        if gate.gate_type == 'INPUT':
            variables.add(gate.index)
        for inp in gate.inputs:
            gather_vars(inp)
    
    gather_vars(circuit)
    return variables

def generate_and_solve(size: int):
    """Generate a random CNF circuit and find a satisfying assignment."""
    # Generate circuit
    circuit = generate_circuit(size, size)
    print(f"\nGenerated circuit (size {size}):")
    print(str(circuit))
    print("\nSolving...")
    
    # Get all variables in the circuit
    all_variables = collect_circuit_variables(circuit)
    
    # Convert to CNF clauses
    clauses = gate_to_cnf_clauses(circuit)
    
    # Find solution
    result = satisfy_cnf(clauses)
    
    # If we found a solution, make sure all circuit variables are assigned
    if result is not None:
        # Add any missing variables with default value True
        for var in all_variables:
            if var not in result:
                result[var] = True
    
    print("\nFinal solution:", format_assignment(result))
    
    # Verify solution
    if result:
        print("Verifying solution...")
        print("Circuit evaluates to:", circuit.evaluate(result))

if __name__ == "__main__":
    print("This program will demonstrate how the number of solutions decreases with circuit size.")
    print("Each size will show the number of satisfying assignments after each clause is added.")
    
    while True:
        try:
            size = int(input("\nEnter circuit size (or 0 to exit): "))
            if size == 0:
                break
            if size < 2:
                print("Please enter a size of at least 2")
                continue
                
            generate_and_solve(size)
                
        except ValueError as e:
            if str(e):
                print(f"Error: {e}")
            else:
                print("Please enter a valid number") 