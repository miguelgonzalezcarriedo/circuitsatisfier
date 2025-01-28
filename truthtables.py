import random
from typing import List, Dict, Set
from itertools import product

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
        # Each clause has 2 literals (variables or their negations)
        literals = random.sample(available_inputs, 2)
        # Randomly negate some literals
        negated_literals = [
            Gate('NOT', [lit]) if random.random() < 0.5 else lit 
            for lit in literals
        ]
        clause = Gate('OR', negated_literals)
        clauses.append(clause)
    
    # Join all clauses with AND
    return Gate('AND', clauses)

def collect_input_values(circuit: Gate) -> Dict[int, bool]:
    # Collect all unique input indices
    def gather_inputs(gate: Gate, indices: set):
        if gate.gate_type == 'INPUT':
            indices.add(gate.index)
        for inp in gate.inputs:
            gather_inputs(inp, indices)
    
    input_indices = set()
    gather_inputs(circuit, input_indices)
    
    # Get T/F value for each input
    input_values = {}
    for idx in sorted(input_indices):
        while True:
            val = input(f"Enter t/f for x₍{idx}₎: ").lower()
            if val in ['t', 'f']:
                input_values[idx] = (val == 't')
                break
            print("Please enter 't' or 'f'")
    
    return input_values

def get_input_variables(circuit: Gate) -> Set[int]:
    """Get all unique input variable indices in the circuit."""
    indices = set()
    def gather_inputs(gate: Gate):
        if gate.gate_type == 'INPUT':
            indices.add(gate.index)
        for inp in gate.inputs:
            gather_inputs(inp)
    gather_inputs(circuit)
    return indices

def generate_truth_table(circuit: Gate) -> List[Dict[str, bool]]:
    """Generate a truth table for the circuit."""
    # Get all input variables
    input_vars = sorted(get_input_variables(circuit))
    
    # Generate all possible combinations of True/False for inputs
    rows = []
    for values in product([False, True], repeat=len(input_vars)):
        input_values = dict(zip(input_vars, values))
        result = circuit.evaluate(input_values)
        row = {
            'inputs': input_values,
            'output': result
        }
        rows.append(row)
    
    return rows

def display_truth_table(circuit: Gate, rows: List[Dict[str, bool]], only_satisfiable: bool = False):
    """Display the truth table in a formatted way."""
    input_vars = sorted(get_input_variables(circuit))
    
    # Filter rows if only showing satisfiable cases
    if only_satisfiable:
        rows = [row for row in rows if row['output']]
    
    # Create header
    headers = [f"x₍{i}₎" for i in input_vars] + ["Result"]
    col_width = max(len(h) for h in headers) + 2
    
    # Print circuit
    if not only_satisfiable:
        print("\nCircuit:")
        print(str(circuit))
    
    # Print table header
    print("\n" + ("Satisfiable Cases:" if only_satisfiable else "Truth Table:"))
    print("-" * (col_width * (len(headers))))
    header_row = "".join(h.ljust(col_width) for h in headers)
    print(header_row)
    print("-" * (col_width * (len(headers))))
    
    # Print table rows
    for row in rows:
        values = [str(row['inputs'][i]).ljust(col_width) for i in input_vars]
        values.append(str(row['output']).ljust(col_width))
        print("".join(values))
    print("-" * (col_width * (len(headers))))
    
    if only_satisfiable:
        print(f"\nTotal satisfiable cases: {len(rows)}")

def generate_and_display(size: int):
    # Size determines both number of available variables and number of clauses
    num_inputs = size
    if num_inputs < 2:
        num_inputs = 2
    
    # Number of clauses equals the size
    circuit = generate_circuit(num_inputs, size)
    print("Generated circuit:")
    print(str(circuit))
    
    # Generate truth table rows
    rows = generate_truth_table(circuit)
    
    # Display both tables
    display_truth_table(circuit, rows)
    display_truth_table(circuit, rows, only_satisfiable=True)

if __name__ == "__main__":
    while True:
        try:
            size = int(input("Enter circuit size (or 0 to exit): "))
            if size == 0:
                break
            if size < 2:
                print("Please enter a size of at least 2")
                continue
                
            generate_and_display(size)
                
        except ValueError:
            print("Please enter a valid number") 