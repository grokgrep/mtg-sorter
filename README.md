# mtg-sorter
MTG sorting machine experimentation.

A collaborative effort by [@awesor](https://github.com/awesor), [@7thGate](https://github.com/7thGate), and [@segfaultmagnet](https://github.com/segfaultmagnet).

### What It Does
Reads in a list of card names and quantities, then scrapes for prices based on an exact name match. Currently only returns the latest printing of each card (see magiccards.info [search](http://magiccards.info/search.html) and [syntax](http://magiccards.info/syntax.html)).

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

### But Wait, There's More
Added file handling, configuration file, and basic error checking.

Input format is defaulted to deckstats collection-style formatting.
### Still To Come
Add search by specific edition.

Add handling for multiple instances of the same card name (duplicates, editions, foils).

Improve formatting for deckstats.net input (add: .dec deck format).

Clean up documentation (what is Python style??).

### Stuff You'll Need
[ConfigObj](https://pypi.python.org/pypi/configobj/)

[docopt](https://pypi.python.org/pypi/docopt/)

[PySide](https://pypi.python.org/pypi/PySide/)
