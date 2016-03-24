# mtg-sorter
MTG sorting machine experimentation.

A collaborative effort by [@awesor](https://github.com/awesor), [@7thGate](https://github.com/7thGate), and [@grokgrep](https://github.com/grokgrep).

    Usage:
      getmagiccardprices.py [-h] INPUT OUTPUT

    Arguments:
      INPUT   Input file. A list of exact card names and quantities, delimited by
              semicolon.
      OUTPUT  Output file. Will be a CSV formatted for Excel and will contain the
              list of card names; quantities; and low, mid, and high prices. This
              file will be appended if it already exists.

    Options:
      -h --help  Show this help message.
      --version  Display program version number.
