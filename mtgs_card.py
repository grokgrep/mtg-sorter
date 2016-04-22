#!/usr/bin/env python

# Name:         mtgs_card.py
# Authors:      Matthew Sheridan
# Date:         19 April 2016
# Revision:     20 April 2016
# Copyright:    Matthew Sheridan 2016
# Licence:      Beer-Ware License Rev. 42

"""Container for MTG card data. Same structure as used by MTG JSON."""

__author__  = "Matthew Sheridan"
__credits__ = ["Matthew Sheridan"]
__date__    = "19 April 2016"
__version__ = "0.3c"
__status__  = "Development"

import os
import sys

# See http://mtgjson.com/documentation.html for description of variables.
# Also includes setCode as a convenience.
class MTGCard:
    def __defaults(self):
        self.id              = None
        self.layout          = "normal"
        self.name            = ""
        self.names           = []
        self.manaCost        = ""
        self.cmc             = None
        self.colors          = []
        self.colorIdentity   = []
        self.type            = ""
        self.supertypes      = []
        self.types           = []
        self.subtypes        = []
        self.rarity          = ""
        self.text            = ""
        self.flavor          = ""
        self.artist          = ""
        self.number          = ""
        self.power           = ""
        self.toughness       = ""
        self.loyalty         = None
        self.multiverseid    = None
        self.variations      = []
        self.imageName       = ""
        self.watermark       = ""
        self.border          = ""
        self.timeshifted     = False
        self.hand            = None
        self.life            = None
        self.reserved        = False
        self.releaseDate     = ""
        self.starter         = False
        self.rulings         = []
        self.foreignNames    = []
        self.printings       = []
        self.originalText    = ""
        self.originalType    = ""
        self.legalities      = []
        self.source          = ""
        self.setCode         = ""

    def __str__(self):
        dat = self.name
        if self.setCode:
            dat += " (" + repr(self.setCode) + ")"
        if self.multiverseid:
            dat += " (" + repr(self.multiverseid) + ")"
        return dat

    def __init__(self, id=None, name="", setCode=""):
        self.__defaults()
        self.id = id
        self.name = name
        self.setCode = setCode
