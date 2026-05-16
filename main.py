from pysat.solvers import Glucose3
from pysat.formula import CNF
import json


def var_index(i, j, l, n, nb_lettre):
    return 1 + (i * n + j) * nb_lettre + l


def check_letter(
    headers, i, j, lettre
):  # verifie si lettre est en i,j selon les headers
    # on part du principe que les grilles données sont valides, sinon il faudrait vérifier une contradiction possible au niveau des lettres données (par exemple un coin ou on aurait A a gauche et B au dessus)
    headers_to_check = {}
    if i == 0:
        headers_to_check["top"] = headers["top"]
    if j == 0:
        headers_to_check["left"] = headers["left"]
    if i == len(grille) - 1:
        headers_to_check["down"] = headers["down"]
    if j == len(grille[i]) - 1:
        headers_to_check["right"] = headers["right"]

    for position, header in headers_to_check.items():
        cord = -1

        if position in [
            "top",
            "down",
        ]:  # vérifie si le header est au dessus/dessous ou sur le coté pour savoir s'il faut utiliser i ou j pour trouver la case correspondante
            cord = j
        else:  # pour left right
            cord = i

        if cord == -1:
            raise Exception("cord inconnue erreur")

        lettre_current = header[cord]
        if lettre_current == lettre:
            return lettre_current
    return "."


def check_any_letter(headers, i, j):  # verifie si une lettre est plaçable en i,j
    # on part du principe que les grilles données sont valides, sinon il faudrait vérifier une contradiction possible au niveau des lettres données (par exemple un coin ou on aurait A a gauche et B au dessus)
    headers_to_check = {}
    if i == 0:
        headers_to_check["top"] = headers["top"]
    if j == 0:
        headers_to_check["left"] = headers["left"]
    if i == len(grille) - 1:
        headers_to_check["down"] = headers["down"]
    if j == len(grille[i]) - 1:
        headers_to_check["right"] = headers["right"]

    for position, header in headers_to_check.items():
        cord = -1

        if position in [
            "top",
            "down",
        ]:  # vérifie si le header est au dessus/dessous ou sur le coté pour savoir s'il faut utiliser i ou j pour trouver la case correspondante
            cord = j
        else:  # pour left right
            cord = i

        if cord == -1:
            raise Exception("cord inconnue erreur")

        lettre = header[cord]
        if lettre != ".":
            return lettre
    return "."


# essaye de placer une lettre en i,j en fonction de headers donnés
# renvoie true si une lettre a été placée
def place_letter(headers, i, j):
    lettre = check_any_letter(headers, i, j)
    if lettre != ".":
        print(lettre, end="")
        return True
    return False


# ======== contraintes de bases ============#
def atLeastOne(
    f, startNumber, endNumber
):  # je passe le fd au lieu du path car ça causait des problemes de pointeurs d'ouvrir plusieurs fois le fichier
    cpt = startNumber
    while cpt < endNumber:
        f.write(f"{cpt} ")
        cpt += 1
    f.write("0\n")


def atMostOne(f, x, y):
    f.write(f"-{x} -{y} 0\n")


def atMostOne_range(f, startNumber, endNumber):
    for i in range(startNumber, endNumber):
        for j in range(i + 1, endNumber):
            atMostOne(f, i, j)


def atLeastOne_list(f, var_list):

    for v in var_list:

        f.write(f"{v} ")

    f.write("0\n")


def atMostOne_list(f, var_list):

    for i in range(len(var_list)):

        for j in range(i + 1, len(var_list)):

            atMostOne(f, var_list[i], var_list[j])


def exactlyOne(clauses, var_list):
    """
    Exactement une variable de var_list est vraie.
    → Combiner atLeastOne et atMostOne.
    """
    atLeastOne_list(clauses, var_list)
    atMostOne_list(clauses, var_list)


# regarde la premeier lettre visible a place (si il y a des cases vide)
def placePremiereVisible(f, cases_dans_ordre, lk, nbLettres, n, nb_states, EMPTY_IDX):

    for k in range(len(cases_dans_ordre)):

        i, j = cases_dans_ordre[k]

        for l_prime in range(nbLettres):

            if l_prime == lk:
                continue

            # mauvaise lettre
            f.write(f"-{var_index(i,j,l_prime,n,nb_states)} ")

            # cases avant vides
            for previous in range(k):

                i_av, j_av = cases_dans_ordre[previous]

                f.write(f"-{var_index(i_av,j_av,EMPTY_IDX,n,nb_states)} ")

            f.write("0\n")


# -------------- Main -----------------


filename = "easy1"


# vérifie si le fichier cnf correspondant au puzzle donné existe, s'il n'existe pas, le créer
try:
    open(f"DIMACS/{filename}.cnf")
except:
    open(f"DIMACS/{filename}.cnf", "x")

firstPass = True
variableCount = 1  # init a 1 pour le solver


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


# AFFICHAGE SOLUTION


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


# RESOLUTION


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
