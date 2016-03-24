# mtg-sorter
MTG sorting machine experimentation.

A collaborative effort by [@awesor](https://github.com/awesor), [@7thGate](https://github.com/7thGate), and [@segfaultmagnet](https://github.com/segfaultmagnet).

    Usage:
      getmagiccardprices.py [-hox] INPUT OUTPUT

    Arguments:
      INPUT   Input file. A list of exact card names and quantities, delimited by
              semicolon.
      OUTPUT  Output file. Will be a CSV formatted for Excel and will contain the
              list of card names; quantities; and low, mid, and high prices. This
              file will be appended if it already exists.

    Options:
      -h --help  Show this help message.
      -o         Overwrite OUTPUT file instead of appending.
      -x         Use Excel-formatted input from deckstats export.
      --version  Display program version number.
