# Anquiz

A quiz generator from an Anki deck

## Prerequisites

- Install the [Anki Connect](https://ankiweb.net/shared/info/2055492159) Add-ons in your anki
- Verify that Anki Connect is exposing the API on the port `8765` by going to `Tools > Add Ons > Select Anki Connect > Choose config` or
- Install python 3

```
curl http://localhost:8765
AnkiConnect v.6
```

## Install dependencies

```
pip install requirements.txt 
```

## Run the app

```
export FLASK_APP=main
flask run
```

Go to [http://localhost:5000](http://localhost:5000)

## Run using Docker

Soon because I need to find a way to access the ANKI API inside Docker

## How to use ?

- Once the first page is ready (This can take a while if you have a lot of decks because it is requesting to the API the list of the decks),
Choose a deck to revise. 

**Note: The name of the decks should not contain spaces to be listed**.

- Then you are ask to choose the number of cards to revise.

**Note: in case you don't choose a deck or set a number of card to revise that is upper than the total number of cards in the deck, the form contains errors**

- You are redirected to `/start` (In case you want to start a session more rapidly, you can pass the parameters in the url)

- Start your quiz by evaluate yourself on the question displayed like Anki: Click on `Show Answer` to verify the answer

- Evaluate yourself using the red button for a wrong answer and the green button for a good answer

- At the end you will have your score
