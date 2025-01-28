from typing import List, Tuple

def generate_pigeonhole(pigeons: int, holes: int) -> List[Tuple[List[int], List[int]]]:
    """
    Generate a SAT formula encoding the pigeonhole principle:
    - Each pigeon must be in at least one hole
    - No hole can contain more than one pigeon
    
    Variables are encoded as: x₍i,j₎ means pigeon i is in hole j
    Variable number = (i-1)*holes + j
    """
    clauses = []
    
    # 1. Each pigeon must be in at least one hole
    for p in range(1, pigeons + 1):
        # Create clause: (x₍p,1₎ ∨ x₍p,2₎ ∨ ... ∨ x₍p,h₎)
        variables = [(p-1)*holes + h for h in range(1, holes + 1)]
        clauses.append((variables, []))  # All positive literals
    
    # 2. No hole can contain more than one pigeon
    for h in range(1, holes + 1):
        for p1 in range(1, pigeons):
            for p2 in range(p1 + 1, pigeons + 1):
                # Create clause: (¬x₍p1,h₎ ∨ ¬x₍p2,h₎)
                # If two pigeons are in same hole, formula is false
                var1 = (p1-1)*holes + h
                var2 = (p2-1)*holes + h
                clauses.append(([], [var1, var2]))  # All negative literals
    
    return clauses

def format_pigeonhole_clause(clause: Tuple[List[int], List[int]], holes: int) -> str:
    """Format a pigeonhole clause in readable form."""
    pos_lits, neg_lits = clause
    
    def var_to_ph(var: int) -> str:
        """Convert variable number to (pigeon,hole) representation."""
        var -= 1  # Convert to 0-based
        p = var // holes + 1
        h = var % holes + 1
        return f"x₍{p},{h}₎"
    
    terms = []
    for var in pos_lits:
        terms.append(var_to_ph(var))
    for var in neg_lits:
        terms.append(f"¬{var_to_ph(var)}")
    
    return "(" + " ∨ ".join(terms) + ")"

def demonstrate_pigeonhole():
    print("Pigeonhole Principle SAT Formula Generator")
    print("This generates formulas proving you can't put n pigeons in m holes where n > m")
    
    while True:
        try:
            pigeons = int(input("\nEnter number of pigeons (or 0 to exit): "))
            if pigeons == 0:
                break
            
            holes = int(input("Enter number of holes: "))
            if pigeons <= 0 or holes <= 0:
                print("Please enter positive numbers")
                continue
            
            clauses = generate_pigeonhole(pigeons, holes)
            
            print(f"\nGenerated formula for {pigeons} pigeons and {holes} holes:")
            print("Each variable x₍i,j₎ means 'pigeon i is in hole j'")
            print("Formula (in CNF):")
            formula = " ∧ ".join(format_pigeonhole_clause(c, holes) for c in clauses)
            print(formula)
            
            print(f"\nNumber of variables: {pigeons * holes}")
            print(f"Number of clauses: {len(clauses)}")
            
            if pigeons > holes:
                print("\nThis formula is UNSATISFIABLE (pigeons > holes)")
                print("But proving this requires exponential time for SAT solvers!")
            else:
                print("\nThis formula is SATISFIABLE (pigeons ≤ holes)")
            
        except ValueError:
            print("Please enter valid numbers")

if __name__ == "__main__":
    demonstrate_pigeonhole() 