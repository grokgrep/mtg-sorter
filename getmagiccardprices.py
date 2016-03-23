#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Geoff
#
# Created:     10/04/2012
# Copyright:   (c) Geoff 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Matthew Sheridan
# getmagiccardprices.py
# 15 November 2015
# Retrieve current price data for MTG cards by name.

#!/usr/bin/env python

from PySide import QtCore, QtGui, QtWebKit
import csv, os, re, sys

# Handle args.
if len(sys.argv) != 3:
    print "Usage:\n  getmagiccardprices.py input output\n"
    print "input \tA list of exact card names and quantities, delimited by semicolon."
    print "output \tA CSV formatted for Excel; will be appended if it already exists."
    exit()

# Output field names, regex for price search, file paths, and rows of input/output data.
output_fields = ["NAME","QTY","LOW (ea.)","MID (ea.)","HI (ea.)","LOW","MID","HI"]
pattern = re.compile("TCGPPriceLow\".*\$(\d*.\d\d).*TCGPPriceMid.*\$(\d*.\d\d).*TCGPPriceHigh[^\$]*\$(\d*.\d\d)")
input_path = os.getcwd() + "\\" + str(sys.argv[1])
output_path = os.getcwd() + "\\" + str(sys.argv[2])

# Counters for summary and misc.
count_total = 0
count_success = 0
count_failed = 0

# Pre:  url is URL of webpage to render.
# Post: Returns HTML of rendered page.
def render(url):
    page = QtWebKit.QWebPage()
    loop = QtCore.QEventLoop()
    page.mainFrame().loadFinished.connect(loop.quit)
    page.mainFrame().load(url)
    loop.exec_()
    return page.mainFrame().toHtml()

# Pre:  path is an input file path. This file lists names and quantities, delimited by semicolon.
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
#       fields is the list of field names to be printed at the top of the output file.
#       output is the list of rows to output, each item of which corresponds to a field name.
# Post: The file at path has either been created or appended with the rows of card names, quantities, and prices.
def write_cards(path, fields, output):
    with open(path, "ab") as o:
        writer = csv.writer(o, dialect='excel')
        # Add header line to output if file is empty.
        if os.stat(path).st_size < 1:
            output.insert(0, fields)
        for r in output:
            writer.writerow(r)

# Pre:  input is a list of card names to search for and quantity of each.
#       pattern is the regular expression
# Post: Returns a list of names, quantities, and prices.
#       Prints progress to console.
def scrape(input_rows, pattern):
    global count_total
    global count_success
    global count_failed
    dat = []
    counter = 0
    sys.stdout.write("Fetching...")
    sys.stdout.flush()
    for r in input_rows:
        counter += 1
        name = str(r[0])
        qty = int(r[1])
        # Search for exact name match.
        result = render("http://magiccards.info/query?q=!" + name)
        prices = pattern.search(result)

        # Display running progress.
        sys.stdout.write("\rFetching... (" + str(counter) + "/" + str(count_total) + ")")
        sys.stdout.flush()

        # If exact match was found, add its data to output.
        if prices:
            dat.append([name, qty, prices.group(1), prices.group(2), prices.group(3), float(prices.group(1)) * qty, float(prices.group(2)) * qty, float(prices.group(3)) * qty])
            count_success += 1
        else:
            dat.append([name, qty])
            count_failed += 1
    return dat

app = QtGui.QApplication(sys.argv)

# Read in cards, conduct search, write results to file.
input_rows = read_cards(input_path)
output_rows = scrape(input_rows, pattern)
write_cards(output_path, output_fields, output_rows)

# Sum everything up!
print ""
if count_success > 0:
    print "Found:\t" + str(count_success) + " card(s)."
if count_failed > 0:
    print "Missed:\t " + str(count_failed) + " card(s)."

app.exit()
