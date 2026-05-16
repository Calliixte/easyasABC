from pysat.solvers import Glucose3
from pysat.formula import CNF
import json

from Functions.helpers import var_index, atLeastOne, atMostOne, atMostOne_range, atLeastOne_list, atMostOne_list, exactlyOne, placePremiereVisible

"""
Fonction qui récupère une entrée définissant une instance du puzzle, et qui crée un fichier DIMACS représentant l'instance
"""
def genererDIMACS(filename, variant=0):

    with open(f"Puzzles/{filename}.json") as fin:

        puzzle_data = json.load(fin)

    headers = puzzle_data["headers"]

    grille = puzzle_data["grid"]

    letters = puzzle_data.get("letters", ["A", "B", "C", "D", "E", "F"])

    n = len(grille)

    has_empty = variant > 0

    nb_empties = variant

    EMPTY_IDX = len(letters)

    nb_states = len(letters)

    if has_empty:

        nb_states += 1

    nb_vars = n * n * nb_states

    clause_count = 0

    with open(f"DIMACS/{filename}.cnf", "w") as f:

        # ligne temporaire
        f.write("p cnf 0 0\n")

        # ====================================================
        # EXACTEMENT UNE VALEUR PAR CASE
        # ====================================================

        variableCount = 1

        for i in range(n):

            for j in range(n):

                start = variableCount

                for l in range(nb_states):

                    variableCount += 1

                end = variableCount

                atLeastOne(f, start, end)

                atMostOne_range(f, start, end)

                clause_count += 1

                clause_count += ((end - start) * ((end - start) - 1)) // 2

        # ====================================================
        # AU PLUS UNE FOIS PAR LIGNE
        # ====================================================

        for i in range(n):

            for l in range(len(letters)):

                row_vars = []

                for j in range(n):

                    row_vars.append(var_index(i, j, l, n, nb_states))

                atMostOne_list(f, row_vars)

                clause_count += (len(row_vars) * (len(row_vars) - 1)) // 2

        # ====================================================
        # AU PLUS UNE FOIS PAR COLONNE
        # ====================================================

        for j in range(n):

            for l in range(len(letters)):

                col_vars = []

                for i in range(n):

                    col_vars.append(var_index(i, j, l, n, nb_states))

                atMostOne_list(f, col_vars)

                clause_count += (len(col_vars) * (len(col_vars) - 1)) // 2

        # ====================================================
        # AU MOINS UNE FOIS PAR LIGNE
        # ====================================================

        for i in range(n):

            for l in range(len(letters)):

                row_vars = []

                for j in range(n):

                    row_vars.append(var_index(i, j, l, n, nb_states))

                atLeastOne_list(f, row_vars)

                clause_count += 1

        # ====================================================
        # AU MOINS UNE FOIS PAR COLONNE
        # ====================================================

        for j in range(n):

            for l in range(len(letters)):

                col_vars = []

                for i in range(n):

                    col_vars.append(var_index(i, j, l, n, nb_states))

                atLeastOne_list(f, col_vars)

                clause_count += 1

        # ====================================================
        # CONTRAINTES CASES VIDES
        # ====================================================

        if has_empty:

            # ------------------------------------------------
            # LIGNES
            # ------------------------------------------------

            for i in range(n):

                empty_vars = []

                for j in range(n):

                    empty_vars.append(var_index(i, j, EMPTY_IDX, n, nb_states))

                # variante 1
                if nb_empties == 1:

                    for a in range(len(empty_vars)):

                        for b in range(a + 1, len(empty_vars)):

                            f.write(f"-{empty_vars[a]} ")

                            f.write(f"-{empty_vars[b]} 0\n")

                            clause_count += 1

                # variante 2
                elif nb_empties == 2:

                    for a in range(len(empty_vars)):

                        for b in range(a + 1, len(empty_vars)):

                            for c in range(b + 1, len(empty_vars)):

                                f.write(f"-{empty_vars[a]} ")

                                f.write(f"-{empty_vars[b]} ")

                                f.write(f"-{empty_vars[c]} 0\n")

                                clause_count += 1

            # ------------------------------------------------
            # COLONNES
            # ------------------------------------------------

            for j in range(n):

                empty_vars = []

                for i in range(n):

                    empty_vars.append(var_index(i, j, EMPTY_IDX, n, nb_states))

                # variante 1
                if nb_empties == 1:

                    for a in range(len(empty_vars)):

                        for b in range(a + 1, len(empty_vars)):

                            f.write(f"-{empty_vars[a]} ")

                            f.write(f"-{empty_vars[b]} 0\n")

                            clause_count += 1

                # variante 2
                elif nb_empties == 2:

                    for a in range(len(empty_vars)):

                        for b in range(a + 1, len(empty_vars)):

                            for c in range(b + 1, len(empty_vars)):

                                f.write(f"-{empty_vars[a]} ")

                                f.write(f"-{empty_vars[b]} ")

                                f.write(f"-{empty_vars[c]} 0\n")

                                clause_count += 1

        # ====================================================
        # CASES PRE-REMPLIES
        # ====================================================

        for i in range(n):

            for j in range(n):

                cell = grille[i][j]

                if cell in letters:

                    l = letters.index(cell)

                    f.write(f"{var_index(i,j,l,n,nb_states)} 0\n")

                    clause_count += 1

                elif cell == "X" and has_empty:

                    f.write(f"{var_index(i,j,EMPTY_IDX,n,nb_states)} 0\n")

                    clause_count += 1

        # INDICES DE BORD

        for j in range(n):

            # TOP
            hint = headers["top"][j]

            if hint != ".":

                l = letters.index(hint)

                if not has_empty:

                    f.write(f"{var_index(0,j,l,n,nb_states)} 0\n")

                    clause_count += 1

                else:

                    cases = []

                    for i in range(n):

                        cases.append((i, j))

                    placePremiereVisible(
                        f, cases, l, len(letters), n, nb_states, EMPTY_IDX
                    )

                    clause_count += n * (len(letters) - 1)

            # DOWN
            hint = headers["down"][j]

            if hint != ".":

                l = letters.index(hint)

                if not has_empty:

                    f.write(f"{var_index(n-1,j,l,n,nb_states)} 0\n")

                    clause_count += 1

                else:

                    cases = []

                    for i in range(n - 1, -1, -1):

                        cases.append((i, j))

                    placePremiereVisible(
                        f, cases, l, len(letters), n, nb_states, EMPTY_IDX
                    )

                    clause_count += n * (len(letters) - 1)

        for i in range(n):

            # LEFT
            hint = headers["left"][i]

            if hint != ".":

                l = letters.index(hint)

                if not has_empty:

                    f.write(f"{var_index(i,0,l,n,nb_states)} 0\n")

                    clause_count += 1

                else:

                    cases = []

                    for j in range(n):

                        cases.append((i, j))

                    placePremiereVisible(
                        f, cases, l, len(letters), n, nb_states, EMPTY_IDX
                    )

                    clause_count += n * (len(letters) - 1)

            # RIGHT
            hint = headers["right"][i]

            if hint != ".":

                l = letters.index(hint)

                if not has_empty:

                    f.write(f"{var_index(i,n-1,l,n,nb_states)} 0\n")

                    clause_count += 1

                else:

                    cases = []

                    for j in range(n - 1, -1, -1):

                        cases.append((i, j))

                    placePremiereVisible(
                        f, cases, l, len(letters), n, nb_states, EMPTY_IDX
                    )

                    clause_count += n * (len(letters) - 1)

    # REECRITURE ENTETE DIMACS

    with open(f"DIMACS/{filename}.cnf", "r") as f:

        contenu = f.readlines()

    contenu[0] = f"p cnf {nb_vars} {clause_count}\n"

    with open(f"DIMACS/{filename}.cnf", "w") as f:

        f.writelines(contenu)

    print(f"[1] DIMACS genere")

    print(f"Variables : {nb_vars}")

    print(f"Clauses : {clause_count}")

    return n, letters, nb_states, EMPTY_IDX, puzzle_data

"""
Fonction qui, à partir de la trace produite par le SAT solveur (glucose), affiche la solution du problème, à savoir la grille remplie
"""
def afficherSolution(model, n, letters, nb_states, EMPTY_IDX, headers, has_empty):

    model_set = set(model)

    grille_resolue = []

    for i in range(n):

        ligne = []

        for j in range(n):

            for l in range(nb_states):

                v = var_index(i, j, l, n, nb_states)

                if v in model_set:

                    if has_empty and l == EMPTY_IDX:

                        ligne.append(".")

                    else:

                        ligne.append(letters[l])

                    break

        grille_resolue.append(ligne)

    top = headers["top"]
    down = headers["down"]
    left = headers["left"]
    right = headers["right"]

    sep = "  +" + "-" * (2 * n - 1) + "+"

    print()

    print("   " + " ".join(top))

    print(sep)

    for i in range(n):

        print(f" {left[i]}|" + " ".join(grille_resolue[i]) + f"|{right[i]}")

    print(sep)

    print("   " + " ".join(down))

    print()


"""
Fonction enchaînant automatiquement les etapes de création d'un fichier DIMACS et d'affichage de la solution ainsi que l’appel au SAT solveur 
"""
def resoudrePuzzle(filename, variant=0):

    n, letters, nb_states, EMPTY_IDX, puzzle_data = genererDIMACS(filename, variant)

    formula = CNF(from_file=f"DIMACS/{filename}.cnf")

    solver = Glucose3(bootstrap_with=formula)

    if solver.solve():

        print("[2] SAT")

        model = solver.get_model()

        afficherSolution(
            model, n, letters, nb_states, EMPTY_IDX, puzzle_data["headers"], variant > 0
        )

        return (solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data)

    else:

        print("[2] UNSAT")

        solver.delete()

        return None, None, n, letters, nb_states, EMPTY_IDX, puzzle_data

