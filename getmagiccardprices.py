#!/usr/bin/env python

# Name:         getmagiccardprices.py
# Authors:      Geoff, Matthew Sheridan
# Date:         04 October 2012
# Revision:     01 May 2016
# Copyright:    (c) Geoff 2012
# Licence:      <your licence>

"""Usage:
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
"""

__authors__ = "Geoff, Matthew Sheridan"
__credits__ = ["Geoff", "Matthew Sheridan"]
__date__    = "28 March 2016"
__version__ = "0.4e"
__status__  = "Development"

import os
import sys
import codecs
from mtgs_error import *
from mtgs_getprices import GetPrices
from docopt import docopt

DEBUG_FILENAME = "debug.log"

if __name__ == "__main__":
    debug = False
    overwrite = False

    # Process arguments and check for errors.
    args = docopt(__doc__, help=True, version=__version__)

    if args["-d"]:
        debug = True
    if args["-o"]:
        overwrite = True

    # Input file:
    read_path  = os.path.normpath(os.getcwd() + "/" + args["<input>"])
    if not os.path.isfile(read_path):
        raise InvalidFileError(read_path)

    # Output file; optional arg, default "<input>_out.csv":
    if args["<output>"]:
        write_path = os.path.normpath(os.getcwd() + "/" + args["<output>"])
    else:
        write_path = os.path.splitext(read_path)[0] + "_out.csv"

    # Get prices!
    gp = GetPrices(debug)
    gp.get_prices(read_path, write_path, overwrite)
    print(gp.summary())

    exit(0)
