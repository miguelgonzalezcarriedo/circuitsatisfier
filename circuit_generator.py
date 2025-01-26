import random
from typing import List

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

def generate_circuit(num_inputs: int, max_gates: int) -> Gate:
    # Create input gates with subscript indices
    inputs = [Gate('INPUT', label=f'x{i+1}', index=i+1) for i in range(num_inputs)]
    gates = inputs.copy()
    
    # Generate a more structured circuit with clauses
    clauses = []
    num_clauses = random.randint(2, max_gates)
    
    for _ in range(num_clauses):
        # Each clause is an OR of two literals
        literals = random.sample(inputs, 2)
        # Randomly negate some literals
        negated_literals = [
            Gate('NOT', [lit]) if random.random() < 0.5 else lit 
            for lit in literals
        ]
        clause = Gate('OR', negated_literals)
        clauses.append(clause)
    
    # Combine all clauses with AND
    final_circuit = Gate('AND', clauses)
    return final_circuit

def generate_and_display(num_inputs: int, max_gates: int):
    circuit = generate_circuit(num_inputs, max_gates)
    print(str(circuit))

if __name__ == "__main__":
    generate_and_display(4, 3) 