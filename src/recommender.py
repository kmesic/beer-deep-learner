# Title: Recommender Machine File
# Author: Kenan Mesic
# Date: 08/12/17
# Purpose: All classes and methods involved with the recommender machine

import numpy as np
from sklearn import metrics
from scipy.sparse.linalg import svds
from math import sqrt
import os.path


# Class: DataProcesser
# Purporse: Handles creating the recommender machine, perform machine learning
#           algorithms on data in the machine, and predicting from the data
class Recommender:

    # CLASS VARIABLES of the types of MACHINE LEARNING ALGORITHMS IT CAN PERFORM
    CC = "Collaborative Filtering"
    UI_CC = "user-item-collabrative-filtering"
    II_CC = "item-item-collabrative-filtering"
    MF = "matrix_factorization"
    FILE_TRAIN_MAT = "../data/train_mat.txt"
    FILE_TEST_MAT = "../data/test_mat.txt"


    # Method: Constructor
    # Purpose: Creates the Recommeder Machine based on the data and algorithm provided
    # Arguments: trainingData (required)- data to be used for training
    #            testingData (required) - data to be used for testing
    #            totalItems (required) - total amount of unique items in the data
    #            alg (optional) - type of machine learning algorithm to use
    #            readFromFiles (optional) - read the training matrix and testing matrix
    #                                       from files
    def __init__(self, trainingData=None,
                       testingData=None,
                       totalUsers=None,
                       totalItems=None,
                       alg=None,
                       saveToFile=False,
                       readFromFiles=True,
                       normalizeDataBefore=False):
        if alg == None:
            alg = self.CC

        # Perform User-Item Collaborative Filtering
        if alg == self.CC:

            # Load training matrix if already saved
            if readFromFiles and os.path.isfile(self.FILE_TRAIN_MAT):
                self.trainingMatrix = np.loadtxt(self.FILE_TRAIN_MAT)
            else:
                # Create training matrix and convert these to numpy arrays for faster calculations
                self.trainingMatrix = self.createUserItemMatrix(trainingData, totalUsers, totalItems)

                self.normalizeDataBefore = normalizeDataBefore

                # Average of each row
                mean_users_ratings = self.trainingMatrix.mean(axis=1)

                # Convert the mean into multiple rows of one column instead of one
                # row to be able to subtract each mean of the row by each element in
                # row of the user
                self.mean_users_ratings = mean_users_ratings.reshape(-1, 1)

                if normalizeDataBefore == True:
                    self.trainingMatrix = self.trainingMatrix - self.mean_users_ratings

                if saveToFile == True:
                    # Save for future use
                    np.savetxt(self.FILE_TRAIN_MAT, self.trainingMatrix, fmt='%1.1f')

            # Load testing matrix if already saved
            if readFromFiles and os.path.isfile(self.FILE_TEST_MAT):
                self.testingMatrix = np.loadtxt(self.FILE_TEST_MAT)
            else:
                # Create testing matrix and convert these to numpy arrays for faster calculations
                self.testingMatrix = self.createUserItemMatrix(testingData, totalUsers, totalItems)

                if saveToFile == True:
                    # Save for future use
                    np.savetxt(self.FILE_TEST_MAT, self.testingMatrix, fmt='%1.1f')


    # Method: createUserItemMatrix
    # Purpose: Create a User Item Matrix - m Users, n items = m * n matrix
    # Arguments: data (required) - data to be used to build the matrix
    #            totalUsers (required) - total amount of users
    #            totalItems (required) - total amount of items
    # Return: the matrix created
    def createUserItemMatrix(self, data, totalUsers, totalItems):

        # Initialize the matrix
        matrix = np.zeros((totalUsers, totalItems))

        # Go through each review in the data and add the data of the review to the matrix
        for review in data:
            # Get the idx of the user in the matrix
            userIdx = review["userIdx"]

            # Get the idx of the item in the matrix
            itemIdx = review["itemIdx"]

            # Convert the overall rating to float and save to the matrix
            matrix[userIdx, itemIdx] = float(review["overall"])

        return matrix


    # Method: matrix_factorization
    # Purpose: Apply SVD, singular-value decomposition, to decompose the matrix
    #          into three matrixes that are can be multiplied together to produce
    #          a similiar training matrix...more info in README
    # Arguments: None
    # Return: None
    def matrix_factorization(self):
        self.U, sigma, self.Vt = svds(self.trainingMatrix, k=20)
        self.sigma = np.diag(sigma)


    # Method: predict
    # Purpose: Create a prediction matrix by performing the formulas described
    #          in the README
    # Arguments: alg (optional) - algorithm to use (user-item or item-item),
    #                             defaults to user-item
    # Return: None
    def predict(self, alg="user"):
        self.prediction = []

        # User-item algorithm using the similarity matrix
        if alg == "user":

            if self.normalizeDataBefore == False:
                trainingMatrix_adjusted = self.trainingMatrix - self.mean_users_ratings

            elif self.normalizeDataBefore == True:
                trainingMatrix_adjusted = self.trainingMatrix

            # Calculate the prediction matrix based on the formula in README
            denominator = np.abs(self.simMatrix).sum(axis=1)[:, np.newaxis]
            numerator = self.simMatrix.dot(trainingMatrix_adjusted)
            self.prediction = self.mean_users_ratings + (numerator/denominator)


        # Similiar formula to user-item expect no need to account for user bias
        # so no need to subtract by mean on each row and then add it back at
        # the end.
        elif alg == "item":
            numerator = self.trainingMatrix.dot(self.simMatrix)

            # Same as user-item because similarity matrix is diagonal
            # expect keep summation as one long list that will be divided by
            # each row
            denominator = np.array([np.abs(self.simMatrix).sum(axis=1)])
            self.prediction = numerator/denominator

        # From matrix_factorization, we can take the decomposed matrix and apply
        # dot product to get the predictions...more on README
        elif alg == "matrix_factorization":

            # Perform U * sigma * Vt, Add the mean_users_ratings back to get
            # predictions in between 1 and 5
            U_dot_sigma = np.dot(self.U, self.sigma)
            self.prediction = np.dot(U_dot_sigma, self.Vt) + self.mean_users_ratings



    # Method: evaluate
    # Purpose: Perform Root Mean Square Error on the prediction and test data
    # Arguments: None
    # Return: Root Mean Square Error from recommender and test data
    def evaluate(self, kind="rmse"):
        # Only what to compare what is in the test data
        test_data_nonzero_idxs = self.testingMatrix.nonzero()

        # Get all nonzero ratings from test data and its corresponding predictions
        # then run RMSE on it
        test_ratings = self.testingMatrix[test_data_nonzero_idxs].flatten()
        predict_ratings = self.prediction[test_data_nonzero_idxs].flatten()
        mse = metrics.mean_squared_error(predict_ratings, test_ratings)
        if kind == "rmse":
            return sqrt(mse)
        elif kind == "mse":
            return mse
        else:
            return 0


    # Method: createSimMatrix
    # Purpose: Create a Similarity Matrix from the training data and use cosine
    #          similarity as a way to find similarity between two users or items
    # Arguments: alg (optional) - algorithm to use (user-item or item-item),
    #                             defaults to user-item
    #            sim (optional) - similarity function to use,
    #                             defaults to cosine
    # Return: None
    def createSimMatrix(self, alg="user", sim="cosine"):
        if alg == "user":
            self.simMatrix = metrics.pairwise.pairwise_distances(self.trainingMatrix,metric=sim)
        elif alg == "item":
            self.simMatrix = metrics.pairwise.pairwise_distances(self.trainingMatrix.T,metric=sim)


    """ THIS METHOD IS FOR LEARNING PURPOSES NOT PRODUCTION"""
    # Method: createSimilarityMatrixLearn
    # Purpose: Create a Similarity Matrix from the training data and use cosine
    #          similarity as a way to find similarity between two users or items
    # Arguments: alg (optional) - algorithm to use (user-item or item-item),
    #                             defaults to user-item
    # Return: None
    def createSimilarityMatrix(self, alg=None, speed="fast"):
        # small number to deal with divides by 0
        errorDecimal = 1e-9
        if alg == None:
            alg = self.UI_CC

        if speed == "fast":
            # Perform cosine similarity dependent on algorithm
            if alg == self.UI_CC:
                simMatrix = self.trainingMatrix.dot(self.trainingMatrix.T) + errorDecimal
            elif alg == self.II_CC:
                simMatrix = self.trainingMatrix.T.dot(self.trainingMatrix) + errorDecimal
            normalization = np.array([np.sqrt(np.diagonal(simMatrix))])

            self.similarityMatrix = simMatrix/(normalization * normalization.T)
