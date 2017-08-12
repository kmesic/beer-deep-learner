from process import DataProcesser


dataProcessor = DataProcesser()
#parser.parseBeerFile('../data/Beeradvocate.txt.gz', 100)
dataProcessor.processReviews('../data/Beeradvocate.txt.gz', 1000)
dataProcessor.parseUsers('../data/gender_age.json')
dataProcessor.createTrainingTestingData(75)
print(len(dataProcessor.training))
print(len(dataProcessor.testing))
