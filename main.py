from pysat.solvers import Glucose3
import json


def atLeastOne(file):
    pass
    
def atMostOne(file):
    pass




with open('Puzzles/easy1.json') as f:
    d=json.load(f)


    for i in d["grid"]:
        for j in i : 
            print(j,end='')
        print("")