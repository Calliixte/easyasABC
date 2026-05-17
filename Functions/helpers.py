from pysat.solvers import Glucose3
from pysat.formula import CNF
import json
# i,j coordonnées de la case, l indice de la lettre, n taille de la grille, nb_lettre nombre de lettres différentes
def var_index(i, j, l, n, nb_lettre):
    return 1 + (i * n + j) * nb_lettre + l


def check_letter(
    headers, i, j, lettre,grille
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


def check_any_letter(headers, i, j,grille):  # verifie si une lettre est plaçable en i,j
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
def place_letter(headers, i, j,grille):
    lettre = check_any_letter(headers, i, j,grille)
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

def atLeastTwo_list(f, var_list):
    n = len(var_list)
    # Pour chaque élément i, on crée une clause contenant tous les AUTRES éléments
    for i in range(n):
        for j in range(n):
            if j != i:
                f.write(f"{var_list[j]} ")
        f.write("0\n")
        
def atMostOne_list(f, var_list):

    for i in range(len(var_list)):

        for j in range(i + 1, len(var_list)):

            atMostOne(f, var_list[i], var_list[j])


def exactlyOne(clauses, var_list):
    """
    Exactement une variable de var_list est vraie.
    Combine atLeastOne et atMostOne.
    """
    atLeastOne_list(clauses, var_list)
    atMostOne_list(clauses, var_list)


def placePremiereVisible(f, cases_dans_ordre, lk, nbLettres, n, nb_states, EMPTY_IDX):

    # Si la lettre est à la position k, toutes les cases avant DOIVENT être vides
    for k in range(len(cases_dans_ordre)):
        i, j = cases_dans_ordre[k]
        
        for previous in range(k):
            i_av, j_av = cases_dans_ordre[previous]
            f.write(f"-{var_index(i, j, lk, n, nb_states)} {var_index(i_av, j_av, EMPTY_IDX, n, nb_states)} 0\n")