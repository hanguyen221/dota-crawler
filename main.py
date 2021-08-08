# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import uuid
from pprint import pprint

import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
from hero import Hero

cred = credentials.Certificate("/Users/hanguyen/PycharmProjects/dota-crawler/dota-crawler-firebase-adminsdk-ojhkv-cff31af6fc.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dota-crawler-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
ref = db.reference('/')
heroNode = 'heroes'
needCrawlHeroes = True

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
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
    badAgainstId = "Bad_against..."
    goodAgainstId = "Good_against..."
    matchupId = "Works_well_with..."

    badAgHeader = soup.find(id=badAgainstId)
    if badAgHeader:
        nextTag = badAgHeader.find_parent().find_next_sibling()
        while nextTag and not nextTag.find(id=goodAgainstId) and not nextTag.find(id=matchupId):
            if nextTag.name == 'div' and nextTag.find('a'):
                bad = nextTag.find('a').contents[0]
                if isinstance(bad, str):
                    hero.badAgainsts.append(bad)
            nextTag = nextTag.find_next_sibling()

    goodAgHeader = soup.find(id=goodAgainstId)
    if goodAgHeader:
        nextTag = goodAgHeader.find_parent().find_next_sibling()
        while nextTag and not nextTag.find(id=matchupId):
            if nextTag.name == 'div' and nextTag.find('a'):
                good = nextTag.find('a').contents[0]
                if isinstance(good, str):
                    hero.goodAgainsts.append(good)
            nextTag = nextTag.find_next_sibling()

    matchupHeader = soup.find(id=matchupId)
    if matchupHeader:
        nextTag = matchupHeader.find_parent().find_next_sibling()
        while nextTag and nextTag.name != 'p':
            if nextTag.name == 'div' and nextTag.find('a'):
                matchup = nextTag.find('a').contents[0]
                if isinstance(matchup, str):
                    hero.matchups.append(matchup)
            nextTag = nextTag.find_next_sibling()

    print('Info for ' + hero.name)
    print('Bad againsts')
    print(hero.badAgainsts)
    print('Good againsts')
    print(hero.goodAgainsts)
    print('Match up')
    print(hero.matchups)

if __name__ == '__main__':
    if needCrawlHeroes:
        heroNames = getHeroNames()
        heroes = []
        for heroName in heroNames:
            heroes.append(Hero(heroName))

        updates = {}
        ref.child(heroNode).delete()
        for hero in heroes:
            getCountersForHero(hero)
            print('Crawl done for ' + hero.name)
            updates[str(uuid.uuid4())] = hero.toDict()

        ref.child(heroNode).update(updates)
        print('Done pushing new data to firebase')
