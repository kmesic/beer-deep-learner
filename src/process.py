# Title: Data Parser File
# Author: Kenan Mesic
# Date: 08/09/17

import gzip
import re
import json

"""
Beer Review Structure in File:
---Ratings out of 5 in foat---
beer/name:
beer/beerId:
beer/brewerId:
beer/ABV:
beer/style:
review/appearance:
review/aroma:
review/palate:
review/taste:
review/overall:
review/time:
review/profileName:
review/text:
"""

# Grab all the beer data and format it into a nice dictionary
def parseBeerFile(filename):
    count = 0
    beers = []

    # Open the gzip file
    with gzip.open(filename) as f:
        beers = {}
        beer = {}
        review = {}
        count = 0
        # Loop through all the lines of the file
        for line in f:
            if count < 30:
                print line
            count += 1
            # Clean the file by striping all tabs and newlines
            line = line.strip()
            line = line.replace("\t", " ")

            # If line is empty ingore
            if line == '':
                continue
            # Get the keyValue Pair
            keyValue = line.split(':')

            key = keyValue[0].split('/')
            value = keyValue[1]

            # Determine if looking at beer or review
            if key[0] == 'beer':
                # If on field name then new beer starting
                if key[1] == 'name':
                    beer = {}
                beer[key[1]] = value

                # If on the last field for beer, save the beer if does not exist
                # in the beers dict
                if key[1] == 'style':
                    idValue = beer["beerId"]
                    if idValue not in beers:
                        beers[idValue] = beer
            # Otherwise on a review
            elif key[0] == 'review':
                # If the start of the review
                if key[1] == 'appearance':
                    review = {}
                review[key[1]] = value

                # If at the end of the review, save the review to beer
                if key[1] == 'text':
                    savedBeer = beers[beer["beerId"]]

                    # If the first review for the beer
                    if "reviews" not in savedBeer:
                        savedBeer["reviews"] = []
                    savedBeer["reviews"].append(review)
    return beers

# Parse all the users from the JSON file
def parseUsers(filename):
    users = {}
    with open(filename) as f:
        # Loop through all users and save them
        for line in f:
            # Conform to JSON standards with double quotes
            line = line.replace("'", '"')
            j = json.loads(line)
            users[j['username']] = j

    return users
