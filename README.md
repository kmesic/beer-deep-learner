# Beer Deep Learner


### Data Files

Because Github has a maximum file size limit, we cannot store the entire file for the data, thus we must split them up.
After cloning locally, please run these commands to merge them into one:
```
cat Ratebeer.txt.gz.part* > Ratebeer.txt.gz
cat Beeradvocate.txt.gz.part* > Beeradvocate.txt.gz
```

This will create two files that all the data, please process then from these files, Ratebeer.txt.gz and Beeradvocate.txt.gz

### Ignoring Files from .gitignore file
We are ignorning all files with the extension .txt.gz because these are left for all massive data files.

## Notes

### Machine Learning Models:

A model in machine learning is just a way to organize the data and perform an algorithm on top of it to train it by fine tuning it. Then when ready the you can plug a arbitrary input into the model and be able to get a prediction from it.

#### Nearest Neighbors

#### Decision Trees

#### Linear Regression

#### Perceptron/SVMs
###### Kernels

#### Neural Networks/Deep Learning

#### Boosting

#### Bayesian Networks
Essentially all of CSE 150, where you build a dependency graph of binary nodes. Then calculate the probabilities of certain nodes occurring from the graph.

#### Recommenders:
###### Collaborative Filtering
Based on what you like and others who are similar to what you like, then we can recommend
certain items.

###### Content Based Filtering
Based on the item attributes, find other similar items.
