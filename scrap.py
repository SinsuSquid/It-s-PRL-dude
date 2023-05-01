try:
    from bs4 import BeautifulSoup
    import requests
    import re, os
    import pandas as pd
    from datetime import datetime
except ImportError:
    print("\tProblem with importing BeautifulSoup and requests. Have you installed it?")
    exit(1)

PRL_ISSUE_LINK="https://journals.aps.org/prl/issues"

month = {'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5, 'June' : 6, 'July' : 7, 'August' : 8, 'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12}

num_issues = {}

def run():
    menu()

def createDatabase():
    print("WARNING : This process can take more than an hour.")
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
    print("Scaping article data from the web...")
    data = []
    for i in range(1,1+len(num_issues)):
        for j in range(num_issues[i]):
            url = PRL_ISSUE_LINK + f"/{i}/{j}"
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            articles = soup.select('div.article.panel.article-result')
            for article in articles:
                title = article.select_one('div > div > h5 > a')
                title = re.search(r'">(.+)</a', str(title)).groups()[0]
                title = re.sub(r'<(.+?)>','',title)
                authors = article.select_one('div > div > h6.authors')
                if (authors): 
                    authors = re.search(r'"authors">(.+)</h6>', str(authors)).groups()[0]
                    authors = authors.replace('and',',').split(',')
                    authors = [e.strip() for e in authors if (e != ' ' and e != '')]
                pub_info = article.select_one('div > div > h6.pub-info')
                pub_info = re.search(r'"pub-info">(.+?) <b>(\d+?)</b>, (\d+?) [(](\d+?)[)].+?Published(.+?)</h6>', str(pub_info)).groups()
                pub_date = pub_info[-1].strip().split(' ')
                dy, mon, yr = int(pub_date[0]), month[pub_date[1]], int(pub_date[2])
                pub_info = pub_info[0] + " " + pub_info[1] + ', ' + pub_info[2] + " (" + pub_info[3] + ")"
                data.append([title,authors,pub_info,yr,mon,dy])
                # print([title,authors,pub_info,yr,mon,dy])
        if (i%10 == 0): print(f"Now checking volume {i:3d}...")
    headers = ['Title','Authors','Publication Info','Year','Month','Day']
    data = pd.DataFrame(data, columns = headers)
    data.to_csv('./data.csv')

def getIssueNum():
    print("Cheking number of issues per Volume...")
    import re

    response = requests.get(PRL_ISSUE_LINK)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        volume = soup.select_one('div.volume-issue-list')
        title = volume.select_one('h4 > a')
        num_volumes = int(re.search(r'Volume (\d+)', str(title)).groups()[0])
        for i in range(1,num_volumes + 1):
            if (i%10 == 0): print(f"Now checking volume {i:3d}...")
            url = PRL_ISSUE_LINK + f"/{i}#v{i}"
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            volume = soup.select('div.volume-issue-list')[-i]
            num_issues[i] = len(volume.select('ul > li'))

    else:
        print(response.status_code)
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
    print("\n--- Scrap database from web ---\n")
    print("\t[00]. Make a new database.")
    print("\t[01]. Check current database.")
    print("\t[02]. Delete current database.")
    print("\t[03]. Back to previous menu.")

if __name__ == '__main__':
    print(open('./kenobi','r').read())
    print("This isn't the file you're looking for.")
    print("Move along.")
    print("\nTip : run \"main.py\" file!")
    exit(1)
