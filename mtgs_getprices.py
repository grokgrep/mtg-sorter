#!/usr/bin/env python

# Name:         mtgs_getprices.py
# Authors:      Geoff, Matthew Sheridan
# Date:         04 October 2012
# Revision:     28 March 2016
# Copyright:    (c) Geoff 2012
# Licence:      <your licence>

"""Retrieve current price data for MTG cards by name."""

__authors__ = "Geoff, Matthew Sheridan"
__credits__ = ["Geoff", "Matthew Sheridan"]
__date__    = "28 March 2016"
__version__ = "0.3a"
__status__  = "Development"

import os
import sys
import csv
import re
from mtgs_error import Error, InvalidFileError, InvalidFormatError
from mtgs_webrenderer import WebRenderer
from configobj import ConfigObj
import numpy as np

# Retrieves current price data for MTG cards by scraping magiccards.info
class GetPrices:
    global CONFIG_FILENAME
    global FORMATS
    global FORMATS_HEADERS
    global SEARCH_PATTERN
    CONFIG_FILENAME = "conf/conf.ini"
    FORMATS = ["deckstats", "excel", "list"]
    FORMATS_HEADERS = [["amount", "card_name", "is_foil", "is_pinned", "set_id"],
                       ["NAME", "QTY", "SET", "LOW (ea.)", "MID (ea.)", "HI (ea.)",
                        "LOW", "MID", "HI"],
                       ["card_name", "amount"]]
    SEARCH_PATTERN = "TCGPPriceLow\".*\$(\d*.\d\d).*TCGPPriceMid.*\$(\d*.\d\d).*TCGPPriceHigh[^\$]*\$(\d*.\d\d)"

    def defaults(self):
        self.debug         = None
        self.read_format   = None
        self.write_format  = None
        self.set_defs      = None
        self.count_total   = 0
        self.count_success = 0
        self.count_failed  = 0

    # Retrives set definitions used to translate set identifiers, formatted
    # same as set_defs.
    def load_set_defs(self, path):
        """Args:
            path    -- string; File path to definition file set_defs.csv.

        Returns:
            numpy array containing common set abbreviations, full set names,
            deckstats.net ID, and magiccards.info abbreviation.
        """
        try:
            dat_array = np.genfromtxt(path, dtype=None, delimiter=";",
                                      skip_header=True,
                                      names=("set_abrv", "set_name",
                                             "ds_id", "mci_id"))
        except Error as e:
            raise e
        return dat_array

    # Prints error message.
    def print_error(self, err, help=False):
        """Args:
            msg     -- string; Error message to print.
            help    -- bool; Print help message yes/no.
        """
        print err
        if help:
            print "\n" + str(__doc__)[:-2]

    # Prints summary of price scraping.
    def summary(self):
        """Returns summary of last scrape attempt."""
        success = "Found:\t" + str(self.count_success) + " card(s)."
        failed = "Missed:\t " + str(self.count_failed) + " card(s)."

        if self.count_success and self.count_failed:
            return success + "\n" + failed
        elif self.count_success:
            return success
        elif self.count_failed:
            return failed
        raise Error("No cards searched for.")
        return

    # Reads from file the list of cards to get prices for.
    def read_cards(self, path, format):
        """Args:
            path    -- string; File path to read the list of cards from.
            format  -- int; Indentifies the file format of path (see FORMATS).

        Returns:
            An array of card names, quantities, and set identifers.
        """
        self.count_total   = 0
        dat = []
        if not os.path.isfile(path):
            raise InvalidFileError(path)
        if not format in FORMATS:
            raise InvalidFormatError(format)

        with open(path, "rb") as f:
            read = None

            if format == FORMATS[0]:
                read = csv.reader(f, dialect="excel")
            elif format == FORMATS[2]:
                read = csv.reader(f, delimiter=";")
            else:
                raise Error(format + " not yet supported as read format.")

            # Check for header row.
            if csv.Sniffer().has_header(f.read(1024)):
                f.seek(0, 0)
                next(read, None)
            else:
                f.seek(0, 0)

            if format == "deckstats":
                for r in read:
                    dat.append([r[1], r[0], r[4]])
            elif format == "list":
                for r in read:
                    r.append("0")
                    dat.append(r)

        self.count_total = len(dat)
        return dat

    # Scrapes magiccards.info for card prices.
    def scrape(self, input_rows):
        """Args:
            input_rows  -- array; The list of card names, quantities, and set identifiers to search for.

        Returns:
            A list of card names, quantities, sets, and prices for each.
            Prints progress to console.
        """
        self.count_success = 0
        self.count_failed  = 0
        renderer = WebRenderer(sys.argv)
        dat = []
        counter = 0
        
        if not self.debug:
            sys.stdout.write("Fetching...")
            sys.stdout.flush()
        regex = re.compile(SEARCH_PATTERN)

        for r in input_rows:
            counter += 1
            name = str(r[0])
            qty  = int(r[1])
            set_id = None
            set_name = None

            # Convert the deckstats set identifier into a magiccards one.
            if int(r[2]) > 0:
                for i in range(0, self.set_defs.size):
                    if str(r[2]) == str(self.set_defs[i][2]):
                        set_id = self.set_defs[i][3]
                        set_name = self.set_defs[i][1]
                        break
            else:
                set_id = "n/a"
                set_name = "n/a"

            # Construct query string.
            url_base = "http://magiccards.info/query?q="
            query_name = "\"" + name + "\""
            if not set_id == "n/a":
                query_set = " e:" + str(set_id) + "/en"
            else:
                query_set = ""
            query = query_name + query_set
            result = renderer.render(url_base + query)
            prices = regex.search(result)

            output_row = []
            hit = False
            # If match was found, add its data to output.
            if prices:
                output_row = [name, qty, set_name, prices.group(1),
                              prices.group(2), prices.group(3),
                              float(prices.group(1)) * qty,
                              float(prices.group(2)) * qty,
                              float(prices.group(3)) * qty]
                self.count_success += 1
                hit = True
            else:
                output_row = [name, qty, set_name]
                self.count_failed += 1

            # Display running progress.
            if self.debug:
                print str(counter) + "/" + str(self.count_total)
                print "> " + name + ", " + str(r[2]) + " (" + set_id + ")"
                print "  " + query
                if hit:
                    print "  Hit!"
                else:
                    print "  Miss!"
            else:
                sys.stdout.write("\rFetching... (" + str(counter) + "/" +
                                 str(self.count_total) + ")")
                sys.stdout.flush()

            dat.append(output_row)

        return dat

    # Writes to file the cards and corresponding prices.
    def write_cards(self, path, format, output, overwrite=False):
        """Args:
            path        -- string; File path to write the list of cards to.
            format      -- string; Indentifies the file format of path
                           (see FORMATS).
            output      -- array; The list of rows containing cards and prices.
            overwrite   -- bool; Idicates whether path should be overwritten or
                           appended.
        """
        if not format in FORMATS:
            raise InvalidFormatError(format)

        if overwrite:
            write_mode = "wb"
        else:
            write_mode = "ab"

        with open(path, write_mode) as f:
            writer = None

            if format == FORMATS[1]:
                writer = csv.writer(f, dialect="excel")
            else:
                raise Error(format + " not yet supported as write format.")

            # Add header line if file is empty.
            if os.stat(path).st_size < 1:
                if format == FORMATS[1]:
                    output.insert(0, FORMATS_HEADERS[1])

            for r in output:
                writer.writerow(r)

    def __init__(self, debug=False):
        self.defaults()
        self.debug = debug
        # Load configuration file info. Make these global later:
        config = ConfigObj(CONFIG_FILENAME)
        config_files  = config["files"]
        config_format = config["format"]

        # Load set definition file.
        set_defs_path = os.path.normpath(os.getcwd() + "/" +
                                         config_files["set_defs"])

        # Check for errors!
        try:
            if not os.path.isfile(set_defs_path):
                raise InvalidFileError(set_defs_path)
        except Error as e:
            print_error (e, True)
            exit(1)
        self.set_defs  = self.load_set_defs(set_defs_path)

    def __del__(self):
        pass
