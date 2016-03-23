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
import csv
import os
import re
import sys
import time

# Renders page passed as "url"
def render(url):
    page = QtWebKit.QWebPage()
    loop = QtCore.QEventLoop()
    page.mainFrame().loadFinished.connect(loop.quit)
    page.mainFrame().load(url)
    loop.exec_()
    return page.mainFrame().toHtml()

app = QtGui.QApplication(sys.argv)

# Output file field names, regex for price search, and empty array of rows to output.
ofields = ["NAME","QTY","LOW(ea.)","MID(ea.)","HI(ea.)","LOW","MID","HI"]
pattern = re.compile("TCGPPriceLow\".*\$(\d*.\d\d).*TCGPPriceMid.*\$(\d*.\d\d).*TCGPPriceHigh[^\$]*\$(\d*.\d\d)")
orows = []

# File handling.
ifile = open(os.getcwd() + "\\" + str(sys.argv[1]), "rb")
reader = csv.reader(ifile, delimiter=";")
ofile = open(os.getcwd() + "\\" + str(sys.argv[2]), "ab")
writer = csv.writer(ofile, dialect='excel')

# Add header line to output if file doesn't already exist.
if os.stat(os.getcwd() + "\\" + str(sys.argv[2])).st_size < 1:
    orows.append(ofields)

success = 0
failed = 0
for row in reader:
    # Query for exact card name.
    name = str(row[0])
    qty = int(row[1])
    print "Fetching \"" + name + "\""
    url = "http://magiccards.info/query?q=!" + name
    result = render(url)

    # Scrape prices and append to output if they were found.
    prices = pattern.search(result)
    if prices:
        orows.append([name, qty, prices.group(1), prices.group(2), prices.group(3), float(prices.group(1)) * qty, float(prices.group(2)) * qty, float(prices.group(3)) * qty])
        success += 1
    else:
        orows.append([name, qty])
        failed += 1

# Write out all rows.
for row in orows:
    writer.writerow(row)

if success > 0:
    print "Done. Wrote " + str(success) + " rows successfully."
if failed > 0:
    print "Did not find " + str(failed) + " items."

app.exit()
