from process import Parser


parser = Parser()
parser.parseBeerFile('../data/Beeradvocate.txt.gz', 100)
#parser.parseUsers('../data/gender_age.json')
"""for key, value in parser.users.items():
    print ((key, value))
"""

print(parser.totalReviews)
