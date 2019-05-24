import os
import cv2
import time
import random
import pickle
import numpy as np
from tqdm import tqdm
from pathlib import Path
import matplotlib.pyplot as plt
"""[summary]
This file handels all the formatting of a choosen traningdata
Tthe code is based on sentdex youtube tutorial see link below
https://www.youtube.com/watch?v=j-3vuBynnOE&list=PLQVvvaa0QuDfhTox0AjmQ6tvTgMBZBEXN&index=2
Author: Daniel Persson & Petter Gullin 2019-05-21
"""

LOCATION_PATH = Path.cwd().parent / 'trainingdata'
SAVE_LOCATION_PATH = Path.cwd().parent / "tensorflowdata"
#Location of image folders
DATAIN = LOCATION_PATH / "trainingdata_images"
#Location to output data
DATAOUT = SAVE_LOCATION_PATH / "tensorflowarrays"

#Folders name
CATEGORIES = ["NAME_OF_FOLDER","NAME_OF_FOLDER"]
#Image size we want picture to be converted to for example 64 = 64px*64px
IMG_SIZE = 64

def create_training_data(categories,img_size):
    """[summary]
    Creates our traningdata
    Args:
        categories ([LIST]): [Our two folders we want to format]
        img_size ([INT]): [The size we want to make the image (example: 64 = 64x64)]
    """
    #create array
    training_data = []
    for category in categories:
        path = DATAIN / category
        class_num = categories.index(category)
        i=0
        for img in tqdm(os.listdir(path)):
            try:
                i = i+1
                img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([new_array, class_num])
            except:
                print("Error:{}:{}".format(i,category))
    return training_data

def shuffledata(categories):
    """[summary]
    Shuffels our data to make model train on mixed data
    Args:
        training_data ([LIST]): [Our traning data in array format]
    """
    for category in categories:
        path = DATAIN / category
        list_images = os.listdir(path)
        random_nums = random.sample(range(1,len(list_images)+1),len(list_images))
        count = 0
        for image in list_images:
            name = F"{random_nums[count]}-{image}"
            os.rename(path / image,path / name)
            count +=1
            
def convert_traning_data(training_data,img_size):
    """[summary]
    Converts our traningdata to two arrays
    Args:
        training_data ([LIST]): [Our traning data in array format]
        img_size ([INT]): [The size we want to make the image (example: 64 = 64x64)]
    """
    image_array_X = []
    image_array_Y = []
    for features, label in training_data:
       image_array_X.append(features)
       image_array_Y.append(label)
    image_array_X = np.array(image_array_X).reshape(-1, img_size, img_size, 1)
    return [image_array_X,image_array_Y]

def create_name_pickle(categories,img_size):
    """[summary]
    Concats our name for the pickle that is going to be created
    Args:
        categories ([LIST]): [Our two folders we want to format]
        img_size ([INT]): [The size we want to make the image (example: 64 = 64x64)]
    """
    pickle_name = "F_{}&{}_S_{}_T_{}".format(categories[0],categories[1],img_size,int(time.time()))
    return pickle_name

def save_traning_data(name_pickle,image_arrays):
    """[summary]
    Saves our arrays in pickle format
    Args:
        name_pickle ([STR]): [The name of the pickle]
        image_arrays ([LIST]): [The arrays we want saved]
    """
    image_arrays_X = image_arrays[0]
    image_arrays_Y = image_arrays[1]
    name_pickleX = name_pickle+"X.pickle"
    pickle_out = open(DATAOUT / name_pickleX,"wb")
    pickle.dump(image_arrays_X, pickle_out)
    pickle_out.close()
    name_pickleY = name_pickle+"Y.pickle"
    pickle_out = open(DATAOUT / name_pickleY,"wb")
    pickle.dump(image_arrays_Y, pickle_out)
    pickle_out.close()

def create_folders():
    """[summary]
    Creates our folders
    """
    try:
        os.makedirs(SAVE_LOCATION_PATH)
    except:
        pass
    try:
        os.makedirs(DATAOUT)
    except:
        pass

def create_save_traning_data(categories,img_size):
    """[summary]
    Calls our functions to create the formatted image data in pickels
    This acts like a controller for all the other functions.
    Args:
        categories ([LIST]): [Our two folders we want to format]
        img_size ([INT]): [The size we want to make the image (example: 64 = 64x64)]
    """
    create_folders()
    shuffledata(CATEGORIES)
    data = create_training_data(categories,img_size)
    image_arrays = convert_traning_data(data,img_size)

    name_pickle = create_name_pickle(categories,img_size)
    save_traning_data(name_pickle,image_arrays)

#Run this method to get traning_data formatted and converted
create_save_traning_data(CATEGORIES,IMG_SIZE)