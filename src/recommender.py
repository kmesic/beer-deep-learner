# Title: Recommender Machine File
# Author: Kenan Mesic
# Date: 08/12/17
# Purpose: All classes and methods involved with the recommender machine

# Class: DataProcesser
# Purporse: Handles creating the recommender machine, perform machine learning
#           algorithms on data in the machine, and predicting from the data
class Recommender:

    # CLASS VARIABLES of the types of MACHINE LEARNING ALGORITHMS IT CAN PERFORM
    UI_CC = "user-item-collabrative-filtering"

    """TODO: ADD arguments to header"""
    # Method: Constructor
    # Purpose: Creates the Recommeder Machine based on the data and algorithm provided
    # Arguments: trainingData (required)- data to be used for training
    #            testingData (required) - data to be used for testing
    #
    #            alg (optional) - type of machine learning algorithm to use
    def __init__(self, trainingData, testingData, totalItems, alg=None):
        if alg == None:
            alg = self.UI_CC

        if alg == self.UI_CC:
            self.trainingMatrix = self.createUserItemMatrix(trainingData, totalItems)
            self.testingMatrix = self.createUserItemMatrix(testingData, totalItems)


    # Method: createUserItemMatrix
    # Purpose: Create a User Item Matrix - m Users, n items = m * n matrix
    # Arguments: data (required) - data to be used to build the matrix
    # Return: the matrix created
    def createUserItemMatrix(self, data, totalItems):
        # Mapping of users and items to the row and column in the matrix
        users = {}
        items = {}
        userCounter = 0
        itemCounter = 0

        # Initialize the matrix
        matrix = []

        # Go through each review in the data and add the data of the review to the matrix
        for review in data:
            # Get the idx of the user in the matrix
            userIdx = -1
            user = review["profileName"]
            if user in users:
                userIdx = users[user]

            # If does not exist create a new row for the user
            else:
                matrix.append([0.0 for i in range(0, totalItems)])
                userIdx = userCounter
                users[user] = userIdx
                userCounter += 1

            # Get the idx of the item in the matrix
            item = review["beerId"]
            itemIdx = -1
            if item in items:
                itemIdx = items[item]

            # If does not exist use a unused idx from the row
            else:
                itemIdx = itemCounter
                items[item] = itemIdx
                itemCounter += 1

            # Convert the overall rating to float and save to the matrix
            matrix[userIdx][itemIdx] = float(review["overall"])

        return matrix
