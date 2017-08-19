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
            dataProcessor = DataProcesser()
            dataProcessor.processReviews('../data/Beeradvocate.txt.gz', 1000000)
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
            alg = "Matrix Factorization"

            print "Decomposing training matrix into smaller matrices"
            recommendMachine.matrix_factorization()

            print "Creating Predictions"
            recommendMachine.predict(alg=recommendMachine.MF)
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
