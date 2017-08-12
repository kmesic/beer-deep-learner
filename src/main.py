from process import Parser


parser = Parser()
parser.parseBeerFile('../data/Beeradvocate.txt.gz')
#parser.parseUsers('../data/gender_age.json')
"""for key, value in parser.users.items():
    print ((key, value))
"""
count = 0
for key, value in beerData.items():
    print value
    count +=1
    if count > 30:
        break
