from rich.console import Console
from rich.progress import track
from rich import print
from rich.panel import Panel

try:
    from bs4 import BeautifulSoup
    import requests
    import re, os
    import pandas as pd
    from datetime import datetime
except ImportError:
    print("\tProblem with importing BeautifulSoup and requests. Have you installed it?")
    exit(1)

console = Console()

PRL_ISSUE_LINK="https://journals.aps.org/prl/issues"

month = {'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5, 'June' : 6, 'July' : 7, 'August' : 8, 'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12}

num_issues = {}

def run():
    menu()

def createDatabase():
    print("\nWARNING : This process can take more than an hour.")
    answer = input("Do you still want to proceed? (y/n) : ")
    if answer not in ['yes','y']: return 
    if ("data.csv" in os.listdir()):
        print()
        print("You already have \'data.csv\' in your current directory.")
        answer = input("Do you want to renew the database? (y/n) : ")
        if answer not in ['yes','y']: return
    getIssueNum()
    getData()

def getData():
    console.log("Scaping article data from the web...")
    data = []
    lenVolume = len(num_issues.keys())
    for i in range(1,1+len(num_issues)):
        for j in track(range(num_issues[i]), description = f"Volume {i:3d}/{lenVolume}"):
            url = PRL_ISSUE_LINK + f"/{i}/{j}"
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            articles = soup.select('div.article.panel.article-result')
            for article in articles:
                title = article.find('h5').string
                if (not title):
                    title = str(article.find('h5', attrs = {'class':'title'}))
                    title = re.sub("<.+?>","",title)
                authors = article.find('h6', attrs = {'class':'authors'})
                if (authors): 
                    authors = authors.string
                    authors = authors.replace('and',',').split(',')
                    authors = [e.strip() for e in authors if (e != ' ' and e != '')]
                pub_info = article.find('h6', attrs = {'class':'pub-info'})
                pub_info = re.search(r'"pub-info">(.+?) <b>(\d+?)</b>, (\d+?) [(](\d+?)[)].+?Published(.+?)</h6>', str(pub_info)).groups()
                pub_date = pub_info[-1].strip().split(' ')
                dy, mon, yr = int(pub_date[0]), month[pub_date[1]], int(pub_date[2])
                pub_info = pub_info[0] + " " + pub_info[1] + ', ' + pub_info[2] + " (" + pub_info[3] + ")"
                data.append([title,authors,pub_info,yr,mon,dy])
                # print([title,authors,pub_info,yr,mon,dy])
    headers = ['Title','Authors','Publication Info','Year','Month','Day']
    data = pd.DataFrame(data, columns = headers)
    data.to_csv('./data.csv')

def getIssueNum():
    console.log("[green]Obtaining number of issues per volume ... ")
    response = requests.get(PRL_ISSUE_LINK)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        num_volumes = int(soup.find('div', attrs = {'class':'volume-issue-list'}).h4.a.string.split()[1])
        for i in track(range(1,num_volumes + 1), description = "Fetching... "):
            url = PRL_ISSUE_LINK + f"/{i}#v{i}"
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            volume = soup.select('div.volume-issue-list')[-i]
            num_issues[i] = len(volume.find_all('li'))

    else:
        print(response.status_code)
        print("ERROR : Maybe you should check your internet status?")
        exit(1)

def menu():
    while(True):
        printMenu()
        print("\n")
        s = input("Please select the menu : ")
    
        if (not s.isnumeric()): 
            print("\n\tDOES NOT COMPUTE, TRY IT AGAIN.\n")
            continue
        s = int(s)
        if (s < 0 or s > 3):
            print("\n\tDOES NOT COMPUTE, TRY IT AGAIN.\n")
        elif (s == 0):
            createDatabase()  # Make a new database.
        elif (s == 1): # Check current database.
            if ('data.csv' in os.listdir()):
                time = datetime.fromtimestamp(os.path.getmtime('./data.csv'))
                time = time.strftime("%Y-%m-%d %H:%M:%S")
                print("Last modified time for \'data.csv\' is " + time + ".")
            else:
                print("There's no \'data.csv\' file in current directory.")
                print("No action performed.\n")
        elif (s == 2): # Delete current database.
            if ('data.csv' in os.listdir()):
                os.remove('./data.csv')
                print("Removed \'data.csv\' from your directory.")
            else:
                print("There's no \'data.csv\' file in current directory.")
                print("No action performed.\n")
        else:
            return # back to previous menu

def printMenu():
    menu = \
    """\n\t---------- [green]Scrap database from web ----------\n
    [white]\t[00]. Make a new database.
    \t[01]. Check current database.
    \t[02]. Delete current database.
    \t[03]. Back to previous menu.
    """
    print(Panel(menu))

if __name__ == '__main__':
    print(open('./kenobi','r').read())
    print("This isn't the file you're looking for.")
    print("Move along.")
    print("\nTip : run \"main.py\" file!")
    exit(1)
