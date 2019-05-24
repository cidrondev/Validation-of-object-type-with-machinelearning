import tensorflow as  tf
from pathlib import Path
import validaton_retrain
import cv2
import os

"""[summary]
Use to manually predict a photos
Author: Petter Gullin 2019-05-10 
Update: Daniel Persson 2019-05-23 
Fixed filepaths
Comments based on before comments 
Added retrain model validation
"""

FOLDER_PICTURES_LOCATED = "FOLDER_NAME"
MODEL_NAME = "MODEL_NAME"
#What type we want to validate against as google models give two result for either label
TYPE_IN = "object or photo"
FILE_NAME = 'FILENAME'

CATEGORIES = ["Photograph","Object","Error"]
MODEL_DIRECTORY = Path.cwd().parent / 'tensorflowdata' / 'tensorflowmodels'
PICTURE_DIRECTORY = Path.cwd().parent / 'trainingdata' / 'trainingdata_images'
FILE_LIST = os.listdir(PICTURE_DIRECTORY / FOLDER_PICTURES_LOCATED)

def prepare(filepath):
    """[summary]
    This method prepares our image before prediction on the .model files
    Args:
        filepath ([PATH]): [The filepath to the image]
    """
    IMG_SIZE = 64
    img_array = cv2.imread(str(filepath), cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

def sort_prediction_retrain(results,type_in):
    """[summary]
    Converts our google model result to int
    Args:
        results ([FLOAT]): [The value from the google model]
        type_in ([STR]): [What program is looking for]
    """
    if type_in == "object":
      result = results[1]
    else:
      result = results[0]
    if result < 0.5:
      result = 1
    else:
      result = 0
    return result

def load_model():
    """[summary]
    Checks what model it is and loads returns them loaded in to the program
    """
    model_type = MODEL_NAME.split(".")
    if(model_type[1] == "model"):
        return tf.keras.models.load_model(MODEL_DIRECTORY / MODEL_NAME)
    else:
        return validaton_retrain.load_graph(MODEL_DIRECTORY / MODEL_NAME)

def predict_model(model,filename):
    """[summary]
    This method make the predictions and returns it
    Args:
        model ([LOADED MODEL]): [The model we loaded in]
        filename ([STR]): [The name of the file we want to predict]
    """
    filepath = PICTURE_DIRECTORY/ FOLDER_PICTURES_LOCATED / filename
    prediction = 2
    model_type = MODEL_NAME.split(".")
    if(model_type[1] == "model"):
        prediction = model.predict([prepare(filepath)])
        return int(prediction[0][0])
    else:
        prediction = validaton_retrain.result(str(filepath),model)
        return sort_prediction_retrain(prediction,TYPE_IN)
            
# Prediction of single Photo
def single_pred(filename):
    """[summary]
    This predict a singel image
    Args:
        filename ([STR]): [The image we want to predict]
    """
    print("Single photo prediction of: ")
    print(1,":"+FILE_NAME + " = " + CATEGORIES[predict_model(load_model(),filename)])

# Prediction for multiple Photos in file_list:
def multi_pred(file_list):
    """[summary]
    Predicts multipel images
    Args:
        file_list ([LIST]): [All the images in the folder we want to predict]
    """
    print("Prediction of multiple photos:")
    count = 0
    for filename in file_list:
        count +=1
        print(count,":",FILE_NAME + " = " + CATEGORIES[predict_model(load_model(),filename)])

#These commands start the program
single_pred(FILE_NAME)
multi_pred(FILE_LIST)

