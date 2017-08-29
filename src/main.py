# Title: Main
# Author: Kenan Mesic
# Date: 08/29/17
# Purpose: Class for running the recommender program

import sys
from process import DataProcesser
from recommender import Recommender


# Class: Main
# Purporse: Trains and evaluates the recommender and handles all IO for
#           the program including command line arguments
class Main:


    # Method: Constructor
    # Purpose: Creates the main executer object to run the entire program
    # Arguments: args (required)- command line arguments of the python program
    def __init__(self, args):
        self.args = args


    # Method: run
    # Purpose: Runs the entire program - trains and evaluates the recommender,
    #                                    plus handles all IO of the program
    # Arguments: None
    # Return: None
    def run(self):
        recommendMachine = None
        saveToFile = False
        normalizeDataBefore = False
        totalRatings = 100000

        # Specify the total number of ratings to examine, ex. -tr 100000
        if ("-tr" in self.args):
            try:
                idxTr = self.args.index("-tr")
                totalRatings = int(self.args[idxTr + 1])
            except (ValueError, IndexError) as e:
                print "Invalid Usage of arguments in program for -tr"
                return

        # Whether or not to save the training matrix to a file, ex. -sf
        if ("-sf" in self.args):
            saveToFile = True

        # Whether or not to normalize the data before mostly used for svds
        # and user-item filtering, ex. -ndb
        if ("-ndb" in self.args):
            normalizeDataBefore = True

        # Whether to grab the training matrix from a file, ex. -sp
        if ("-sp" in self.args):
            print "Building Recommender Machine"
            recommendMachine = Recommender(saveToFile=saveToFile,
                                           normalizeDataBefore=normalizeDataBefore,
                                           readFromFiles=True)

        # Otherwise build the training matrix by going through the ratings data
        else:

            # Process all the data
            print("Processing " + str(totalRatings) + " ratings")
            dataProcessor = DataProcesser()
            dataProcessor.processReviews('../data/Beeradvocate.txt.gz', totalRatings)
            dataProcessor.parseUsers('../data/gender_age.json')
            dataProcessor.createTrainingTestingData(75)
            print(len(dataProcessor.training))
            print(len(dataProcessor.testing))

            # Calculate the sparsity of the training matrix
            numerator = float(len(dataProcessor.training))
            denominator = float(dataProcessor.totalUsersReviewed * dataProcessor.totalBeersReviewed)
            sparsity = numerator/denominator
            sparsity *= 100
            print("Sparsity Percentage: " + str(sparsity))

            # Build the reccommender machine
            print "Building Recommender Machine"
            recommendMachine = Recommender(dataProcessor.training,
                                           dataProcessor.testing,
                                           dataProcessor.totalUsersReviewed,
                                           dataProcessor.totalBeersReviewed,
                                           saveToFile=saveToFile,
                                           normalizeDataBefore=normalizeDataBefore,
                                           readFromFiles=False)

        alg = ""

        # Model based filtering using matrix factorization
        # Specify with -mf {kvalue}, ex. -mf 25
        # kvalue - the number of k latent factors to use
        if ("-mf" in self.args):
            idxMf = self.args.index("-mf")
            kValue = 10
            try:
                kValue = int(self.args[idxMf + 1])
            except (ValueError, IndexError) as e:
                print("Default value of k being used: " + str(kValue))

            # Specify which matrix factorization algorithm to use
            # -mf {kvalue} {svd|sgd}, ex. -mf svd | -mf 10 sgd
            if ("svd" in self.args):
                alg = "Matrix Factorization using SVDs"

                # Decompose the training matrix into two matrices with k latent factors using svd
                print("Decomposing training matrix into smaller matrices with hidden features of " + str(kValue))
                recommendMachine.matrix_factorization_svd(k=kValue)

                # Create a predictions matrix to know all the predicted ratings
                print "Creating Predictions"
                recommendMachine.predict(alg=recommendMachine.MF_SVD)

            # Use stochastic gradient descent
            elif ("sgd" in self.args):
                alg = "Matrix Factorization using Stochastic Gradient Descent"
                iterations = [1, 2, 5, 10, 25, 50, 100, 200]

                # Decompose the training matrix into two matrices with k latent factors using sgd
                # and pass in the num of iterations to perform sgd on the training matrix
                print("Decomposing training matrix into smaller matrices with hidden features of " + str(kValue))
                recommendMachine.stochastic_gradient_descent(k=kValue, iterations=1)

                # Create a predictions matrix to get all the predicted ratings
                print "Creating Predictions"
                recommendMachine.predict(alg=recommendMachine.MF_SGD)

            # Otherwise error because no algorithm was specified to use
            else:
                print "You need to specify an algorithm for matrix factorization to use.\nEx. -mf sgd | -mf 10 sgd"
                return

        # Otherwise default to perform user item collaborative filtering
        else:
            alg = "User Item Collaborative Filtering"

            print "Creating Similiarity Matrix"
            recommendMachine.createSimMatrix(sim="cosine")

            print "Creating Predictions"
            recommendMachine.predict()

        # Evaluate the reccommender machine using RMSE
        print "\nEvaluating the Recommender Machine using the testing data"
        error = recommendMachine.evaluate()
        print ("RMSE for " + alg + " : " + str(error))


# Run the main with the command line arguments
main = Main(sys.argv)
main.run()
