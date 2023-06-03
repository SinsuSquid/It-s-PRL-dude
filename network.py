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

    G = nx.Graph() # graph 초기화

    thisLevel = [name]
    level = 0

    while (level < maxLevel):
        nextLevel = [] # 다음 단계에서 탐색할 저자 list 생성
        for i in range(len(thisLevel)):
            cand = thisLevel[i]

            names = []
            for author in track(data.Authors, description = f"Cousins of {cand}..."):
                if (type(author) != float): # NaN은 skip
                    authorList = author.split(';')

                    if cand in authorList: # 검색 대상이 작성한 논문 탐색
                        for a in authorList:
                            if (a != cand): names.append(a) # 본 저자 외 다른 이름 추가

            freq = Counter(names) # 같이 작업한 저자의 빈도 저장
            console.log("[green]Creating a Graph ... ")

            # create graph

            G.add_node(cand) # 원래 저자의 node 생성

            for n, f in freq.most_common(maxNum):
                G.add_node(n)
                G.add_edge(cand, n, weight = f) # 원래 저자와 공동 저자의 edge 생성
                nextLevel.append(n) # 새로운 저자는 다음 level에 저장

            if (i == len(thisLevel) - 1): # 현재 level이 끝나고 다음 level로 이동
                thisLevel = nextLevel

        level += 1
    
    color_map = ['red' if (i == 0) else 'blue' for i in range(len(G))] # 검색 대상만 붉은색으로 표시

    edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())

    nx.draw(G, with_labels = True,
               node_color = color_map,
               edgelist = edges,
               edge_color = weights,
               edge_cmap = plt.cm.Blues,
               width = 3.0)
    plt.show()

def checkName(data):
    global name

    name = input("Give me the name! : ");
    
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
