# -*- coding: utf-8 -*-

"""Covid 19 Display"""

from albertv0 import *
import time
import os
import sys
import requests
# enable local module import
# relative imports don't work for some reason
sys.path.append(os.path.dirname(__file__))

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "Covid19"
__version__ = "0.1"
__trigger__ = "covid"
__author__ = "cyd3r"
__dependencies__ = []

icon_recovered = iconLookup("face-cool")
icon_confirmed = iconLookup("face-sick")
icon_deaths = iconLookup("face-crying")

covid_data = None
keys = ["Confirmed", "Deaths", "Recovered"]

def initialize():
    global covid_data
    covid_data = requests.get("https://api.covid19api.com/summary").json()

def handleQuery(query):
    if covid_data is None:
        print("Covid19 data is not available")
        return

    if not query.isTriggered:
        return

    # avoid rate limiting
    time.sleep(0.1)
    if not query.isValid:
        return

    stripped = query.string.strip()

    display_data = covid_data["Global"]
    if stripped:
        stripped = stripped.lower()
        for country_data in covid_data["Countries"]:
            if country_data["Country"].lower() == stripped or country_data["CountryCode"].lower() == stripped or country_data["Slug"].lower() == stripped:
                display_data = country_data
                break

    items = []
    for category in keys:
        main_key = "New" + category
        sub_key = "Total" + category
        if category == "Confirmed":
            icon_path = icon_confirmed
        elif category == "Recovered":
            icon_path = icon_recovered
        elif category == "Deaths":
            icon_path = icon_deaths
        else:
            # should not happen
            continue

        item = Item(id=__prettyname__,
                    icon=icon_path,
                    text="New {}: {}".format(category, display_data[main_key]),
                    subtext="Total {}: {}".format(category, display_data[sub_key]))
        items.append(item)
    return items

