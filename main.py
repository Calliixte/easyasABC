from pysat.solvers import Glucose3
from pysat.formula import CNF
import json

def check_letter(headers,i,j,lettre): #verifie si lettre est en i,j selon les headers
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
            
        lettre_current = header[cord]
        if(lettre_current == lettre):
            return lettre_current
    return '.'

def check_any_letter(headers,i,j):#verifie si une lettre est plaçable en i,j
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

        
def atLeastOne(f,startNumber,endNumber): #je passe le fd au lieu du path car ça causait des problemes de pointeurs d'ouvrir plusieurs fois le fichier
    cpt = startNumber
    while(cpt < endNumber):
        f.write(f"{cpt} ")
        cpt+=1
    fout.write("0\n")
    
    
def atMostOne(f,x,y):
    f.write(f"-{x} -{y} 0\n")

def atMostOne_range(f, startNumber, endNumber):
    for i in range(startNumber, endNumber):
        for j in range(i + 1, endNumber):
            atMostOne(f,i,j)
    


# -------------- Main -----------------


filename = 'veasytest'


# vérifie si le fichier cnf correspondant au puzzle donné existe, s'il n'existe pas, le créer
try:
    open(f"DIMACS/{filename}.cnf")
except :
    open(f"DIMACS/{filename}.cnf","x")

firstPass= True
variableCount = 1 #init a 1 pour le solver
with open(f"Puzzles/{filename}.json") as fin:
    with open(f"DIMACS/{filename}.cnf","w") as fout:
        d=json.load(fin)
        
        headers = d["headers"]
        grille = d["grid"]
        hauteur = len(grille)
        largeur = len(grille[0]) #part du principe que la grille est carrée
        lettres_utilisees = ['A','B']
        nbLettres = (len(lettres_utilisees))
        
        for i in range(hauteur):
            for j in range(largeur):
                count_before = variableCount
                for lettre in lettres_utilisees:
                    if(check_letter(headers,i,j,lettre)!='.'):
                        fout.write(f"{variableCount} 0\n")
                    variableCount+=1
                count_after = variableCount
                
                #peut pas avoir 2 lettres différentes sur une case
                atLeastOne(fout,count_before,count_after) #il manque le fait de preciser que chaque ligne et colonne peut avoir que 1 de chaque
                atMostOne_range(fout,count_before,count_after)
            print("")
        
        
        #boucles des contraintes de bases sur lignes et colonnes
        
        for i in range(hauteur): #on se positionne a une ligne
            for lk in range(nbLettres): # on prend une lettre
                for ja in range(largeur): # on se positionne a une case
                    for jb in range(ja + 1, largeur): # on l'interdit d'avoir la meme lettre que toutes les cases d'après sur la ligne via des at most one
                        x = 1 + i*largeur*nbLettres + ja*nbLettres + lk
                        y = 1 + i*largeur*nbLettres + jb*nbLettres + lk
                        atMostOne(fout,x,y)
        
        
        
        for j in range(largeur): #positionne a une colonne
            for lk in range(nbLettres): #on prend une lettre
                for ia in range(hauteur): #on se met a une case
                    for ib in range(ia + 1, hauteur): #on l'interdit d'avoir la meme lettre que toutes les cases d'après sur la colonne
                        x = 1 + ia*largeur*nbLettres + j*nbLettres + lk
                        y = 1 + ib*largeur*nbLettres + j*nbLettres + lk
                        atMostOne(fout,x,y)
            


res = CNF(from_file=f"DIMACS/{filename}.cnf")
solver = Glucose3(bootstrap_with=res)
            
if solver.solve():
    print("SAT ! Modèle :", solver.get_model())
else:
    print("UNSAT")
    
      
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            