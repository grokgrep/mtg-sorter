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
#!/usr/bin/env python

import csv
import os
import re
import sys
import time

from lxml import html
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

# Renders page passed as "url"
class Render(QWebPage):
  def __init__(self, url):
    self.app = QApplication(sys.argv)
    QWebPage.__init__(self)
    self.loadFinished.connect(self._loadFinished)
    self.mainFrame().load(QUrl(url))
    self.app.exec_()

  def _loadFinished(self, result):
    self.frame = self.mainFrame()
    self.app.quit()

# Input and output file handling
ifile  = open(os.getcwd() + "\\" + str(sys.argv[1]), "rb")
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
    # e.g. "http://magiccards.info/query?q=!Bane of Bala Ged"
    url = "http://magiccards.info/query?q=!" + str(row[0])

    # Render page and converts to text
    r = Render(url)
    result = r.frame.toHtml().toAscii()

    # Fetch prices and print to file
    prices = pattern.search(result)
    toWrite = row[0] + "," + row[1] + ","
    if prices:
        toWrite = toWrite + prices.group(1) + "," + prices.group(2) + "," + prices.group(3) + "," + str(float(prices.group(1)) * int(row[1])) + "," + str(float(prices.group(2)) * int(row[1])) + "," + str(float(prices.group(3)) * int(row[1]))
    else:
        toWrite = toWrite + ",,,,,"
    toWrite = toWrite + "\n"
    ofile.write(toWrite)

    # Need to exit here or Qt craps out as soon as second row is hit
    # Why?
    exit()
