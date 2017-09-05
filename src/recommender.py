# Title: Recommender Machine File
# Author: Kenan Mesic
# Date: 08/12/17
# Purpose: All classes and methods involved with the recommender machine

import numpy as np
from sklearn import metrics
from scipy.sparse.linalg import svds
from math import sqrt
import os.path
import json


# Class: DataProcesser
# Purporse: Handles creating the recommender machine, perform machine learning
#           algorithms on data in the machine, and predicting from the data
class Recommender:

    # CLASS VARIABLES of the types of MACHINE LEARNING ALGORITHMS IT CAN PERFORM
    CC = "Collaborative Filtering"
    UI_CC = "user-item-collabrative-filtering"
    II_CC = "item-item-collabrative-filtering"
    MF_SVD = "matrix_factorization_svd"
    MF_SGD = "matrix_factorization_sgd"
    MF_ALS = "matrix_factorization_als"
    FILE_TRAIN_MAT = "../data/train_mat.txt"
    FILE_TEST_MAT = "../data/test_mat.txt"
    FILE_PRED_MAT = "../data/predications.txt"
    FILE_RECOM = "../data/recommendations.txt"
    FILE_RATINGS = "../data/top_ratings.txt"
    MAPPING_IDX_BEER = "../data/mapping_idx_beer"
    TOP_RECOMMENDATIONS = 20


    # Method: Constructor
    # Purpose: Creates the Recommeder Machine based on the data and algorithm provided
    # Arguments: trainingData (required)- data to be used for training
    #            testingData (required) - data to be used for testing
    #            totalItems (required) - total amount of unique items in the data
    #            alg (optional) - type of machine learning algorithm to use
    #            readFromFiles (optional) - read the training matrix and testing matrix
    #                                       from files
    #            empty (optional) - whether to build the machine with the training matrix
    #                               or leave it empty
    def __init__(self, trainingData=None,
                       testingData=None,
                       totalUsers=None,
                       totalItems=None,
                       alg=None,
                       saveToFile=False,
                       readFromFiles=True,
                       normalizeDataBefore=False,
                       empty=False):
        self.mappingIdxToBeer = {}

        if empty == True:
            return

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

            # Store the mapping to be able to print out the beer recommendations later
            self.mappingIdxToBeer[itemIdx] = review["name"]

        return matrix

    def cleanData(self, userMinReviews=10, itemMinReviews=5):
        userIdx = 0
        for user in self.trainingMatrix:
            totalReviews = np.count_nonzero(user)
            if totalReviews < userMinReviews:
                np.delete(self.trainingMatrix, userIdx, 0)
            userIdx += 1
        print len(self.trainingMatrix)


    # Method: matrix_factorization_svd
    # Purpose: Apply SVD, singular-value decomposition, to decompose the matrix
    #          into three matrixes that are can be multiplied together to produce
    #          a similiar training matrix...more info in README
    # Arguments: k (optional) - specify how many hidden features to find,
    #                           default to 10
    # Return: None
    def matrix_factorization_svd(self, k=10):

        # Perform singular-value decomposition and convert sigma into diagonal matrix
        self.U, sigma, self.Vt = svds(self.trainingMatrix, k=k)
        self.sigma = np.diag(sigma)


    # Method: stochastic_gradient_descent
    # Purpose: TODO
    # Arguments: TODO
    # Return: TODO
    def stochastic_gradient_descent(self,
                                    k=10,
                                    learning_rate=0.0002,
                                    regularization=0.02,
                                    iterations=1):
        # Create two matrices to be used for spliting the training matrix
        totalUsers = len(self.trainingMatrix)
        totalItems = len(self.trainingMatrix[0])
        self.U = np.random.rand(totalUsers, k)
        self.Vt = np.random.rand(k, totalItems)

        # Go through the number of steps for convergence
        for iteration in range(0, iterations):

            # Iterate through the entire training matrix
            for row_idx in range(0, totalUsers):
                for rating_idx in range(0, totalItems):
                    real_rating = self.trainingMatrix[row_idx][rating_idx]

                    # Only consider the real recorded ratings
                    if real_rating != 0:

                        # Calculate the error and perform update
                        predicted_rating = np.dot(self.U[row_idx], self.Vt[:, rating_idx])
                        eij = real_rating - predicted_rating
                        self.sgd_update(eij, row_idx, rating_idx, k, learning_rate, regularization)



    # Method: sgd_update
    # Purpose: TODO
    # Arguments: TODO
    # Return: TODO
    def sgd_update(self, eij, row_idx, rating_idx, total_k, learning_rate, regul):

        # For the passed in user and item, update their corresponding for each kth latent factor
        for k in range(0, total_k):

            # Get the old kth latent factor for the user and item
            user_feature_factor = self.U[row_idx][k]
            item_feature_factor = self.Vt[k][rating_idx]

            # Perform the update calculation and saved it for the kth latent factor of both of the user and item
            user_learn_rate_multiply = (2 * eij * item_feature_factor) - (regul * user_feature_factor)
            item_learn_rate_multiply = (2 * eij * user_feature_factor) - (regul * item_feature_factor)
            self.U[row_idx][k] = user_feature_factor + (learning_rate * user_learn_rate_multiply)
            self.Vt[k][rating_idx] = item_feature_factor + (learning_rate * item_learn_rate_multiply)


    # Method: alternating_least_squares
    # Purpose: TODO
    # Arguments: TODO
    # Return: TODO
    def alternating_least_squares(self,
                                  k=10,
                                  regularization=0.02,
                                  iterations=1):
        # Create two matrices to be used for spliting the training matrix
        # Randomize the matrices intially
        totalUsers = len(self.trainingMatrix)
        totalItems = len(self.trainingMatrix[0])
        self.U = np.random.rand(totalUsers, k)
        V = np.random.rand(totalItems, k)

        # Create a regularization matrix to be added on.
        reg = regularization * np.identity(k)

        # Iterate and alternate between keeping the User matrix constant and
        # then the Item matrix constant
        for iteration in range(0, iterations):
            for user_idx in range(0, totalUsers):
                # Solve for each user, by (VTV + reg) * u = VT * ratings_u
                #                                       u = (VTV + reg)^-1 * (VT * ratings_u)
                VTV = np.dot(V.T, V)
                ratingsU = self.trainingMatrix[user_idx, :]
                VTV_plus_reg = VTV + reg
                VTV_dot_ratingsU = np.dot(V.T, ratingsU)
                self.U[user_idx, :] = np.linalg.solve(VTV_plus_reg, VTV_dot_ratingsU)

            for item_idx in range(0, totalItems):
                # Solve for each item, by (UTU + reg) * i = UT * ratings_i
                #                                       i = (UTU + reg)^-1 * (VT * ratings_i)
                UTU = np.dot(self.U.T, self.U)
                ratingsI = self.trainingMatrix[:, item_idx]
                UTU_plus_reg = UTU + reg
                V[item_idx, :] = np.linalg.solve(UTU_plus_reg, np.dot(self.U.T, ratingsI))

        self.Vt = V.T


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
        elif alg == Recommender.MF_SVD:

            # Perform U * sigma * Vt, Add the mean_users_ratings back to get
            # predictions in between 1 and 5
            U_dot_sigma = np.dot(self.U, self.sigma)
            self.prediction = np.dot(U_dot_sigma, self.Vt) + self.mean_users_ratings

        # For SGD and ALS, just produce the predications by taking dot product of
        # the two decomposed matrices
        elif alg == Recommender.MF_SGD or alg == Recommender.MF_ALS:
            self.prediction = np.dot(self.U, self.Vt)


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


    # Method: printRecommendations
    # Purpose: TODO
    # Arguments: TODO
    # Return: TODO
    def printRecommendations(self, user=0):
        user_predications = self.prediction[user, :].tolist()
        user_ratings = self.trainingMatrix[user, :]
        ratingsNames = []
        ratingsIdx = []
        recommendationNames = []
        for idx, rating in enumerate(user_ratings):
            if rating > 0:
                beerName = self.mappingIdxToBeer[idx]
                ratingsNames.append((beerName, rating))
                ratingsIdx.append(idx)

        user_predications.sort(reverse=True)
        for idx, predication in enumerate(user_predications):
            if idx not in ratingsIdx:
                beerName = self.mappingIdxToBeer[idx]
                recommendationNames.append((beerName, predication))


        print "User " + str(user) + " rated: "
        print ratingsNames

        print "Recommendations: "
        print recommendationNames[:20]


    # Method: savePredictions
    # Purpose: TODO
    # Arguments: TODO
    # Return: TODO
    def savePredictions(self):
        np.savetxt(self.FILE_PRED_MAT, self.prediction, fmt='%1.1f')


    # Method: saveRecommendations
    # Purpose: TODO
    # Arguments: TODO
    # Return: TODO
    def saveRecommendations(self):
        with open(self.FILE_RECOM, 'w') as rec, open(self.FILE_RATINGS, 'w') as rat, open(self.FILE_PRED_MAT, 'r') as pred:
            user = 0
            for line in pred:
                user_predications = map(float, line.split())
                user_ratings = self.trainingMatrix[user, :].tolist()
                ratingsNames = []
                ratingsIdx = []
                recommendationNames = []
                user_ratings.sort(reverse=True)
                for idx, rating in enumerate(user_ratings):
                    if rating > 0:
                        beerName = self.mappingIdxToBeer[idx]
                        ratingsNames.append((beerName, rating))
                        ratingsIdx.append(idx)

                user_predications.sort(reverse=True)
                totalRecommendations = 0
                for idx, predication in enumerate(user_predications):
                    if idx not in ratingsIdx:
                        beerName = self.mappingIdxToBeer[idx]
                        recommendationNames.append((beerName, predication))
                        totalRecommendations += 1

                    if totalRecommendations >= self.TOP_RECOMMENDATIONS:
                        break

                recommendStringList = [str(r[0]) + "::" + ("%.1f" % r[1]) for r in recommendationNames]
                lineToWrite = ", ".join(recommendStringList)
                rec.write(lineToWrite + "\n")

                # Take top 20 ratings
                ratingsNames = ratingsNames[:20]
                ratingsStringList =  [str(r[0]) + "::" + ("%.1f" % r[1]) for r in ratingsNames]
                lineToWrite = ", ".join(ratingsStringList)
                rat.write(lineToWrite + "\n")

                user += 1


    # Method: loadPredications
    # Purpose: TODO
    # Arguments: TODO
    # Return: TODO
    def loadPredications(self):
        self.predications = np.loadtxt(self.FILE_PRED_MAT)


    # Method: saveMappingFromIdxToBeer
    # Purpose: TODO
    # Arguments: TODO
    # Return: TODO
    def saveMappingFromIdxToBeer(self):
        with open('../data/mapping.json', 'w') as fp:
            json.dump(self.mappingIdxToBeer, fp, sort_keys=True, indent=4)
