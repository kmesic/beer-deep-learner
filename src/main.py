import sys
from process import DataProcesser
from recommender import Recommender

class Main:

    def __init__(self, args):
        self.args = args

    def run(self):
        recommendMachine = None
        if (len(self.args) > 1 and self.args[1] == "-sp"):
            print "Building Recommender Machine"
            recommendMachine = Recommender(readFromFiles=True)

        else:
            dataProcessor = DataProcesser()
            dataProcessor.processReviews('../data/Beeradvocate.txt.gz', 100000)
            dataProcessor.parseUsers('../data/gender_age.json')
            dataProcessor.createTrainingTestingData(75)
            print(len(dataProcessor.training))
            print(len(dataProcessor.testing))

            print "Building Recommender Machine"
            recommendMachine = Recommender(dataProcessor.training,
                                           dataProcessor.testing,
                                           dataProcessor.totalUsersReviewed,
                                           dataProcessor.totalBeersReviewed,
                                           readFromFiles=False)

        print "Creating Similiarity Matrix"
        recommendMachine.createSimMatrix()

        print "Creating Predictions"
        recommendMachine.predict()

        print "Calulating Testing Error"
        error = recommendMachine.evaluate()

        print ("RMSE for User-Item: %f", error)


# Run the main
main = Main(sys.argv)
main.run()
