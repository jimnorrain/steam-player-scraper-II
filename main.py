from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import datetime
import re
import time
from urllib.error import HTTPError

def get_title(url):
    try:
        req = Request("{}".format(url), headers={'User-Agent': 'Mozilla/5.0'})  # Prevents request being denied.
        link = urlopen(req).read()
        soup = BeautifulSoup(link, 'html.parser')
        var = soup.title.string
        var = var[:-14]
        return var
    except:
        return

def main():
    running = True
    print("STEAM PLAYER COUNTS\n\n")

    while running == True:

        try:
                queryVar = input(f"Enter the game's title or app ID (integer) to start a player count query (enter 0 to exit) : ")

                if queryVar == "0":
                    exit(0)

                elif re.match('^[0-9]*$', queryVar): # Checks for all integer inputs
                    queryURL = f'https://steamcharts.com/app/{queryVar}'

                    req = Request("{}".format(queryURL), headers={'User-Agent': 'Mozilla/5.0'})  # Prevents request being denied.
                    url = urlopen(req).read()
                    bs = BeautifulSoup(url, 'html.parser')
                    dataList = []

                    playerCounts = bs.find_all('div', {"class": "app-stat"})  # Finds all images/webms on the page
                    for stat in playerCounts:
                        if stat.find('span', {"class" : "num"}):
                            #dataList.append(stat.find('a')['href'])
                            dataList.append(stat.find('span').text)
                            time.sleep(0.1)

                    now = datetime.now()
                    dtStr = now.strftime("%m/%d/%Y %H:%M:%S")
                    print(f"\nPlayer count data for {get_title(queryURL)}on {dtStr}\n\nPast 20 hours: {dataList[0]} players\n24-Hour Peak: {dataList[1]} players\nAll-time Peak: {dataList[2]} players")
                    input("\nPress Enter to continue : ")

                    selectVar = input("\nExecute next query? [Y\\N] : ").lower()
                    while selectVar not in ("y", "n"):
                        print("Invalid input!")
                        selectVar = input("\nExecute next query? [Y\\N] : ").lower()
                    if selectVar == "n":
                        running = False

                else:
                    #queryVar = queryVar.replace('_'," ")
                    queryURL = f'https://steamcharts.com/search/?q=' + queryVar.replace(' ', '_')
                    req = Request("{}".format(queryURL),
                                  headers={'User-Agent': 'Mozilla/5.0'})  # Prevents request being denied.
                    url = urlopen(req).read()
                    bs = BeautifulSoup(url, 'html.parser')
                    gameURLs = []
                    appURLs = []

                    for elem in bs.find_all('a', href=re.compile('')):
                        appURLs.append(elem['href'])
                        time.sleep(0.1)

                    for urls in appURLs:
                        if urls.find('/apps/') != True:
                            appURLs.remove(urls)

                    del appURLs[-3:]

                    for urls in appURLs:
                        gameURLs.append(f'https://steamcharts.com{urls}')

                    gameURLs.insert(0, 'null')
                    #print(gameURLs)
                    print("Retrieving relevant results, please wait...")
                    for i, results in enumerate(gameURLs, start=0):
                        if gameURLs[i] == 'null':
                            continue
                        elif get_title(results) == None:
                            print(f'{i}. 500 Error code: no response from URL...')
                            #continue
                            break
                        else:
                            print('{}. {}'.format(i, get_title(results)))
                        time.sleep(0.1)

                    while True:

                        try:
                            if len(gameURLs) == 1:
                                print('No results could be found! Enter 0 to exit this query.')
                            else:
                                pass

                            selected = int(input('\n(Enter 0 to exit current query)\nSelect a game (integer inputs only) : '))
                            result = gameURLs[selected]

                            if selected == 0:
                                print('\nExiting current query...')
                                break

                            elif get_title(result) == None:
                                print('Could not find a working page from this input, received a 500 server error!')

                                selectVar = input("\nExecute next query? [Y\\N] : ").lower()
                                while selectVar not in ("y", "n"):
                                    print("Invalid input!")
                                    selectVar = input("\nExecute next query? [Y\\N] : ").lower()

                                if selectVar == "n":
                                    exit(0)

                                else:
                                    break

                            else:
                                print('\nYou have selected {}\n'.format(get_title(result)))
                                break
                        except (ValueError, IndexError):
                            print('This is not a valid selection. Please enter a valid integer from the list of results!')

                    if selected == 0 or get_title(result) == None:
                        pass

                    else:
                        req = Request("{}".format(result), headers={'User-Agent': 'Mozilla/5.0'})  # Prevents request being denied.
                        url = urlopen(req).read()
                        bs = BeautifulSoup(url, 'html.parser')
                        dataList = []

                        playerCounts = bs.find_all('div', {"class": "app-stat"})  # Finds all images/webms on the page
                        for stat in playerCounts:
                            if stat.find('span', {"class": "num"}):
                                dataList.append(stat.find('span').text)
                                time.sleep(0.1)

                        now = datetime.now()
                        dtStr = now.strftime("%m/%d/%Y %H:%M:%S")
                        print(f"\nPlayer count data for {get_title(result)}on {dtStr}\n\nPast 20 hours: {dataList[0]} players\n24-Hour Peak: {dataList[1]} players\nAll-time Peak: {dataList[2]} players")
                        input("\nPress Enter to continue : ")

                        selectVar = input("\nExecute next query? [Y\\N] : ").lower()
                        while selectVar not in ("y", "n"):
                            print("Invalid input!")
                            selectVar = input("\nExecute next query? [Y\\N] : ").lower()
                        if selectVar == "n":
                            running = False

        except HTTPError:
            print('Invalid URL given...\n')

main()
