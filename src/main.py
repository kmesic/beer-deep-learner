from process import parserUsers, parserBeerFile
"""
users = parseUsers('../data/gender_age.json')
for key, value in users.items():
    print((key, value))
"""

beerData = parseBeerFile('../data/Beeradvocate.txt.gz')

count = 0
for key, value in beerData.items():
    print value
    count +=1
    if count > 30:
        break
