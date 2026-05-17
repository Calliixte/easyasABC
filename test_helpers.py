import io 
from Functions.helpers import *


## Test de la fonction var_index qui calcule l'indice d'une variable pour une case donnée et une lettre donnée
def test_var_index():
    assert var_index(0, 0, 0, 3, 3) == 1
    assert var_index(0, 0, 0, 3, 4) == 1
    #case lettre si case empty dans la grille
    assert var_index(1, 1, 1, 3, 4) == 18
    # case empty
    assert var_index(1, 1, 4, 3, 4) == 21


def test_check_letter_and_any_and_place():
    grille = [["."] * 3 for _ in range(3)]
    headers = {"top": "..A", "left": "A..", "down": "...", "right": "..."}

    # case en bord haut-droite -> top[2] == 'A'
    assert check_letter(headers, 0, 2, "A",grille) == "A"
    # case interne -> pas de lettre imposée
    assert check_letter(headers, 1, 1, "A",grille) == "."

    # check_any_letter retourne la première lettre non '.'
    assert check_any_letter(headers, 0, 0,grille) == "A"

    # place_letter imprime la lettre et renvoie True
    assert place_letter(headers, 0, 0,grille) is True


def test_atLeastOne_and_variants():
    f = io.StringIO()
    atLeastOne(f, 1, 4)
    assert f.getvalue() == "1 2 3 0\n"

    f = io.StringIO()
    atLeastOne(f, 1, 2)
    assert f.getvalue() == "1 0\n"

    f = io.StringIO()
    atMostOne(f, 2, 3)
    assert f.getvalue() == "-2 -3 0\n"

    f = io.StringIO()
    atMostOne_range(f, 1, 2)
    assert f.getvalue() == ""

    f = io.StringIO()
    atMostOne_range(f, 1, 4)
    assert f.getvalue() == "-1 -2 0\n-1 -3 0\n-2 -3 0\n"

    f = io.StringIO()
    atLeastOne_list(f, [5, 6, 7])
    assert f.getvalue() == "5 6 7 0\n"

    f = io.StringIO()
    atLeastTwo_list(f, [1, 2, 3])
    assert f.getvalue() == "2 3 0\n1 3 0\n1 2 0\n"

    f = io.StringIO()
    atMostOne_list(f, [1, 2, 3])
    assert f.getvalue() == "-1 -2 0\n-1 -3 0\n-2 -3 0\n"


def test_exactlyOne_combines_constraints():
    f = io.StringIO()
    exactlyOne(f, [9, 10])
    assert f.getvalue() == "9 10 0\n-9 -10 0\n"


def test_placePremiereVisible_writes_clauses():
    f = io.StringIO()
    cases = [(0, 0), (0, 1)]
    n = 2
    nb_states = 2
    EMPTY_IDX = 2
    lk = 0

    placePremiereVisible(f, cases, lk, nb_states, n, nb_states, EMPTY_IDX)

    # vérifier qu'au moins une clause correspond à la forme attendue
    v1 = var_index(0, 1, lk, n, nb_states)
    v2 = var_index(0, 0, EMPTY_IDX, n, nb_states)
    assert f.getvalue().strip().splitlines()[-1] == f"-{v1} {v2} 0"

    f = io.StringIO()
    cases = [(0, 0), (0, 1)]
    n = 2
    nb_states = 2
    EMPTY_IDX = 0
    lk = 2

    placePremiereVisible(f, cases, lk, nb_states, n, nb_states, EMPTY_IDX)

    # vérifier qu'au moins une clause correspond à la forme attendue
    v1 = var_index(0, 1, lk, n, nb_states)
    v2 = var_index(0, 0, EMPTY_IDX, n, nb_states)
    assert f.getvalue().strip().splitlines()[-1] == f"-{v1} {v2} 0"

    f = io.StringIO()
    cases = [(0, 0), (0, 1)]
    n = 2
    nb_states = 2
    EMPTY_IDX = 1
    lk = 1

    placePremiereVisible(f, cases, lk, nb_states, n, nb_states, EMPTY_IDX)

    # vérifier qu'au moins une clause correspond à la forme attendue
    v1 = var_index(0, 1, lk, n, nb_states)
    v2 = var_index(0, 0, EMPTY_IDX, n, nb_states)
    assert f.getvalue().strip().splitlines()[-1] == f"-{v1} {v2} 0"
