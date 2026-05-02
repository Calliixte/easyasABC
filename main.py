from pysat.solvers import Glucose3
import json


def check_letter(headers,i,j):
    # on part du principe que les grilles données sont valides, sinon il faudrait vérifier une contradiction possible au niveau des lettres données (par exemple un coin ou on aurait A a gauche et B au dessus)
    headers_to_check = {}
    if(i==0):
        headers_to_check["top"] = headers["top"]
    if(j==0):
        headers_to_check["left"] = headers["left"]
    if(i==len(grille)-1):
        headers_to_check["down"] = headers["down"]
    if(j==len(grille[i])-1):
        headers_to_check["right"] = headers["right"]
        
    for position,header in headers_to_check.items() : 
        cord = -1
        
        if(position in ["top","down"]): #vérifie si le header est au dessus/dessous ou sur le coté pour savoir s'il faut utiliser i ou j pour trouver la case correspondante
            cord = j
        else:                           #pour left right
            cord = i
            
        if(cord==-1):
            raise Exception("cord inconnue erreur")
            
        lettre = header[cord]
        if(lettre != '.'):
            return lettre
    return '.'

#essaye de placer une lettre en i,j en fonction de headers donnés
#renvoie true si une lettre a été placée
def place_letter(headers,i,j):
    lettre = check_letter(headers,i,j)
    if lettre !='.':
        print(lettre,end='')
        return True
    return False

def atLeastOne(file):
    pass
    
def atMostOne(file):
    pass

# -------------- Main -----------------


filename = 'easy1'


# vérifie si le fichier cnf correspondant au puzzle donné existe, s'il n'existe pas, le créer
try:
    open(f"DIMACS/{filename}.cnf")
except :
    open(f"DIMACS/{filename}.cnf","x")

variableCount = 1 #init a 1 pour le solver
with open(f"Puzzles/{filename}.json") as fin:
    with open(f"DIMACS/{filename}.cnf") as fout:
        d=json.load(fin)
        headers = d["headers"]
        grille = d["grid"]
        for i in range(len(grille)):
            for j in range(len(grille[i])):
                
                lettre_placee = place_letter(headers,i,j)
                
                if(not lettre_placee): #si aucun header ne couvrait cette case on réécrit juste ce qu'il y avait dans la grille 
                    print(grille[i][j],end='')
            print("")
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            