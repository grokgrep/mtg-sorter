# mtg-sorter
MTG sorting machine experimentation.

A collaborative effort by [@awesor](https://github.com/awesor), [@7thGate](https://github.com/7thGate), and [@segfaultmagnet](https://github.com/segfaultmagnet).

### What It Does
Reads in a list of card names and quantities, then scrapes for prices based on a name and printing match (see magiccards.info [search](http://magiccards.info/search.html) and [syntax](http://magiccards.info/syntax.html)).

        Usage:
          new.getprices.py [-dlo] <input> [<output>]
          new.getprices.py -h | --help
          new.getprices.py --version

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
          -l         Use a semicolon-delimited list of names and quantities instead of
                     default deckstats formatting.
          -o         Overwrite OUTPUT file instead of appending.
          --version  Display program version number.

### New
Can now search for different editions and partial matches.

### To-Do
Known causes of misses:

  Multiple results (e.g. Forest 10e also returns Karplusan Forest 10e). Query does not work with both full name and edition?

  No price returned at all (e.g. Purphoros's Emissary).

Possible solutions:

  Re-try with exact name only on initial miss (still questionable).

Add exception handling.

Add handling for multiple instances of the same card name (duplicates, foils).

Improve formatting for deckstats.net input (add: .dec deck format).

Clean up documentation (what is Python style??).

### Dependencies and Resources
[ConfigObj](http://www.voidspace.org.uk/python/configobj.html)

[docopt](http://docopt.org/)

[MTG JSON](http://mtgjson.com/)

[PySide](https://pypi.python.org/pypi/PySide/)
