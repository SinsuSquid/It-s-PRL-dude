import scrap, ngram
import os
from rich import print
from rich.panel import Panel

def logo():
    logo =\
    """
    [yellow]
---------------------------------------------------------------------------------
---------------------------------------------------------------------------------
      _____ _   _        _____  _____  _                _           _        
     |_   _| | ( )      |  __ \|  __ \| |              | |         | |       
       | | | |_|/ ___   | |__) | |__) | |            __| |_   _  __| | ___   
       | | | __| / __|  |  ___/|  _  /| |           / _` | | | |/ _` |/ _ \  
      _| |_| |_  \__ \  | |    | | \ \| |____   _  | (_| | |_| | (_| |  __/_ 
     |_____|\__| |___/  |_|    |_|  \_\______| ( )  \__,_|\__,_|\__,_|\___(_)
                                               |/                            
---------------------------------------------------------------------------------
---------------------------------------------------------------------------------
                                                             [bright_green]Made by : SinsuSquid
    """

    print(logo)

def menu():
    print("Welcome to \"It's PRL, dude.\"!\n")
    if 'data.csv' not in os.listdir('.'):
        print("***** [red]WARNING WARNING WARNING WARNING WARNING[/red] *****")
        print("*                                                 *")
        print('* We couldn\'t find \'data.csv\' in this directory.  *')
        print('* Please proceed with scaping a new database.     *')
        print("*                                                 *")
        print("***** [red]WARNING WARNING WARNING WARNING WARNING[/red] *****")
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
            scrap.run()  # go to database scrap menu
            continue
        elif (s == 1):
            ngram.run() # go to n-gram menu
            continue
        elif (s == 2):
            pass # go to keyword-of-the-year menu
            break
        else:
            exit(0)

def printMenu():
    menu = \
    """\n\t[green]---------- Main Menu ----------\n
    [white]\t[00]. Scrap database from web
    \t[01]. Search n-gram
    \t[02]. Find keyword-of-the-year
    \t[03]. Exit
    """
    print(Panel(menu))

if __name__ == '__main__':
    print(open('./kenobi','r').read())
    print("This isn't the file you're looking for.")
    print("Move along.")
    print("\nTip : run \"main.py\" file!")
    exit(1)
