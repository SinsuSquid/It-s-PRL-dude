from rich import print
from rich.panel import Panel
try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import re, os
    from collections import Counter
except ImportError:
    print("\tProblem with importing BeautifulSoup and requests. Have you installed it?")
    exit(1)

STOPWORDS = "a about above after again against all am an and any are aren't as at be because been before being below between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves [Phys. Rev. Lett. Publisher's Note: et al. two x ray dimensional".lower().split(' ')


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
            ngramTrend()  # ngram trend search
        elif (s == 1):
            ngramOTY()  # ngram of the year
        else:
            return # go back to previous menu

def ngramOTY():
    if ("data.csv" not in os.listdir()):
        print("There's no \'data.csv\' file in current directory.")
        print("Please start from scrapping data.")
        return

    startYear, endYear = getYears()
    while(True):                           
        N = input("Please set N for N-gram (either 2 and 3) ")
        if (N.isnumeric() and N in ['2', '3']): N = int(N); break  
    while(True):
        howMany = input("How many results to display per year : ")
        if (howMany.isnumeric()): howMany = int(howMany); break

    data = pd.read_csv('./data.csv', index_col = 0)
    for yr in range(startYear, endYear + 1):
        temp = data[data.Year == yr].iloc[:,0]
        ngrams = []
        for title in temp:
            splitted = re.split('[ ,-]', title)
            splitted = [word.lower() for word in splitted \
                        if (word.lower() not in STOPWORDS and not word.isnumeric())]
            if (N == 2): ngrams.extend([(splitted[i], splitted[i+1]) for i in range(len(splitted) - 2)])
            if (N == 3): ngrams.extend([(splitted[i], splitted[i+1], splitted[i+2]) \
                                        for i in range(len(splitted) - 3)])
        common = Counter(ngrams).most_common(howMany)
        print(f"\n{yr} : ")
        showResult = ""
        if (N == 2): 
            for j in range(howMany): showResult += f"{common[j][0][0]} {common[j][0][1]} - {common[j][1]}\n"
        if (N == 3): 
            for j in range(howMany): 
                showResult += f"{common[j][0][0]} {common[j][0][1]} {common[j][0][2]} - {common[j][1]}\n"
        print(Panel(showResult))


def ngramTrend():
    if ("data.csv" not in os.listdir()):
        print("There's no \'data.csv\' file in current directory.")
        print("Please start from scrapping data.")
        return

    keywords = getKeywords()
    startYear, endYear = getYears()
    data = pd.read_csv('./data.csv', index_col = 0)
    mod = getMode()
    for keyword in keywords:
        freq = {}
        for yr in range(startYear, endYear + 1):
            temp = data[data.Year == yr]
            freq[yr] = 0
            for title in temp.iloc[:,0]:
                if (type(title) != str): continue
                freq[yr] += len(re.findall(keyword, title, re.I))
            if (mod == 1): freq[yr] = freq[yr] / len(temp)

        temp = pd.Series(freq)
        plt.plot(temp.index, temp, label = keyword)
    plt.title(f"Trend change for keyword : \n{', '.join(keywords)}")
    plt.xlabel("Year"); 
    if (mod == 1): plt.ylabel("Relative Frequency")
    else: plt.ylabel("Counts")
    plt.legend()
    plt.show()

def getMode():
    while(True):
        mod = input("Select display method (0 : count, 1 : relative freq.) : ")
        if (mod.isnumeric() and mod in ['0','1']): return int(mod)

def getKeywords():
    temp = input("Keyword(s) (Separate by ',') : ")
    keywords = [word.strip() for word in temp.split(',')]
    return keywords

def getYears():
    startYear = input("From Which Year (default : 1958) : ")
    if (not startYear.isnumeric() or startYear == ''): startYear = 1958
    else: startYear = int(startYear)
    endYear = input("Until Which Year (default : 2022) : ")
    if (not endYear.isnumeric() or endYear == ''): endYear = 2022
    else: endYear = int(endYear)
    return (startYear, endYear)

def printMenu():
    menu = \
    """\n\t---------- [green]About Topics Menu[/green] ----------\n
    \t[00]. Search Trend of N-gram
    \t[01]. Find N-gram of the year
    \t[02]. Back to previous menu
    """
    print(Panel(menu))

if __name__ == '__main__':
    print(open('./kenobi','r').read())
    print("This isn't the file you're looking for.")
    print("Move along.")
    print("\nTip : run \"main.py\" file!")
    exit(1)
