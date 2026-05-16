from Functions.steps import resoudrePuzzle
from Functions.steps import trouverDeuxiemeSolution

filename = "easy_2nd_sol"
variant = 0

result = resoudrePuzzle("easy_2nd_sol", variant)

if result[0] is not None:
    solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data = result
    trouverDeuxiemeSolution(solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data, filename, variant)
    
# resoudrePuzzle("easy_var_1",variant=1)
# resoudrePuzzle("easy_var_2",variant=2)
