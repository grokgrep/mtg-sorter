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
        return repr(self.msg_)

class InvalidFileError(Error):
    """Should be thrown for an invalid filename."""
    def __init__(self, file):
        self.file_ = file
    def __str__(self):
        return repr(self.file_ + " is not a valid filename.")

class InvalidFormatError(Error):
    """Should be thrown for an incorrect or undefined import/export format."""
    def __init__(self, format):
        self.format_ = format
    def __str__(self):
        return repr(self.format_ + " is not a valid format.")
