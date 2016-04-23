#!/usr/bin/env python

# Name:         mtgs_card.py
# Authors:      Matthew Sheridan
# Date:         19 April 2016
# Revision:     23 April 2016
# Copyright:    Matthew Sheridan 2016
# Licence:      Beer-Ware License Rev. 42

"""Container for MTG card data. Same structure as used by MTG JSON."""

########################################
# Change this to emulate dict
########################################

__author__  = "Matthew Sheridan"
__credits__ = ["Matthew Sheridan"]
__date__    = "19 April 2016"
__version__ = "0.4b"
__status__  = "Development"

import os
import sys
from mtgs_error import *

# See http://mtgjson.com/documentation.html for description of variables.
# Also includes setCode as a convenience.
class MTGCard:
    def _default(self):
        self._dict = {"id": "",
            "layout": "normal",
            "name": "",
            "names": [],
            "manaCost": "",
            "cmc": None,
            "colors": [],
            "colorIdentity": [],
            "type": "",
            "supertypes": [],
            "types": [],
            "subtypes": [],
            "rarity": "",
            "text": "",
            "flavor": "",
            "artist": "",
            "number": "",
            "power": "",
            "toughness": "",
            "loyalty": None,
            "mciNumber": "",
            "multiverseid": None,
            "variations": [],
            "imageName": "",
            "watermark": "",
            "border": "",
            "timeshifted": False,
            "hand": None,
            "life": None,
            "reserved": False,
            "releaseDate": "",
            "starter": False,
            "rulings": [],
            "foreignNames": [],
            "printings": [],
            "originalText": "",
            "originalType": "",
            "legalities": [],
            "source": "",
            "setCode": ""
        }

    def __getitem__(self, key):
        if key in self._dict:
            return self._dict[key]
        else:
            raise CardKeyError(key)

    def __setitem__(self, key, value):
        temp = self.__getitem__(key)
        if not value == "":
            if type(value) == type(temp) or temp == None:
                self._dict[key] = value
            else:
                raise CardTypeError(value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (str(self.__getitem__("name")) + " (" +
                str(self.__getitem__("setCode")) + ") (" +
                str(self.__getitem__("multiverseid")) + ")")

    def __init__(self, id="", name="", setCode=""):
        self._default()
        self.__setitem__("id", id)
        self.__setitem__("name", name)
        self.__setitem__("setCode", setCode)
