# mtg-sorter
MTG sorting machine experimentation.

A collaborative effort by [@awesor](https://github.com/awesor), [@7thGate](https://github.com/7thGate), and [@segfaultmagnet](https://github.com/segfaultmagnet).

### What It Does
Reads in a list of card names and quantities, then scrapes for prices based on a name and printing match (see magiccards.info [search](http://magiccards.info/search.html) and [syntax](http://magiccards.info/syntax.html)).

        Usage:
          getmagiccardprices.py [-do] <input> [<output>]
          getmagiccardprices.py -h | --help
          getmagiccardprices.py --version

        Arguments:
          input     Input file. A list of exact card names and quantities, delimited
                    by semicolon. By default, this is exported from a deckstats.net
                    collection as a CSV file.
          output    Output file. Will be a CSV formatted for Excel and will contain
                    the list of card names; quantities; and low, mid, and high
                    prices. This file will be appended if it already exists.
                    [default:INPUT_out.csv]

        Options:
          -d         Enable debugging output.
          -h --help  Show this help message.
          -o         Overwrite OUTPUT file instead of appending.
          --version  Display program version number.

### New
Can now search for exact cards in sets and partial name matches.

### Issues
Known causes of misses:

  No price returned at all (e.g. Purphoros's Emissary). Try different editions, skip online editions of cards.

  Exact name duplicates? (e.g. Forest OGW misses, Forest SOI hits)

  Inconsistent MTG JSON data means that some exact URLs can be used.

### To-Do
Add handling for multiple instances of the same card in input (duplicates, foils).

Add better exception handling!

Clean up documentation (what is Python style??).

Improve formatting for deckstats.net input (add: .dec deck format).

### Dependencies and Resources
[ConfigObj](http://www.voidspace.org.uk/python/configobj.html)

[docopt](http://docopt.org/)

[MTG JSON](http://mtgjson.com/)

[PySide](https://pypi.python.org/pypi/PySide/)
