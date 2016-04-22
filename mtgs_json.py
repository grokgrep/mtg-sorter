#!/usr/bin/env python

# Name:         mtgs_json.py
# Authors:      Matthew Sheridan
# Date:         29 March 2016
# Revision:     21 April 2016
# Copyright:    Matthew Sheridan 2016
# Licence:      Beer-Ware License Rev. 42

"""Interface for searching MTG JSON data."""

__author__  = "Matthew Sheridan"
__credits__ = ["Matthew Sheridan"]
__date__    = "29 March 2016"
__version__ = "0.4"
__status__  = "Development"

import os
import sys
import json
from mtgs_card import MTGCard
from mtgs_error import *

# Loads JSON object from path and returns as dict.
class MTGJson:
    def __json_load(self, path):
        dat = None
        with open(path, "r", encoding="utf-8") as file:
            dat = json.load(file)
        return dat

    #def find_exact_name(self, name, setCode):

    # Returns a dict of cards and sets based on a partial name match.
    def find_partial_name(self, name):
        dat = dict()
        for set in self.__json_sets.items():
            for card in set[1]["cards"]:
                if name.lower() in card["name"].lower():
                    dat[card["id"]] = dict(name=card["name"], setCode=set[1]["code"], set=set[1]["name"])
        return dat

    def __init__(self, path):
        path = os.path.normpath(os.getcwd() + "/json/AllSets-x.json")
        self.__json_sets = self.__json_load(path)
