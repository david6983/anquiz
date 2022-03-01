import json
import urllib.request
import re
import random
from flask import Flask, render_template, request, redirect

dnsCompliant = re.compile('^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$')

app = Flask(__name__)


def anki_req(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    requestJson = json.dumps(anki_req(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


def getDecks():
    return list(filter(dnsCompliant.match, invoke('deckNames')))


def getTags():
    return invoke('getTags')


def getCards(deck_name):
    if not dnsCompliant.match(deck_name):
        return "deck name should be dns compliant", []

    return invoke('findCards', query="deck:" + deck_name), ""


def getCardsFromTag(tag_name):
    return invoke('findCards', query="tag:" + tag_name), ""


def shuffle(cards):
    random.shuffle(cards)


def pickUpRandom(n, cards):
    if n >= len(cards) or n < 0:
        print("error n is too long or less than 0")
        return []
    return random.choices(cards, k=n)


def getInfos(cards):
    return invoke('cardsInfo', cards=cards)


@app.route('/start', methods=["GET"])
def start_quiz():
    if request.method == "GET":
        deck_selected = request.args.get('deck-select')
        tag_selected = request.args.get('tag-select')
        number_of_questions = request.args.get('nb-questions')
        if deck_selected == 'NULL' and tag_selected == 'NULL':
            return render_template('index.html', decks=getDecks(), error="You need to choose a deck or a tag")
        else:
            if tag_selected == 'NULL':
                cards, error = getCards(deck_selected)
            else:
                cards, error = getCardsFromTag(tag_selected)

            if error != "":
                return render_template('index.html', decks=getDecks(), error=error)
            if cards == []:
                return render_template('index.html', decks=getDecks(), error="The deck selected is empty")
            if int(number_of_questions) >= len(cards):
                return render_template('index.html', decks=getDecks(), error="Choose a number of cards below " + str(len(cards)))

            print("tout est ok")
            shuffle(cards)
            cards = pickUpRandom(int(number_of_questions), cards)
            return render_template('play.html', cards=getInfos(cards), number_of_questions=number_of_questions)

    return render_template('index.html', decks=getDecks())


@app.route('/')
def hello():
    return render_template('index.html', decks=getDecks(), tags=getTags())

