from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.progress import track

try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import re, os
    from collections import Counter
    import networkx as nx
except ImportError:
    print("\tProblem with importing networkx. Have you installed it?")
    exit(1)

console = Console()
G = nx.Graph

def run():
    menu()

def menu():
    while(True):
        printMenu()
        print("\n")
        s = input("Please select the menu : ")
        if (not s.isnumeric()): 
            print("\n\tDOES NOT COMPUTE, TRY IT AGAIN.\n")
            continue 
        s = int(s)
        if (s < 0 or s > 2):
            print("\n\tDOES NOT COMPUTE, TRY IT AGAIN.\n")
        elif (s == 0):
            findMyCousin()  # scholar network
        else:
            return # go back to previous menu

def findMyCousin():
    global name

    if ("data.csv" not in os.listdir()):
        print("There's no \'data.csv\' file in current directory.")
        print("Please start from scrapping data.")
        return

    data = pd.read_csv('./data.csv')
    if (not checkName(data)) :
        print("I can't find the name on the list. Please Check again. :(")
        return

    temp = input("How many levels ? (default : 2) : ")
    maxLevel = int(temp) if (temp != '') else 2
    temp = input("How many cousins per level (default : 5) : ")
    maxNum = int(temp) if (temp != '') else 5

    console.log("[green]Looking for his/her/its cousins ... ")

    G = nx.Graph()
    edge_weight = []

    thisLevel = [name]
    level = 0

    while (level < maxLevel):
        nextLevel = []
        for i in range(len(thisLevel)):
            cand = thisLevel[i]

            names = []
            for author in track(data.Authors, description = f"Cousins of {cand}..."):
                if (type(author) != float):
                    authorList = author.split(';')

                    if cand in authorList:
                        for a in authorList:
                            if (a != cand): names.append(a)

            freq = Counter(names)
            console.log("[green]Creating a Graph ... ")

            # create graph

            G.add_node(cand)

            for n, f in freq.most_common(maxNum):
                G.add_node(n)
                G.add_edge(cand, n)
                edge_weight.append(f)
                nextLevel.append(n);

            if (i == len(thisLevel) - 1):
                thisLevel = nextLevel

        level += 1
    
    color_map = ['red' if (i == 0) else 'blue' for i in range(len(G))]

    nx.draw(G, with_labels = True,
               node_color = color_map)
    plt.show()

def checkName(data):
    global name

    name = input("Give me the name and I'll try to find his/her/its academic cousins! : ");
    
    for author in data.Authors:
        if (type(author) != float):
            authorList = author.split(';')

            if name in authorList: 
                return True

    return False

def printMenu():
    menu = \
    """\n\t---------- [green]About Authors Menu[/green] ----------\n
    \t[00]. Scholar Network
    \t[01]. Back to previous menu
    """
    print(Panel(menu))

if __name__ == '__main__':
    print(open('./kenobi','r').read())
    print("This isn't the file you're looking for.")
    print("Move along.")
    print("\nTip : run \"main.py\" file!")
    exit(1)
