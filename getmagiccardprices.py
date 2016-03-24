#!/usr/bin/env python

# Name:         getmagiccardprices.py
# Authors:      Geoff, Matthew Sheridan
# Date:         04 October 2012
# Revision:     23 March 2016
# Copyright:    (c) Geoff 2012
# Licence:      <your licence>
# Description:  Retrieve current price data for MTG cards by name.

"""Usage:
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

"""

__authors__ = "Geoff, Matthew Sheridan"
__credits__ = ["Geoff", "Matthew Sheridan"]
__date__    = "23 March 2016"
__version__ = "0.1g"
__status__  = "Development"

OUTPUT_FIELDS  = ["NAME", "QTY", "LOW (ea.)", "MID (ea.)",
                  "HI (ea.)", "LOW", "MID", "HI"]
SEARCH_PATTERN = "TCGPPriceLow\".*\$(\d*.\d\d).*TCGPPriceMid.*\$(\d*.\d\d).*TCGPPriceHigh[^\$]*\$(\d*.\d\d)"

import os
import sys
import csv
import re
from docopt import docopt
from PySide import QtCore, QtGui, QtWebKit

# Pre:  path is an input file path. This file lists names and quantities,
#       delimited by semicolon.
# Post: Returns list of card names to search for and quantity of each.
def read_cards(path):
    global count_total
    dat = []
    with open(path, "rb") as i:
        read = csv.reader(i, delimiter=";")
        for r in read:
            dat.append(r)
    count_total = len(dat)
    return dat

# Pre:  path is an output file path.
#       fields is the list of field names to be printed at the top of the output
#       file.
#       output is the list of rows to output, each item of which corresponds to
#       a field name.
# Post: The file at path has either been created or appended with the rows of
#       card names, quantities, and prices.
def write_cards(path, fields, output):
    with open(path, "ab") as o:
        writer = csv.writer(o, dialect='excel')
        # Add header line to output if file is empty.
        if os.stat(path).st_size < 1:
            output.insert(0, fields)
        for r in output:
            writer.writerow(r)

# Pre:  msg is the specific error message to pring.
# Post: Prints error message, usage, and quits.
def error(msg):
    print msg
    print str(__doc__)[:-2]
    exit(1)

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

def main(args):
    # Filename and path handling.
    input_filename = str(args["INPUT"])
    output_filename = str(args["OUTPUT"])
    input_path = os.getcwd() + "\\" + str(input_filename)
    output_path = os.getcwd() + "\\" + str(output_filename)
    if not os.path.isfile(input_path):
        error(input_filename + " is not a valid filename.\n")

    # Counters for summary.
    count_total = 0
    count_success = 0
    count_failed = 0

    # Read in cards to search for, conduct the search, and write out results.
    input_rows = read_cards(input_path)
    output_rows = scrape(input_rows, SEARCH_PATTERN)
    write_cards(output_path, OUTPUT_FIELDS, output_rows)

    # Sum everything up!
    print ""
    if count_success > 0:
        print "Found:\t" + str(count_success) + " card(s)."
    if count_failed > 0:
        print "Missed:\t " + str(count_failed) + " card(s)."

if __name__ == "__main__":
    # Parse arguments and call main function.
    args = docopt(__doc__, help=True, version=__version__)
    main(args)
