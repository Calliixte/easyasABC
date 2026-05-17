import json
import os
from Functions.steps import *

# solution puzzle0:
#[
#   ["A","C","B"],
#   ["C","B","A"],
#   ["B","A","C"]
#]
# solution puzzle1:
#[
#   ["A",".","B"],
#   [".","B","A"],
#   ["B","A","."]
#]
# solution puzzle2 :
#[
#   ["A",".","B","."],
#   [".","B",".","A"],
#   ["B",".","A","."],
#   [".","A",".","B"]
#]




## Test de la fonction genererDIMACS avec les 3 variants
def test_genererDIMACS_variant0():
    """Test genererDIMACS avec variant=0 (aucune case vide)"""
    # Test avec test_puzzle0 (3x3)
    n, letters, nb_states, EMPTY_IDX, puzzle_data = genererDIMACS("test_puzzle0", variant=0)
    
    assert n == 3, "test_puzzle0 doit être une grille 3x3"
    assert letters == ['A', 'B','C'], "variant=0: doit avoir 3 lettres (A, B, C)"
    assert nb_states == 3, "nb_states doit être 3"
    assert EMPTY_IDX == 3, "EMPTY_IDX doit être 3"
    assert os.path.exists("DIMACS/test_puzzle0.cnf"), "Le fichier DIMACS doit être créé"


def test_genererDIMACS_variant1():
    """Test genererDIMACS avec variant=1 (1 case vide)"""
    # Test avec test_puzzle1 (3x3)
    n, letters, nb_states, EMPTY_IDX, puzzle_data = genererDIMACS("test_puzzle1", variant=1)
    
    assert n == 3, "test_puzzle1 doit être une grille 3x3"
    assert letters == ['A', 'B'], "variant=1: doit avoir 2 lettres (A, B)"
    assert nb_states == 3, "nb_states doit être 3"
    assert EMPTY_IDX == 2, "EMPTY_IDX doit être 2   "
    assert os.path.exists("DIMACS/test_puzzle1.cnf"), "Le fichier DIMACS doit être créé"


def test_genererDIMACS_variant2():
    """Test genererDIMACS avec variant=2 (2 cases vides)"""
    # Test avec test_puzzle0 (4x4)
    n, letters, nb_states, EMPTY_IDX, puzzle_data = genererDIMACS("test_puzzle2", variant=2)
    
    assert n == 4, "test_puzzle2 doit être une grille 4x4"
    assert letters == ['A','B'], "variant=2: doit avoir 2 lettres"
    assert nb_states == 3, "nb_states doit être 3"
    assert EMPTY_IDX == 2, "EMPTY_IDX doit être 2"
    assert os.path.exists("DIMACS/test_puzzle2.cnf"), "Le fichier DIMACS doit être créé"


def test_afficherSolution(capsys):
    """Test que afficherSolution affiche correctement la solution"""
    # Model pour un puzzle 2x2: positions des variables positives indiquent les vraies valeurs
    # var_index(i, j, l, n, nb_states) = 1 + (i * n + j) * nb_states + l
    # Pour n=2, nb_states=2:
    # (0,0) : indices 1-2
    # (0,1) : indices 3-4
    # (1,0) : indices 5-6
    # (1,1) : indices 7-8
    model = [1, -2, 3, -4, 5, -6, 7, -8]  # A at (0,0), A at (0,1), A at (1,0), A at (1,1)
    n = 2
    letters = ['A', 'B']
    nb_states = 2
    EMPTY_IDX = 2
    headers = {"top": ["A", "B"], "down": ["B", "A"], "left": ["A", "B"], "right": ["B", "A"]}
    has_empty = False
    
    # Juste vérifier qu'il ne lève pas d'exception
    afficherSolution(model, n, letters, nb_states, EMPTY_IDX, headers, has_empty)
    
    captured = capsys.readouterr()
    assert "A" in captured.out or "B" in captured.out, "La solution doit contenir des lettres"


def test_resoudrePuzzle_variant0():
    """Test que resoudrePuzzle résout correctement avec variant=0"""
    result = resoudrePuzzle("test_puzzle0", variant=0)
    
    # test_puzzle0 est un puzzle 3x3 avec 3 lettres (A, B, C) et aucune case vide, donc n=3, nb_states=3, EMPTY_IDX=3
    assert result is not None, "Le puzzle doit avoir une solution"
    assert len(result) == 7, "resoudrePuzzle doit retourner 7 éléments"
    
    solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data = result
    
    assert n == 3, "test_puzzle0 doit avoir n=3"
    assert letters == ['A', 'B', 'C'], "test_puzzle0 doit avoir les 3 lettres"
    assert model is not None, "Le modèle doit exister"
    assert len(model) > 0, "Le modèle doit avoir au moins une variable"


def test_resoudrePuzzle_variant1():
    """Test que resoudrePuzzle résout correctement avec variant=1"""
    result = resoudrePuzzle("test_puzzle1", variant=1)
    
    assert result is not None, "Le puzzle avec variant=1 doit avoir une solution"
    assert len(result) == 7, "resoudrePuzzle doit retourner 7 éléments"
    solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data = result
    
    assert n == 3, "test_puzzle1 doit avoir n=3"
    assert letters == ['A', 'B'], "variant=1: doit avoir 2 lettres (A, B)"
    assert model is not None, "Le modèle doit exister"


def test_resoudrePuzzle_variant2():
    """Test que resoudrePuzzle résout correctement test_puzzle2 avec variant=2"""
    result = resoudrePuzzle("test_puzzle2", variant=2)
    
    assert result is not None, "test_puzzle2 avec variant=2 doit avoir une solution"
    assert len(result) == 7, "resoudrePuzzle doit retourner 7 éléments"
    solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data = result
    
    assert n == 4, "test_puzzle2 doit avoir n=4"
    assert letters == ['A', 'B'], "variant=2: doit avoir 2 lettres (A, B)"
    assert model is not None, "Le modèle doit exister"


def test_trouverDeuxiemeSolution_variant0():
    """Test que trouverDeuxiemeSolution cherche correctement une deuxième solution avec variant=0"""
    # D'abord résoudre le puzzle
    result = resoudrePuzzle("test_puzzle0", variant=0)
    
    assert result is not None, "Le puzzle doit avoir une solution"
    solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data = result
    
    # Chercher une deuxième solution
    trouverDeuxiemeSolution(solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data, "test_puzzle0", variant=0)
    
    # Vérifier que le fichier de la deuxième solution a été créé
    assert os.path.exists("DIMACS/test_puzzle0_sol2.cnf"), "Le fichier DIMACS pour la deuxième solution doit être créé"


def test_trouverDeuxiemeSolution_variant1():
    """Test que trouverDeuxiemeSolution cherche correctement une deuxième solution avec variant=1"""
    # D'abord résoudre le puzzle
    result = resoudrePuzzle("test_puzzle1", variant=1)
    
    assert result is not None, "Le puzzle doit avoir une solution"
    solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data = result
    
    # Chercher une deuxième solution
    trouverDeuxiemeSolution(solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data, "test_puzzle1", variant=1)
    
    # Vérifier que le fichier de la deuxième solution a été créé
    assert os.path.exists("DIMACS/test_puzzle1_sol2.cnf"), "Le fichier DIMACS pour la deuxième solution doit être créé"

def test_trouverDeuxiemeSolution_variant2():
    """Test que trouverDeuxiemeSolution cherche correctement une deuxième solution avec variant=2  """
    # D'abord résoudre le puzzle
    result = resoudrePuzzle("test_puzzle2", variant=2)
    
    assert result is not None, "Le puzzle doit avoir une solution"
    solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data = result
    
    # Chercher une deuxième solution
    trouverDeuxiemeSolution(solver, model, n, letters, nb_states, EMPTY_IDX, puzzle_data, "test_puzzle2", variant=2)
    
    # Vérifier que le fichier de la deuxième solution a été créé
    assert os.path.exists("DIMACS/test_puzzle2_sol2.cnf"), "Le fichier DIMACS pour la deuxième solution doit être créé"

