from Functions.steps import resoudrePuzzle
from Functions.steps import trouverDeuxiemeSolution

filename = "easy_2nd_sol"
filename1 = "easy_var_1"
filename2 = "easy_var_2"
variant = 0
variant1 = 1
variant2 = 2
result = resoudrePuzzle("easy_2nd_sol", variant)

if result[0] is not None:
    solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data = result
    trouverDeuxiemeSolution(solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data, filename, variant)

print ("2 puzzle")
result2 = resoudrePuzzle("easy_var_1",variant1)

if result2[0] is not None:
    solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data = result2
    trouverDeuxiemeSolution(solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data, filename1, variant1)
result3 = resoudrePuzzle("easy_var_2",variant2)
print ("3 puzzle")
if result3[0] is not None:
    solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data = result3
    trouverDeuxiemeSolution(solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data, filename2, variant2)


