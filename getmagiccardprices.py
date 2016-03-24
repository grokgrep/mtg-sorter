#!/usr/bin/env python

# Name:         getmagiccardprices.py
# Authors:      Geoff, Matthew Sheridan
# Date:         04 October 2012
# Revision:     23 March 2016
# Copyright:    (c) Geoff 2012
# Licence:      <your licence>
# Description:  Retrieve current price data for MTG cards by name.

"""Usage:
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

"""

__authors__ = "Geoff, Matthew Sheridan"
__credits__ = ["Geoff", "Matthew Sheridan"]
__date__    = "23 March 2016"
__version__ = "0.1i"
__status__  = "Development"

CONFIG_FILENAME = "conf.ini"
SEARCH_PATTERN = "TCGPPriceLow\".*\$(\d*.\d\d).*TCGPPriceMid.*\$(\d*.\d\d).*TCGPPriceHigh[^\$]*\$(\d*.\d\d)"

READ_FORMATS  = ["deckstats", "list-semi"]
# WRITE_FORMATS = ["excel"]

ERROR_INVALID_FILENAME = " is not a valid filename!"
ERROR_READ_FORMAT = "Unknown read format!"

deckstats_fields = None
output_fields    = None
ifile            = None
ofile            = None
read_format      = None
write_format     = None
write_overwrite  = False
count_total   = 0
count_success = 0
count_failed  = 0

import os
import sys
import csv
import re
from configobj import ConfigObj
from docopt import docopt
from PySide import QtCore, QtGui, QtWebKit

# Pre:  path is an input file path. This file lists names and quantities,
#       delimited by semicolon.
# Post: Returns list of card names to search for and quantity of each.
def read_cards(path, read_format):
    global count_total
    dat = []
    with open(path, "rb") as i:
        # For deckstats-formatted input:
        if read_format == READ_FORMATS[0]:
            read = csv.reader(i, dialect="excel")
            for r in read:
                # Skip header row.
                if r[0] != deckstats_fields[0]:
                    dat.append([r[1], r[0]])

        # For semicolon-delimited list:
        elif read_format == READ_FORMATS[1]:
            read = csv.reader(i, delimiter=";")
            for r in read:
                dat.append(r)

        # Any strange value for read_format should have already been caught...
        else:
            error(ERROR_READ_FORMAT, False)

    count_total = len(dat)
    return dat

# Pre:  path is an output file path.
#       fields is the list of field names to be printed at the top of the output
#       file.
#       output is the list of rows to output, each item of which corresponds to
#       a field name.
# Post: The file at path has either been created or appended with the rows of
#       card names, quantities, and prices.
def write_cards(path, write_format, overwrite, fields, output):
    # write_format
    if overwrite:
        write_mode = "wb"
    else:
        write_mode = "ab"

    with open(path, write_mode) as o:
        writer = csv.writer(o, dialect="excel")
        # Add header line to output if file is empty.
        if os.stat(path).st_size < 1:
            output.insert(0, fields)
        for r in output:
            writer.writerow(r)

# Pre:  msg is the specific error message to pring.
# Post: Prints error message, help, and quits.
def error(msg, print_help):
    print msg
    if print_help:
        print ""
        print str(__doc__)[:-2]
    exit(1)

def print_summary(success, failed):
    # Sum everything up!
    print ""
    if count_success > 0:
        print "Found:\t" + str(count_success) + " card(s)."
    if count_failed > 0:
        print "Missed:\t " + str(count_failed) + " card(s)."

# Pre:  url is URL of webpage to render.
# Post: Returns HTML of rendered page.
def render(url):
    page = QtWebKit.QWebPage()
    loop = QtCore.QEventLoop()
    page.mainFrame().loadFinished.connect(loop.quit)
    page.mainFrame().load(url)
    loop.exec_()
    return page.mainFrame().toHtml()

# Pre:  input is a list of card names to search for and quantity of each.
#       pattern is the regular expression
# Post: Returns a list of names, quantities, and prices.
#       Prints progress to console.
def scrape(input_rows, pattern):
    global count_total
    global count_success
    global count_failed
    app = QtGui.QApplication(sys.argv)
    dat = []
    counter = 0
    sys.stdout.write("Fetching...")
    sys.stdout.flush()
    regex = re.compile(pattern)

    for r in input_rows:
        counter += 1
        name = str(r[0])
        qty = int(r[1])
        # Search for exact name match.
        result = render("http://magiccards.info/query?q=!" + name)
        prices = regex.search(result)

        # Display running progress.
        sys.stdout.write("\rFetching... (" + str(counter) + "/" +
                         str(count_total) + ")")
        sys.stdout.flush()

        # If exact match was found, add its data to output.
        if prices:
            dat.append([name, qty, prices.group(1),
                        prices.group(2), prices.group(3),
                        float(prices.group(1)) * qty,
                        float(prices.group(2)) * qty,
                        float(prices.group(3)) * qty])
            count_success += 1
        else:
            dat.append([name, qty])
            count_failed += 1

    app.exit()
    return dat

def main():
    global input_path
    global output_path
    global read_format
    global write_format

    # Read in cards to search for, conduct the search, and write out results.
    input_rows = read_cards(input_path, read_format)
    output_rows = scrape(input_rows, SEARCH_PATTERN)
    write_cards(output_path, write_format, write_overwrite,
                output_fields, output_rows)
    print_summary(count_success, count_failed)

if __name__ == "__main__":
    # Parse arguments and call main function.
    args = docopt(__doc__, help=True, version=__version__)

    # Handle configuration issues.
    config = ConfigObj(CONFIG_FILENAME)
    config_prices = config["get_prices"]
    deckstats_fields = config_prices["deckstats_fields"]
    output_fields = config_prices["output_fields"]

    # Handle file paths.
    ifile = str(args["INPUT"])
    ofile = str(args["OUTPUT"])
    input_path = os.getcwd() + "\\" + str(ifile)
    output_path = os.getcwd() + "\\" + str(ofile)
    if not os.path.isfile(input_path):
        error(ifile + ERROR_INVALID_FILENAME, True)
    if args["-o"]:
        write_overwrite = True

    # Handle formatting.
    # Read formatting:
    if args["-l"]:
        read_format = READ_FORMATS[1]
    else:
        read_format = READ_FORMATS[0]
    if not read_format in READ_FORMATS:
        error(ERROR_READ_FORMAT, False)

    # Write formatting:
    # write_format = WRITE_FORMATS[0]

    main()
