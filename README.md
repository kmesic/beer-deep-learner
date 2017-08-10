# Beer Deep Learner

### Data Files
Because Github has a maximum file size limit, we cannot store the entire file for the data, thus we must split them up.
After cloning locally, please run these commands to merge them into one:
```
cat Ratebeer.txt.gz.part* > Ratebeer.txt.gz
cat Beeradvocate.txt.gz.part* > Beeradvocate.txt.gz 
```

This will create two files that all the data, please process then from these files, Ratebeer.txt.gz and Beeradvocate.txt.gz

##### .gitignore
It is ignorning all files with the extension .txt.gz
