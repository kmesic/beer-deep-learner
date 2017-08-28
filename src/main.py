import sys
from process import DataProcesser
from recommender import Recommender

class Main:

    def __init__(self, args):
        self.args = args

    def run(self):
        recommendMachine = None
        saveToFile = False
        normalizeDataBefore = False
        totalRatings = 100000

        if ("-tr" in self.args):
            try:
                idxTr = self.args.index("-tr")
                totalRatings = int(self.args[idxTr + 1])
            except (ValueError, IndexError) as e:
                print "Invalid Usage of arguments in program for -tr"
                return

        if ("-sf" in self.args):
            saveToFile = True

        if ("-ndb" in self.args):
            normalizeDataBefore = True

        if ("-sp" in self.args):
            print "Building Recommender Machine"
            recommendMachine = Recommender(saveToFile=saveToFile,
                                           normalizeDataBefore=normalizeDataBefore,
                                           readFromFiles=True)

        else:
            print("Processing " + str(totalRatings) + " ratings")
            dataProcessor = DataProcesser()
            dataProcessor.processReviews('../data/Beeradvocate.txt.gz', totalRatings)
            dataProcessor.parseUsers('../data/gender_age.json')
            dataProcessor.createTrainingTestingData(75)
            print(len(dataProcessor.training))
            print(len(dataProcessor.testing))

            numerator = float(len(dataProcessor.training))
            denominator = float(dataProcessor.totalUsersReviewed * dataProcessor.totalBeersReviewed)
            sparsity = numerator/denominator
            sparsity *= 100
            print("Sparsity Percentage: " + str(sparsity))

            print "Building Recommender Machine"
            recommendMachine = Recommender(dataProcessor.training,
                                           dataProcessor.testing,
                                           dataProcessor.totalUsersReviewed,
                                           dataProcessor.totalBeersReviewed,
                                           saveToFile=saveToFile,
                                           normalizeDataBefore=normalizeDataBefore,
                                           readFromFiles=False)

        alg = "User Item Collaborative Filtering"
        # Model based filtering
        if ("-mf" in self.args):
            idxMf = self.args.index("-mf")
            kValue = 10
            try:
                kValue = int(self.args[idxMf + 1])
            except (ValueError, IndexError) as e:
                print("Default value of k being used: " + str(kValue))

            if ("svd" in self.args):
                print("Decomposing training matrix into smaller matrices with hidden features of " + str(kValue))
                recommendMachine.matrix_factorization_svd(k=kValue)

                print "Creating Predictions"
                recommendMachine.predict(alg=recommendMachine.MF_SVD)
            elif ("sgd" in self.args):
                print("Decomposing training matrix into smaller matrices with hidden features of " + str(kValue))
                recommendMachine.stochastic_gradient_descent(k=kValue)

                print "Creating Predictions"
                recommendMachine.predict(alg=recommendMachine.MF_SGD)
        else:
            print "Creating Similiarity Matrix"
            recommendMachine.createSimMatrix(sim="cosine")

            print "Creating Predictions"
            recommendMachine.predict()

        print "Calulating Testing Error"
        error = recommendMachine.evaluate()


        print ("RMSE for " + alg + " : " + str(error))


# Run the main
main = Main(sys.argv)
main.run()
