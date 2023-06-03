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

month = {'January' : 1, 'February' : 2,
         'March' : 3, 'April' : 4,
         'May' : 5, 'June' : 6,
         'July' : 7, 'August' : 8,
         'September' : 9, 'October' : 10,
         'November' : 11, 'December' : 12}

num_issues = {}

def run():
    menu()

def createDatabase():
    print("\n[red]WARNING[/red] : This process can take more than an hour.")
    answer = input("\tDo you still want to proceed? (y/n) : ")
    if answer not in ['yes','y']: return 
    if ("data.csv" in os.listdir()):
        print()
        print("You already have \'data.csv\' in your current directory.")
        answer = input("Do you want to renew the database? (y/n) : ")
        if answer not in ['yes','y']: return
    getIssueNum()
    getData()

def getData():
    console.log("[green]Scaping article data from the web...")
    data = []
    lenVolume = len(num_issues.keys()) # 하나의 Volume이 갖는 Issue의 수
    for i in range(1,1+len(num_issues)):
        for j in track(range(num_issues[i]), description = f"Volume {i:3d}/{lenVolume}"):
            url = PRL_ISSUE_LINK + f"/{i}/{j}" # 해당 Volume과 Issue에 해당하는 페이지
            response = requests.get(url) # requests module 이용해 response object 생성
            html = response.text # response로부터 html 정보 추출
            soup = BeautifulSoup(html, 'html.parser') # html parsing, soup object 생성
            articles = soup.select('div.article.panel.article-result') # 페이지에서 논문 정보만 추출
            for article in articles:
                # 논문의 제목
                title = article.find('h5').string 
                if (not title): # h5 string으로 저장되지 않은 제목 - 수식, 특수문자 등
                    title = str(article.find('h5', attrs = {'class':'title'}))
                    title = re.sub("<.+?>","",title) # regex를 이용한 처리 - tag 내용 삭제
                # 논문의 저자 정보
                # 논문 저자의 경우 h6의 다양한 tag로 저장 - 일괄적으로 regex 처리
                authors = article.find('h6', attrs = {'class':'authors'})
                if (authors):
                    authors = re.sub("<.+?>", "", str(authors))
                    authors = re.sub("[(].+?[)]", "", authors) # tag 및 () 안의 정보 삭제
                    authors = authors.replace('and',',').split(',') # , 또는 and로 저자 분리
                    authors = ";".join([e.strip() for e in authors if (e != ' ' and e != '')]) # 문자열로 저장, 각 저자의 분리는 ;로 표시
                else: # 저자 정보가 없는 논문 - editorial 등
                    authors = ""
                pub_info = article.find('h6', attrs = {'class':'pub-info'})
                # [Phys. Rev. Lett.] [130], [190201] (2023) – Published [11 May 2023]
                pub_info = re.search(r'"pub-info">(.+?) <b>(\d+?)</b>, (\d+?) [(](\d+?)[)].+?Published(.+?)</h6>', str(pub_info)).groups()
                # 11 May 2023
                pub_date = pub_info[-1].strip().split(' ')
                dy, mon, yr = int(pub_date[0]), month[pub_date[1]], int(pub_date[2])
                # Phys. Rev. Leet. 130, 190201 (2023)
                pub_info = pub_info[0] + " " + pub_info[1] + ', ' + pub_info[2] + " (" + pub_info[3] + ")"
                data.append([title,authors,pub_info,yr,mon,dy])
                # print([title,authors,pub_info,yr,mon,dy])
    # DataFrame 생성 및 저장
    headers = ['Title','Authors','Publication Info','Year','Month','Day']
    data = pd.DataFrame(data, columns = headers)
    data.to_csv('./data.csv')
    console.log("[yellow]Thanks for waiting :D[/yellow]")

def getIssueNum(): # Volume별 Issue 갯수 저장
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
    """\n\t---------- [green]Data Scrap Menu[/green] ----------\n
    \t[00]. Make a new database
    \t[01]. Check current database
    \t[02]. Delete current database
    \t[03]. Back to previous menu
    """
    print(Panel(menu))

if __name__ == '__main__':
    print(open('./kenobi','r').read())
    print("This isn't the file you're looking for.")
    print("Move along.")
    print("\nTip : run \"main.py\" file!")
    exit(1)
