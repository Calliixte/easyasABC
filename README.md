# easyasABC
> Mini-projet S2 1A ENSIIE

## Arborescence

- DIMACS/
    - *Fichiers dimacs cnf générés par l'execution des programmes*
- Functions/
    - helpers.py
        - *Fonctions utiles à la génération de dimacs à partir de puzzles exemple : atLeastOne/atMostOne*
    - steps.py 
        - *Fonctions de résolution de puzzles, une fonction par point demandé dans le sujet*
- Puzzles/
    - *Instances de puzzles qui vont être utilisées pour générer les fichiers dimacs*
- .gitignore 
    - *Le développement partagé a été fait sur github, ce fichier en est une trace*
- main.py
    - *Fichier dans lequel il est possible d'utiliser les différentes fonctions pour résoudre des puzzles*
- Makefile
    - *Permet de lancer le programme, gere l'installation des dépendances si besoin*
- sujet.pdf
    - *Sujet du projet*

**Remarque** : Il existe une correspondance entre le nom d'un fichier Puzzle et son DIMACS associé. Par exemple, le puzzle ```easy.json``` sera représenté en dimacs par ```easy.cnf```