# Beer Deep Learner
### Running the Program
Be in the src directory.

Usage:
```
python ./main.py -tr 100000 -mf sgd
python ./main.py -tr 100000 -mf 10 sgd
python ./main.py -tr 100000 -mf 10 svd
python ./main.py -tr 100000 -sf -ndb
python ./main.py -tr 100000
python ./main.py -sp -ndb
python ./main.py -sp -ndb -mf svd

Options:
-tr {totalRatings}      Specify the number of ratings to use for the data.
-sf                     Save the training matrix to a file to use for later.
-ndb                    Normalize the data before training. Do not use with sgd algorithm.
-sp                     Skip processing the data, use the saved file to get the training matrix.
-mf [kvalue] {svd|sgd}  Matrix Factorization using either svd or sgd algorithm.
                        kvalue is optional and specifies the number of k latent factors to use.
```

### Package and Language Dependencies
```
Python 2.7
numpy
sklearn
scipy
```

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

Evaluating your recommender:
* Offline Ways:
  * Root Mean Squared Error (RMSE) - You take only a subset of these ratings, say 80% (called the train set), build the RS on them, and then ask the RS to predict the ratings on the 20% you’ve hidden (the test set). And so it may happen that a test user rated some item with 4 stars, but your model predicts 3.5, hence it has an error of 0.5 on that rating, and that’s exactly where RMSE comes from. Then you just compute the average of the errors from the whole test set using a formula and get a final result of 0.71623
  * Recall - You may have hidden 4 purchased items and ask the RS for 10 items. You may get 0%, 25%, 50%, 75%, or 100% accuracy for that user, depending on how many of the hidden 4 appeared in the recommended 10. Take the average over the entire test set.
  * Mean Absolute Error (MAE)- Same as RMSE, just does not penalize on large errors

* Online Ways:
  * Click-Through Rate (CTR) - number of times the user clicked on a recommendation
  * Conversion Rate (CR) - number of times the user went ahead and bought the recommendation

###### Collaborative Filtering

Normalization of data:

If we normalize ratings, by subtracting from each rating the average rating
of that user, we turn low ratings into negative numbers and high ratings into
positive numbers. If we then take the cosine distance, we find that users with
opposite views of the movies they viewed in common will have vectors in almost
opposite directions, and can be considered as far apart as possible. However,
users with similar opinions about the movies rated in common will have a
relatively small angle between them


Based on what you like and others who are similar to what you like, then we can recommend
certain items.

Steps:

1. Build a user to item matrix. This means for every user have a ratings row that has the rating of each item.
2. Build similarity matrix
3. Run prediction algorithm
4. Evaluate it

###### Content Based Filtering
Based on the item attributes, find other similar items.

Links Used:
https://cambridgespark.com/content/tutorials/implementing-your-own-recommender-systems-in-Python/index.html

http://blog.ethanrosenthal.com/2015/11/02/intro-to-collaborative-filtering/

https://medium.com/recombee-blog/evaluating-recommender-systems-choosing-the-best-one-for-your-business-c688ab781a35

## Style Guide

#### Object Oriented Model
  We will try to follow a object oriented approach where each file in python should contain all classes
  associate with the purpose of that file. Every thing should ideally be in a class.

  Main file will execute everything need to perform the global logic

#### Headers/Spacing:
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

  Every file should have a file header
  ```python
    # Title: Processor File
    # Author: Foo Bar
    # Date: 01/01/1970
    # Purpose: All classes and methods involved with the processor
  ```

  Every Class should have a class header
  ```python
  # Class: UNIX
  # Purpose: Handles the UNIX OS  
  ```
