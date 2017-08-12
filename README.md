# Beer Deep Learner


### Data Files

Beeradvocate contains all reviews for beers by users.
gender_age contains all info about the users that made reviews in Beeradvocate.

Beeradvocate.txt.gz has **1586614** total reviews. gender_age.json has **35610** total users

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

## Style Guide

#### Object Oriented Model
  We will try to follow a object oriented approach where each file in python should contain all classes
  associate with the purpose of that file. Every thing should ideally be in a class.

  Main file will execute everything need to perform the global logic

#### Spacing:
  Every logical block of code should be separate with a space and a comment explaining the logical block
  ```python
    # Puts item in list only if array is nonempty
    if len(l) != 0:
      l.append(2)

    # Otherwise create the array
    else:
      l = []
      l.append(2)
  ```

  Every method in or outside class should be separate by a two spaces and have a method header
  ```python
    # Method: printList
    # Purpose: prints all items in list
    # Arguments: l (required) - list to print out
    # Return: None
    def printList(l, amount=None):
        if amount == None:
          amount = len(l)
        for i in range(0, amount):
          print("List item %d: %s", i, str(l[i]))


    # Method: newMethod
    # ...
  ```
