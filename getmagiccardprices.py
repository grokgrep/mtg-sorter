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

# import PyQt4.QtGui
# import PyQt4.QtCore
# import PyQt4.QtWebKit

# Renders page passed as "url"
def render(url):
    page = QtWebKit.QWebPage()
    loop = QtCore.QEventLoop()
    page.mainFrame().loadFinished.connect(loop.quit)
    page.mainFrame().load(url)
    loop.exec_()
    return page.mainFrame().toHtml()

app = QtGui.QApplication(sys.argv)

# Input and output file handling
ifile = open(os.getcwd() + "\\" + str(sys.argv[1]), "rb")
ofile = open(os.getcwd() + "\\" + str(sys.argv[2]), "a")
if os.stat(os.getcwd() + "\\" + str(sys.argv[2])).st_size < 1:
    print("Creating " + sys.argv[2])
    toWrite = "NAME,QTY,LOW(ea.),MID(ea.),HI(ea.),LOW,MID,HI\n"
    ofile.write(toWrite)
else:
    print("Appending " + sys.argv[2])

# CSV reader and regex for price search
reader = csv.reader(ifile, delimiter=",")
pattern = re.compile("TCGPPriceLow\".*\$(\d*.\d\d).*TCGPPriceMid.*\$(\d*.\d\d).*TCGPPriceHigh[^\$]*\$(\d*.\d\d)")

for row in reader:
    # Query for exact card name, no quotes.
    url = "http://magiccards.info/query?q=!" + str(row[0])
    result = render(url)

    # Fetch prices and write
    prices = pattern.search(result)
    toWrite = row[0] + "," + row[1] + ","
    if prices:
        toWrite = toWrite + prices.group(1) + "," + prices.group(2) + "," + prices.group(3) + "," + str(float(prices.group(1)) * int(row[1])) + "," + str(float(prices.group(2)) * int(row[1])) + "," + str(float(prices.group(3)) * int(row[1]))
    else:
        toWrite = toWrite + ",,,,,"
    toWrite = toWrite + "\n"
    ofile.write(toWrite)
    # print toWrite

    # Need to exit here or Qt craps out as soon as second row is hit
    # Why?
    # app.exit()
