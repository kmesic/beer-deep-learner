# Title: Data Processing File
# Author: Kenan Mesic
# Date: 08/09/17
# Purpose: All classes and methods involved with processing any sort of data

import gzip
import json
import random

"""
Beer Review Structure in File:
---Ratings out of 5 in float---
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


# Class: DataProcesser
# Purporse: Processes all data and exposes utility methods to perform
#           operations on the data
class DataProcesser:


    # Method: Constructor
    # Purpose: Create the Parser object and initialize storage for data
    # Arguments: None
    def __init__(self):
        self.users = {}
        self.beers = {}
        self.reviews = []
        self.totalReviews = 0
        self.totalUsers = 0
        self.totalUserReviewed = 0
        self.totalBeersReviewed = 0
        self.totalItems = 0
        self.training = []
        self.testing = []


    # Method: parseBeerFile
    # Purpose: Grab all the beer data and format it into a nice dictionary
    # Arguments: filename - path to file trying to open
    # Return: None
    def parseBeerFile(self, filename, trainPercent):
        self.beers = {}

        # Open the gzip file
        with gzip.open(filename) as f:
            beer = {}
            review = {}
            # Loop through all the lines of the file
            for line in f:
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

                    # If on the last field for beer, save the beer if does not
                    # exist in the beers dict
                    if key[1] == 'style':
                        idValue = beer["beerId"]
                        if idValue not in self.beers:
                            self.beers[idValue] = beer
                # Otherwise on a review
                elif key[0] == 'review':
                    # If the start of the review
                    if key[1] == 'appearance':
                        review = {}
                    review[key[1]] = value

                    # If at the end of the review, save the review to beer
                    if key[1] == 'text':
                        savedBeer = self.beers[beer["beerId"]]

                        # If the first review for the beer
                        if "reviews" not in savedBeer:
                            savedBeer["reviews"] = []
                        savedBeer["reviews"].append(review)
                        self.totalReviews += 1


    # Method: processReviews
    # Purpose: Grab amount of reviews from the file and store in a array
    #          If amount of reviews is less than amount passed in, then process
    #          all reviews in file
    # Arguments: filename (required) - path to file trying to open
    #            amount (optional) - total amount of reviews to process
    #                                defaults to 1 trillion
    # Return: None
    def processReviews(self, filename, amount=1000000000000):
        self.reviews = []
        review = {}
        beers = {}
        users = {}
        uniqueIdxUser = 0
        uniqueIdxItem = 0
        filterIdxUser = 0
        filterIdxItem = 0
        self.totalReviews = 0
        beersWithMoreRatings = {}
        usersWithMoreRatings = {}

        # Open the gzip file
        with gzip.open(filename) as f:
            # Loop through all the lines of the file
            for line in f:
                # If passed total reviews stop processing
                if self.totalReviews >= amount:
                    break

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
                    # If on field name then new review starting
                    if key[1] == 'name':
                        review = {}

                    # Used to count number of unique beers
                    elif key[1] == 'beerId':
                        if value in beers:
                            #review["itemIdx"] = beers[value][0]
                            #beers[value] = (beers[value][0], beers[value][1] + 1)
                            beers[value] += 1
                            if (beers[value] == 5):
                                beersWithMoreRatings[value] = filterIdxItem
                                filterIdxItem += 1
                        else:
                            beers[value] = 1
                            #beers[value] = (uniqueIdxItem, 1)
                            #review["itemIdx"] = uniqueIdxItem
                            #uniqueIdxItem += 1


                    review[key[1]] = value

                # Otherwise on a review
                elif key[0] == 'review':
                    review[key[1]] = value

                    # Used to count number of unique users
                    if key[1] == 'profileName':
                        if value in users:
                            #review["userIdx"] = users[value][0]
                            #users[value] = (users[value][0], users[value][1] + 1)
                            users[value] += 1
                            if (users[value] == 10):
                                usersWithMoreRatings[value] = filterIdxUser
                                filterIdxUser += 1
                        else:
                            users[value] = 1
                            #users[value] = (uniqueIdxUser, 1)
                            #review["userIdx"] = uniqueIdxUser
                            #uniqueIdxUser += 1

                    # If at the end of the review, save the review to reviews
                    elif key[1] == 'text':
                        self.reviews.append(review)
                        self.totalReviews += 1


        # Count the total amount of unique beers and users from the reviews
        #self.totalBeersReviewed = len(beers)
        #self.totalUsersReviewed = len(users)
        self.totalBeersReviewed = len(beersWithMoreRatings)
        self.totalUsersReviewed = len(usersWithMoreRatings)

        print self.totalBeersReviewed
        print self.totalUsersReviewed
        print len(beersWithMoreRatings)
        print len(usersWithMoreRatings)

        oldReviews = self.reviews
        self.reviews = []
        for review in oldReviews:
            if review['profileName'] in usersWithMoreRatings and review['beerId'] in beersWithMoreRatings:
                review["userIdx"] = usersWithMoreRatings[review['profileName']]
                review["itemIdx"] = beersWithMoreRatings[review['beerId']]
                self.reviews.append(review)

        with open('../data/beer_count.json', 'w') as fp:
            json.dump(beers, fp, sort_keys=True, indent=4)


    # Method: parseUsers
    # Purpose: Parse all the users from the JSON file
    # Arguments: filename (required)- path to file trying to open
    # Return: None
    def parseUsers(self, filename):
        self.users = {}
        with open(filename) as f:
            # Loop through all users and save them
            for line in f:
                # Conform to JSON standards with double quotes
                line = line.replace("'", '"')
                j = json.loads(line)
                self.users[j['username']] = j
                self.totalUsers += 1


    # Method: shuffleReviews
    # Purpose: Shuffles the reviews randomly
    # Arguments: None
    # Return: None
    def shuffleReviews(self):
        random.shuffle(self.reviews)


    # Method: createTrainingTestingData
    # Purpose: Shuffles the reviews and splits based on the percentage
    # Arguments: percent (optional) - the amount of data to be in training,
    #                                 rest goes into test data,
    #                                 default is to put all into training
    # Return: None
    def createTrainingTestingData(self, percent=100):
        # Shuffle the reviews randomly
        self.shuffleReviews()

        # Split the arrays according to what was passed in
        percent = float(percent)
        reviewsSplit = len(self.reviews) * (percent/100)
        reviewsSplit = int(round(reviewsSplit))
        self.training = self.reviews[:reviewsSplit]
        self.testing = self.reviews[reviewsSplit:]


    # Method: printReviews
    # Purpose: Print x amount of reviews if passed in
    # Arguments: amount(optional) - amount of reviews to print, if not provided
    #                               prints all reviews
    # Return: None
    def printReviews(self, amount=None):
        # Default is print all reviews
        if amount == None:
            amount = len(self.reviews)

        # Print the amount of reviews
        for i in range(0, amount):
            print self.reviews[i]
