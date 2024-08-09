# FFTrice

FFTrice is a utility which generates an Final Fantasy TCG XML file for use with Cockatrice.

This repository contains xml for Opus 23.

## Features
- All rarity tags are removed from card codes.  This allows easier importing of decks from FFDecks.

## Requirements
- Python 3.x
- Cockatrice - https://cockatrice.github.io/

# Using main.py
- Download files from git repository
- Go to the page "https://fftcg.square-enix-games.com/en/card-browser"
- Open the inspect window, click on Network, load the set we want on the page and in the rectangle below a "get-cards" appears, we copy it and put it in the "cards.json" of the file.
- In the "cards.json" file we delete the last line and the first 3 up to ":" of the third line
- Run script with python on machine with internet access
```bash
./python main.py
```
- This will create a `cards.xml` that can be imported into Cockatrice

# Installation into Cockatrice
- Please see Cockatrice custom set documentation for assistance with importing this set.
    - https://github.com/Cockatrice/Cockatrice/wiki/Custom-Cards-&-Sets
    
   