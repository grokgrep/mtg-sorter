#!/usr/bin/env python

# Name:         mtgs_getprices.py
# Authors:      Geoff, Matthew Sheridan
# Date:         04 October 2012
# Revision:     21 April 2016
# Copyright:    (c) Geoff 2012
# Licence:      <your licence>

"""Retrieve current price data for MTG cards by name."""

__authors__ = "Geoff, Matthew Sheridan"
__credits__ = ["Geoff", "Matthew Sheridan"]
__date__    = "28 March 2016"
__version__ = "0.3c"
__status__  = "Development"

import os
import sys
import codecs
import csv
import re
import traceback
from mtgs_card import MTGCard
from mtgs_error import *
from mtgs_json import MTGJson
from mtgs_webrenderer import WebRenderer
from configobj import ConfigObj

# Retrieves current price data for MTG cards by scraping magiccards.info
class GetPrices:
    global CONFIG_FILENAME
    global FORMATS
    global FORMATS_HEADERS
    global SEARCH_PATTERN
    CONFIG_FILENAME = "conf/conf.ini"
    FORMATS = ["deckstats", "excel", "list"]
    FORMATS_HEADERS = [["amount", "card_name", "is_foil", "is_pinned", "set_id"],
                       ["CARD NAME", "QTY", "SET", "SET NAME", "LOW (ea.)", "MID (ea.)", "HI (ea.)",
                        "LOW", "MID", "HI"],
                       ["card_name", "amount"]]
    SEARCH_PATTERN = "TCGPPriceLow\".*\$(\d*.\d\d).*TCGPPriceMid.*\$(\d*.\d\d).*TCGPPriceHigh[^\$]*\$(\d*.\d\d)"

    def __defaults(self):
        self.__debug         = None
        self.__read_format   = None
        self.__write_format  = None
        self.__set_defs      = None
        self.__json_set      = None
        self.__count_total   = 0
        self.__count_success = 0
        self.__count_failed  = 0

    # Retrives set definitions used to translate set identifiers, formatted
    # same as set_defs.
    def __load_set_defs(self, path):
        """Args:
            path    -- string; File path to definition file set_defs.csv.

        Returns:
            numpy array containing common set abbreviations, full set names,
            deckstats.net ID, and magiccards.info abbreviation.
        """
        dat = []
        try:
            with open(path, "rb") as f:
                # Check for header row.
                header = csv.Sniffer().has_header(str(f.read(1024)))
                f.seek(0)
                if header:
                    next(f)

                for r in f:
                    dat.append([r[1], r[0], r[5], r[4]])

        except Error as e:
            raise e
        return dat

    # Prints error message.
    def __print_error(self, err, help=False):
        """Args:
            msg     -- string; Error message to print.
            help    -- bool; Print help message yes/no.
        """
        print(err)
        if help:
            print("\n" + str(__doc__)[:-2])

    # Conduct full read in, scrape, and write out.
    def get_prices(self, input_path, output_path, overwrite=False):
        """Args:
            input_path  -- string; File path to read the list of cards from.
            output_path -- string; File path to write the list of cards to.
            overwrite   -- bool; Idicates whether path should be overwritten or
                           appended.
        """
        self.__count_total   = 0
        self.__count_success = 0
        self.__count_failed  = 0
        input_rows  = []
        output_rows = []
        try:
            input_rows  = self.read_cards(input_path, self.__read_format)
            ########################################
            if not self.__debug:
                output_rows = self.scrape(input_rows)
            ########################################
        except Error as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(e)
            traceback.print_tb(exc_traceback, file=sys.stdout)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(type(e))
            traceback.print_tb(exc_traceback, file=sys.stdout)
        finally:
            self.write_cards(output_path, self.__write_format, output_rows, overwrite)

    # Reads from file the list of cards to get prices for.
    def read_cards(self, path, format):
        """Args:
            path    -- string; File path to read the list of cards from.
            format  -- int; Indentifies the file format of path (see FORMATS).

        Returns:
            An array of cards and quantities.
        """
        dat = dict()
        if not os.path.isfile(path):
            raise InvalidFileError(path)
        if not format in FORMATS:
            raise InvalidFormatError(format)

        with open(path, "r", encoding="utf-8") as f:
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

            for r in read:
                card = MTGCard()
                name     = ""
                setCode  = ""
                qty = 0
                if format == "deckstats":
                    name = r[1]
                    for i in range(0, len(self.__set_defs)):
                        if str(r[4]) == str(self.__set_defs[i][2]):
                            setCode = self.__set_defs[i][1]
                    qty = r[0]
                elif format == "list":
                    name = r[0]
                    qty = r[1]
                find = self.__json_set.find_partial_name(name)
                for key in find:
                    print(key + ": " + find[key]["name"] + ", " + find[key]["setCode"])
                card.name = name
                card.setCode = setCode
                dat[card] = qty
                ########################################
                print(str(card) + " (" + str(qty) + ")")
                ########################################

        if len(dat) < 1:
            raise ZeroLengthOutputError

        self.__count_total = len(dat)
        return dat

    ########################################
    # Need to update for new MTGCard
    ########################################
    # Scrapes magiccards.info for card prices.
    def scrape(self, input_rows):
        """Args:
            input_rows  -- array; The list of card names, quantities, and set identifiers to search for.

        Returns:
            A list of card names, quantities, sets, and prices for each.
            Prints progress to console.
        """
        renderer = WebRenderer(sys.argv)
        dat = []
        counter = 0
        
        if not self.__debug:
            sys.stdout.write("Fetching...")
            sys.stdout.flush()
        regex = re.compile(SEARCH_PATTERN)

        try:
            for r in input_rows:
                counter += 1
                name = str(r[0])
                qty  = int(r[1])
                set_abv = None
                set_id = None
                set_name = None
                output_row = []
                hit = False

                # Convert the deckstats set identifier into a magiccards one.
                if int(r[2]) > 0:
                    for i in range(0, len(self.__set_defs)):
                        if str(r[2]) == str(self.__set_defs[i][2]):
                            set_abv = self.__set_defs[i][0]
                            set_id = self.__set_defs[i][3]
                            set_name = self.__set_defs[i][1]
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

                # If match was found, add its data to output.
                if prices:
                    output_row = [name, qty, set_abv, set_name, prices.group(1),
                                  prices.group(2), prices.group(3),
                                  float(prices.group(1)) * qty,
                                  float(prices.group(2)) * qty,
                                  float(prices.group(3)) * qty]
                    self.__count_success += 1
                    hit = True
                else:
                    output_row = [name, qty, set_abv]
                    self.__count_failed += 1

                # Display running progress.
                if self.__debug:
                    print(str(counter) + "/" + str(self.__count_total))
                    print("> " + name + ", " + str(r[2]) + " (" + set_id + ")")
                    print("  " + query)
                    if hit:
                        print("  Hit!")
                    else:
                        print("  Miss!")
                else:
                    sys.stdout.write("\rFetching... (" + str(counter) + "/" +
                                     str(self.__count_total) + ")")
                    sys.stdout.flush()

                # Push last result onto results.
                dat.append(output_row)

        except (KeyboardInterrupt, SystemExit):
            raise InterruptedScrapeError
        except Exception as e:
            print("\n" + str(e))
            raise Error(e)
        finally:
            print("")
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
            write_mode = "w"
        else:
            write_mode = "a"

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

    # Prints summary of price scraping.
    def summary(self):
        """Returns summary of last scrape attempt."""
        success = "Found:\t" + str(self.__count_success) + " card(s)."
        failed = "Missed:\t " + str(self.__count_failed) + " card(s)."

        if self.__count_success and self.__count_failed:
            return success + "\n" + failed
        elif self.__count_success:
            return success
        elif self.__count_failed:
            return failed
        return "No cards searched for."

    def __init__(self, read_format, write_format, debug=False):
        self.__defaults()
        self.__debug = debug
        # Load configuration file info. Make these global later:
        config = ConfigObj(CONFIG_FILENAME)
        config_files  = config["files"]
        config_format = config["format"]

        set_defs_path = os.path.normpath(os.getcwd() + "/" +
                                         config_files["set_defs"])
        set_data_path = os.path.normpath(os.getcwd() + "/" +
                                         config_files["json_sets"])

        # Check for errors!
        try:
            if not os.path.isfile(set_defs_path):
                raise InvalidFileError(set_defs_path)
            if not os.path.isfile(set_data_path):
                raise InvalidFileError(set_data_path)
            if not read_format in FORMATS:
                raise InvalidFormatError(read_format)
            if not write_format in FORMATS:
                raise InvalidFormatError(write_format)
        except Error as e:
            __print_error (e, True)
            exit(1)

        self.__read_format = read_format
        self.__write_format = write_format
        self.__set_defs  = self.__load_set_defs(set_defs_path)
        self.__json_set  = MTGJson(set_data_path)

    def __del__(self):
        pass
