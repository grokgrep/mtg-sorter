#!/usr/bin/env python

# Name:         getmagiccardprices.py
# Authors:      Geoff, Matthew Sheridan
# Date:         04 October 2012
# Revision:     28 March 2016
# Copyright:    (c) Geoff 2012
# Licence:      <your licence>

"""Usage:
  new.getprices.py [-lo] <input> [<output>]
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
  -h --help  Show this help message.
  -l         Use a semicolon-delimited list of names and quantities instead of
             default deckstats formatting.
  -o         Overwrite OUTPUT file instead of appending.
  --version  Display program version number.
"""

DEBUG = False

__authors__ = "Geoff, Matthew Sheridan"
__credits__ = ["Geoff", "Matthew Sheridan"]
__date__    = "28 March 2016"
__version__ = "0.3"
__status__  = "Development"

import os
import sys
from mtgs_error import Error
from mtgs_getprices import GetPrices
from docopt import docopt

if __name__ == "__main__":
    # Process arguments and check for errors.
    args = docopt(__doc__, help=True, version=__version__)
    read_path  = os.getcwd() + "\\" + args["<input>"]
    write_path = os.getcwd() + "\\" + args["<output>"]
    overwrite = False
    if args["-o"]:
        overwrite = True
    if args["-l"]:
        read_format = "list"
    else:
        read_format = "deckstats"
    write_format = "excel"

    # Get prices!
    try:
        gp = GetPrices(DEBUG)
        input_rows  = gp.read_cards(read_path, read_format)
        output_rows = gp.scrape(input_rows)
        gp.write_cards(write_path, write_format, output_rows, overwrite)
        print "\n" + gp.summary()
    except Error as e:
        print e
        exit(1)
    exit(0)
