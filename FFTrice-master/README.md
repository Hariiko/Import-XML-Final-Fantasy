# FFTrice

FFTrice is a utility which generates an Final Fantasy TCG XML file for use with Cockatrice.

As of Opus 9, this repository contains a pre-built xml for Opus1-9.

## Features
- All rarity tags are removed from card codes.  This allows easier importing of decks from FFDecks.

## Requirements
- Python 3.x
- Cockatrice - https://cockatrice.github.io/

# Using main.py
- Download files from git repository
- Run script with python on machine with internet access
```bash
./python main.py
```
- This will create a `cards.xml` that can be imported into Cockatrice

# Installation into Cockatrice
- Please see Cockatrice custom set documentation for assistance with importing this set.
    - https://github.com/Cockatrice/Cockatrice/wiki/Custom-Cards-&-Sets
    
   