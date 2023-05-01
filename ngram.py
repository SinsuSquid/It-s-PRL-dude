try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import re, os
except ImportError:
    print("\tProblem with importing BeautifulSoup and requests. Have you installed it?")
    exit(1)

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
        if (s < 0 or s > 1):
            print("\n\tDOES NOT COMPUTE, TRY IT AGAIN.\n")
        elif (s == 0):
            ngramTrend()  # ngram trend search
        else:
            return # go back to previous menu

def ngramTrend():
    if ("data.csv" not in os.listdir()):
        print("There's no \'data.csv\' file in current directory.")
        print("Please start from scrapping data.")
        return

    keywords = getKeywords()
    startYear, endYear = getYears()
    data = pd.read_csv('./data.csv', index_col = 0)
    for keyword in keywords:
        freq = {}
        for yr in range(startYear, endYear):
            temp = data[data.Year == yr]
            freq[yr] = 0
            for title in temp.iloc[:,0]:
                if (type(title) != str): continue
                freq[yr] += len(re.findall(keyword, title, re.I))
                # freq[yr] = freq[yr] / len(temp)

        temp = pd.Series(freq)
        print(freq)
        plt.plot(temp.index, temp, label = keyword)
    plt.title(f"Trend change for keyword : \n{', '.join(keywords)}")
    plt.xlabel("Year"); plt.ylabel("Relative Frequency")
    plt.legend()
    plt.show()

def getKeywords():
    temp = input("Keyword(s) (Separate by ',') : ")
    keywords = [word.replace(' ', '') for word in temp.split(',')]
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
    print("\n--- N-gram Search Menu  ---\n")
    print("\t[00]. Search Trend of N-gram")
    print("\t[01]. Back to previous menu.")

if __name__ == '__main__':
    print(open('./kenobi','r').read())
    print("This isn't the file you're looking for.")
    print("Move along.")
    print("\nTip : run \"main.py\" file!")
    exit(1)
