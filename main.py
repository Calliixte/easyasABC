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
    
def atMostOne(f,startNumber,endNumber):
    cpt = startNumber
    while(cpt < endNumber):
        f.write(f"-{cpt} ")
        cpt+=1
    fout.write("0\n")
    
def atLeastOne_col(f,varNum,maxNum,step): #maxNum = i*j*nbLettres, step = i*j
    cpt = varNum
    while(cpt < maxNum):
        f.write(f"{cpt} ")
        cpt+=step
    fout.write("0\n")
    
def atMostOne_col(f,varNum,maxNum,step): #maxNum = i*j*nbLettres
    cpt = varNum
    while(cpt < maxNum):
        f.write(f"-{cpt} ")
        cpt+=step
    fout.write("0\n")
    
    ### c'est le mm code voir une refacto plz
    # hasardeux, il me manque que les contraintes sur les lignes et colonnes de ne pas avoir la meme lettre 2x sur une ligne bref c'est un atMost + atLeast sur tout mais faut arriver a chopper le bon pas et la ça fait trop longtemps jsuis dessus
def atLeastOne_row(f,varNum,maxNum,step): #maxNum = i*j*nbLettres
    cpt = varNum
    while(cpt < maxNum):
        f.write(f"{cpt} ")
        cpt+=step
    fout.write("0\n")
    
def atMostOne_row(f,varNum,maxNum,step): #maxNum = i*j*nbLettres
    cpt = varNum
    while(cpt < maxNum):
        f.write(f"-{cpt} ")
        cpt+=step
    fout.write("0\n")

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
                    
                    if(firstPass):
                        atLeastOne_col(fout,variableCount,largeur*nbLettres,nbLettres)
                        atMostOne_col(fout,variableCount,largeur*nbLettres,nbLettres)
                        atLeastOne_row(fout,variableCount,hauteur*largeur*nbLettres,nbLettres)
                        atMostOne_row(fout,variableCount,hauteur*largeur*nbLettres,nbLettres)
                        
                    variableCount+=1
                count_after = variableCount
                
                #peut pas avoir 2 lettres différentes sur une case
                atLeastOne(fout,count_before,count_after) #il manque le fait de preciser que chaque ligne et colonne peut avoir que 1 de chaque
                atMostOne(fout,count_before,count_after)
            firstPass = False
            print("")
           
            

"""
res = CNF(from_file=f"DIMACS/{filename}.cnf")
solver = Glucose3(bootstrap_with=res)
            
if solver.solve():
    print("SAT ! Modèle :", solver.get_model())
else:
    print("UNSAT")
    
"""
      
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            