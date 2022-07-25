
from solver import Solver, Problem
from brute import Brute
from ga import GA

jsonFile = "small_input.json"
jsonFile = input(f'Enter input file (default => {jsonFile}):') or jsonFile
algorithms = {'b':Brute,'g':GA}
problem = Problem(jsonFile)
algorithm = input(f'Select the algorithm (Brute-Force (b) / Genetic Algorithm (g)) (default => (Brute-Force)):') or 'b'
match algorithm:
    case 'g':
        solverClass = GA
    case _ :
        solverClass = Brute
print("Processing...")
solver = Solver.solve(problem, solverClass)
print("Done...")
