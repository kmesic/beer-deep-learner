from process import DataProcesser
from recommender import Recommender


dataProcessor = DataProcesser()
#parser.parseBeerFile('../data/Beeradvocate.txt.gz', 100)
dataProcessor.processReviews('../data/Beeradvocate.txt.gz', 100)
dataProcessor.parseUsers('../data/gender_age.json')
dataProcessor.createTrainingTestingData(75)
print(len(dataProcessor.training))
print(len(dataProcessor.testing))
recommendMachine = Recommender(dataProcessor.training, dataProcessor.testing,
                               dataProcessor.totalBeersReviewed)

print(recommendMachine.trainingMatrix)



print(dataProcessor.totalUsersReviewed)
print(dataProcessor.totalBeersReviewed)
