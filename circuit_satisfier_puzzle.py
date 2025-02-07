import random
from typing import List, Dict

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

def generate_and_display(size: int):
    # Size determines both number of available variables and number of clauses
    num_inputs = size
    if num_inputs < 2:
        num_inputs = 2
    
    # Number of clauses equals the size
    circuit = generate_circuit(num_inputs, size)
    print("Generated circuit:")
    print(str(circuit))
    
    # Collect input values and evaluate
    input_values = collect_input_values(circuit)
    result = circuit.evaluate(input_values)
    print(f"\nCircuit evaluates to: {result}")

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