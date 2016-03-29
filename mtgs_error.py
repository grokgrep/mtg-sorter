#!/usr/bin/env python

# Name:         mtgs_error.py
# Authors:      Matthew Sheridan
# Date:         27 March 2016
# Revision:     27 March 2016
# Copyright:    Matthew Sheridan 2016
# Licence:      Beer-Ware License Rev. 42

"""Defines errors tailored for use with the MTG-Sorter project."""

__author__ = "Matthew Sheridan"
__credits__ = ["Matthew Sheridan"]
__date__    = "27 March 2016"
__version__ = "0.3"
__status__  = "Development"

import os
import sys

class Error(Exception):
    """Base class for error handling."""
    def __init__(self, msg):
        self.msg_ = msg
    def __str__(self):
        return repr(type(self).__name__ + ": " + self.msg_)

class InvalidFileError(Error):
    """Should be thrown for an invalid filename."""
    def __init__(self, file):
        self.msg_ = repr(file) + " is not a valid filename."

class InvalidFormatError(Error):
    """Should be thrown for an incorrect or undefined import/export format."""
    def __init__(self, format):
        self.msg_ = repr(format) + " is not a valid format."

class InterruptedScrapeError(Error):
    """Should be thrown for keyboard or system exit exceptions."""
    def __init__(self):
        self.msg_ = repr("Scrape interrupted and existing results written out.")

class ZeroLengthInputError(Error):
    """Should be thrown if input has now rows."""
    def __init__(self):
        self.msg_ = repr("Zero length input.")

class ZeroLengthOutputError(Error):
    """Should be thrown if input has now rows."""
    def __init__(self):
        self.msg_ = repr("Zero length output.")
