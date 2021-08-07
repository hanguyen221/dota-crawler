# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup

from hero import Hero

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    # 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

def getHeroNames():
    heroListUrl = "https://dota2.fandom.com/wiki/Dota_2_Wiki"
    req = requests.get(heroListUrl, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    heroEntries = soup.find_all(class_='heroentry')
    heroNames = []
    for heroEntry in heroEntries:
        aTag = heroEntry.find('a')
        name = aTag.attrs['title']
        heroNames.append(name)
    return heroNames

def getCountersForHero(hero: Hero):
    heroUrl = 'https://dota2.fandom.com/wiki/' + hero.name + '/Counters'
    req = requests.get(heroUrl, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    allTags = soup.find_all()
    badAgainstId = "Bad_against..."
    goodAgainstId = "Good_against..."
    matchupId = "Works_well_with..."
    startBad = False
    startGood = False
    startMatchup = False
    for tag in allTags:
        if tag.name == 'h2':
            if tag.find(id=badAgainstId):
                startBad = True
                startGood = startMatchup = False
                continue
            if tag.find(id=goodAgainstId):
                startGood = True
                startBad = startMatchup = False
                continue
            if tag.find(id=matchupId):
                startMatchup = True
                startBad = startGood = False
                continue
        if tag.name == 'p':
            break
        if startBad and tag.name == 'div':
            bad = tag.find('a').contents[0]
            if isinstance(bad, str):
                hero.badAgainsts.append(bad)
        if startGood and tag.name == 'div':
            good = tag.find('a').contents[0]
            if isinstance(good, str):
                hero.badAgainsts.append(good)
        if startMatchup and tag.name == 'div':
            matchup = tag.find('a').contents[0]
            if isinstance(matchup, str):
                hero.matchups.append(matchup)

if __name__ == '__main__':
    heroNames = getHeroNames()
    heroes = []
    for heroName in heroNames:
        heroes.append(Hero(heroName))

    getCountersForHero(heroes[0])
    for bad in heroes[0].badAgainsts:
        print(bad)