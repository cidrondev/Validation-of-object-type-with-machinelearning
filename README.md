# Validation-of-object-type-with-machinelearning
Program was created by Daniel Persson and Petter Gullin.
This program was created for our B-essay (B-uppsats), the B-essay is included in the repository.

Thank you Albin Larsson [Abbe98](https://github.com/Abbe98) on github for all the techincal help and guidance on this project

# Models and CSV files from our testing
[Download link](https://drive.google.com/file/d/1BidRbOqKRJIzD13vE3YMdORzOQQJCgZu/view?usp=sharing)

# To use the program
| Programfolders | Start files
| ------------- |:-------------:|
| trainingmaterial_app|main.py|
| Trainingtensorflow_scripts|create_training_data.py, create_training_data.py|
| Validation_scripts |compare_folders.py, manual_validation.py, validation.py|

## What is this program?
These programs download, creates and validates picture from Swedish National Heritage Board (Riksantikvarieämbetet) database.
This throught [API ksamsok](http://www.ksamsok.se/api/).

## Why was it created?
These programs were created as the Swedish National Heritage Board saw a problem with the quailty of metadata.

## Purpose of the program
To find wrongfully classifed metadata in their database.

# What do the programs do?
Here comes lists about the programs.

## General notes
+ The program either validates from a retrained model or a custom trained model.
+ The files in this repository is the two best models from our testing trained on aprox 22000 pictures.
+ The image csv files are before the balancing of the two folders to equal levels.

## First program
+ Handels the downloading of the pictures
+ Deleting all corrupted files
+ Removing the info of deleted files from the csv files.

## Second program
+ Randomising image files in a folder
+ Creates the trainingdata
### Retrained model
+ For the retrained model use this [tutorial](https://www.tensorflow.org/hub/tutorials/image_retraining)

## Third program
+ Validate against the database by instution with the wrongfully validated pictures getting downloaded
+ Validate manually from either a folder or a file
+ Compare two folders and printout the number of same files in the folders
