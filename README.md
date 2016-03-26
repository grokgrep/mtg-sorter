# mtg-sorter
MTG sorting machine experimentation.

A collaborative effort by [@awesor](https://github.com/awesor), [@7thGate](https://github.com/7thGate), and [@segfaultmagnet](https://github.com/segfaultmagnet).

### What It Does
Reads in a list of card names and quantities, then scrapes for prices based on a name and printing match (see magiccards.info [search](http://magiccards.info/search.html) and [syntax](http://magiccards.info/syntax.html)).

        Usage:
          getmagiccardprices.py [-hlo] INPUT OUTPUT

        Arguments:
          INPUT   Input file. A list of exact card names and quantities, delimited by
                  semicolon. By default, this is exported from a deckstats.net
                  collection as a CSV file.
          OUTPUT  Output file. Will be a CSV formatted for Excel and will contain the
                  list of card names; quantities; and low, mid, and high prices. This
                  file will be appended if it already exists.

        Options:
          -h --help  Show this help message.
          -l         Use a semicolon-delimited list of names and quantities instead of
                     default deckstats formatting.
          -o         Overwrite OUTPUT file instead of appending.
          --version  Display program version number.

### New
Can now search for different editions.

### To-Do
Known causes of misses:
  Non-alphanumeric characters (e.g. Æther Burst, R&D's Secret Lair, Legions of Lim-Dûl). Some of these work when the correct character is used; others do not (sometimes depends on whether input CSV has correct character).
  Multiple results (e.g. Forest 10e also returns Karplusan Forest 10e). Query does not work with both full name and edition?
  No price returned at all (e.g. Purphoros's Emissary).

Possible solutions:
  Re-try with exact name only on initial miss (still questionable).
  Retrieve additional info from [mtgjson](http://mtgjson.com/) via [DeckBrew's API](https://deckbrew.com/api/) (i.e. number within printing), then try exact URL of card (e.g. http://magiccards.info/cstd/en/29.html).

Add exception handling.

Add handling for multiple instances of the same card name (duplicates, foils).

Improve formatting for deckstats.net input (add: .dec deck format).

Clean up documentation (what is Python style??).

### Dependencies
[ConfigObj](https://pypi.python.org/pypi/configobj/)

[docopt](https://pypi.python.org/pypi/docopt/)

[numpy](https://github.com/numpy/numpy)

[PySide](https://pypi.python.org/pypi/PySide/)
