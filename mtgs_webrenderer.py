#!/usr/bin/env python

# Name:         mtgs_webrenderer.py
# Authors:      Matthew Sheridan
# Date:         28 March 2016
# Revision:     28 March 2016
# Copyright:    Matthew Sheridan 2016
# Licence:      Beer-Ware License Rev. 42

"""Renders webpages tailored for use with the MTG-Sorter project."""

__author__ = "Matthew Sheridan"
__credits__ = ["Matthew Sheridan"]
__date__    = "28 March 2016"
__version__ = "0.3"
__status__  = "Development"

import os
import sys
from PySide import QtCore, QtGui, QtWebKit

class WebRenderer(object):
    def __init__(self, sys_argv_):
        """Args:
            sysargs -- System arguments (sys.argv).
        """
        self.app = QtGui.QApplication(sys_argv_)

    def __del__(self):
        self.app.exit()

    # Renders and returns a webpage's HTML.
    def render(self, url):
        """Args:
            url     -- string; URL of webpage to render.

        Returns:
            HTML of rendered page in ASCII format.
        """
        page = QtWebKit.QWebPage()
        loop = QtCore.QEventLoop()
        page.mainFrame().loadFinished.connect(loop.quit)
        page.mainFrame().load(url)
        loop.exec_()
        return page.mainFrame().toHtml().encode("ascii", "ignore")
