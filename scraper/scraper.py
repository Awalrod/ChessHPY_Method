import requests
import re

DEBUG = True

def dprint(text):
    if DEBUG:
        print(text)

def collectPgnsFromUrl(url):
    """Collect all pgns from a chessgames.com database query, from various sources

    Args:
        url (string): url of chessgames.com table
    """
    tableUrls = collectTableUrlsFromUrl(url)
    pgns = []
    gids = set()
    for tableUrl in tableUrls:
        newIds = collectChessGameIdsFromTable(tableUrl)
        gids.update(newIds)
        
    for gid in gids:
        pgns.append(getPgnFromId(gid))
    return pgns

def collectTableUrlsFromUrl(url):
    """Get a list of chessgame table urls from a tournament, opening, or other list view

    Args:
        url (string): url of chessgames.com table
    Returns:
        list(str): a list of urls that contain chessgames.com tables with all relevant games
    """

    tableHtml = requests.get(url).text
    numPages = int(re.search("page [0-9]+ of ([0-9]+)", tableHtml).group(1))

    formattedUrl = re.sub(r"page=[0-9]+&?","",url)
    #this formatted URL makes sure there is no page argument in the base url

    urls = [formattedUrl+"&page="+str(x+1) for x in range(numPages)]

    return urls

def collectChessGameIdsFromTable(url):
    """Get complete list of chessgame id's from chessgames.com using any url that provides a table view

    Args:
        url (string): url of chessgames.com table
    Returns:
        set(str): A set of gids
    """

    tableHtml = requests.get(url)
    gidLines = [line for line in tableHtml.text.split("\n") if "gid=" in line]

    gids = set()
    for line in gidLines:
        result = re.search(r"gid=([0-9]+)",line)
        gids.add(result.group(1))
        
    return gids

def collectPgnsFromTable(url):
    """Get the pgn strings from a list of chessgames.com table

    Args:
        url (string): url of chessgames.com table
    Returns:
        list(str): A list of pgns
    """

    gids = collectChessGameIdsFromTable(url)
    dprint("Processing "+ str(len(gids))+ " gids")
    dprint(gids)

    pgns = []
    for gid in gids:
        dprint(type(gid))
        dprint(gid)
        pgns.append(getPgnFromId(gid))
    
    return pgns



#https://www.chessgames.com/nodejs/game/viewGamePGN?text=1&gid=2941121
def getPgnFromId(gid):
    """Get the pgn text from a chessgames.com game id

    Args:
        gid (string): chessgames.com game id

    Returns:
        string: pgn text
    """

    url = "https://www.chessgames.com/nodejs/game/viewGamePGN?text=1&gid=" + gid
    pgn = requests.get(url).text
    return pgn


