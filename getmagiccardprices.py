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

if len(sys.argv) != 3:
    print "Usage:\n  getmagiccardprices.py input output\n"
    print "input \tA list of exact card names and quantities, delimited by semicolon."
    print "output \tA CSV formatted for Excel; will be appended if it already exists."
    exit()

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
output_fields = ["NAME","QTY","LOW (ea.)","MID (ea.)","HI (ea.)","LOW","MID","HI"]
pattern = re.compile("TCGPPriceLow\".*\$(\d*.\d\d).*TCGPPriceMid.*\$(\d*.\d\d).*TCGPPriceHigh[^\$]*\$(\d*.\d\d)")
input_rows = []
output_rows = []

input_path = os.getcwd() + "\\" + str(sys.argv[1])
output_path = os.getcwd() + "\\" + str(sys.argv[2])

with open(input_path, "rb") as input_file:
    reader = csv.reader(input_file, delimiter=";")
    for row in reader:
        input_rows.append(row)

counter = 0
total = len(input_rows)
success = 0
failed = 0
for row in input_rows:
    counter += 1
    name = str(row[0])
    qty = int(row[1])

    # Query for exact card name.
    print "Fetching " + str(counter) + "/" + str(total) + ": \"" + name + "\""
    url = "http://magiccards.info/query?q=!" + name
    result = render(url)

    # Scrape prices and append to output if they were found.
    prices = pattern.search(result)
    if prices:
        output_rows.append([name, qty, prices.group(1), prices.group(2), prices.group(3), float(prices.group(1)) * qty, float(prices.group(2)) * qty, float(prices.group(3)) * qty])
        success += 1
    else:
        output_rows.append([name, qty])
        failed += 1

# Write out all rows.
with open(output_path, "ab") as output_file:
    writer = csv.writer(output_file, dialect='excel')
    # Add header line to output if file is empty.
    if os.stat(output_path).st_size < 1:
        output_rows.insert(0, output_fields)
    for row in output_rows:
        writer.writerow(row)

if success > 0:
    print "Done. Wrote " + str(success) + " rows successfully."
if failed > 0:
    print "Did not find " + str(failed) + " items."

app.exit()
