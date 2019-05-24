from django.template.defaultfilters import slugify
from datetime import datetime
from pathlib import Path
import get_validation_info
import validaton_retrain
import tensorflow as tf
import urllib.request
import cv2
import csv
import os

"""[summary]
This program validates against k-samsok API and download every picture that is wrongfully validated.
It also creates a csv file with picture data. You can use both pb and model files.
Author: Petter Gullin 2019-05-10
Update: Daniel Persson 2019-05-23
Fixed filepaths
Comments based on before comments 
Added retrain model validation
"""

# Choose from one or more of the following institutions (keyword "all" gives every instituion):
""" s-vlm,kbg,enk,smvk-mm,shm,hallwylska museet,aero,vgm,osmu,smvk-om,smm-mm,bhm,socken,lsh,vm,nomu,
jm,Kortnamn,arkm,blm,skoklosters slott,pm,s-tek,s-hm,rsms,shfa,jlm,slm,mili,imvg,heo,smm-sm,mm,s-fv,
tum,s-om,soc,livrustkammaren,smm-vm,smvk-em,kulturen,jfl,vax,gnm,hem,vbg,tes,upmu,smha,gfm,dramawebben,
smvk-vkm,sm,sk,dfh,litografiska,s-xlm,raä,arme,ajtte,wws,ablm,fmb,s-fbm,gsm,s-olm
"""
INSTITUTION = "all"
# Choose "foto" or "objekt/föremål"
ITEM_TYPE = "foto"
# The modelname you want to use
MODEL_NAME = "MODEL_NAME"
#The two categories for that we validate from
CATEGORIES = ["Photograph", "Object"]

MODEL_DIRECTORY = Path.cwd().parent / 'tensorflowdata' / 'tensorflowmodels'
RESULT_DIRECTORY = Path.cwd().parent / 'results'

def prepare(filepath):
    """[summary]
    This method prepares our image before prediction on the .model files
    Args:
        filepath ([PATH]): [The filepath to the image]
    """
    IMG_SIZE = 64
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

def url_to_image(url):
    """[summary]
    This method gets a temporary picture name tmp.jpeg for validation
    Args:
        url ([LINK]): [The link to the images we want to download]
    """
    try:
        urllib.request.urlretrieve(url, "tmp.jpeg")
    except:
        print("Error something went wrong")

def itemId_get_num(itemId_link):
    """[summary]
    Gets the itemId numbers from the full link that K-samsok gets
    Args:
        itemId_link ([String]): [The full itemId link from k-samsok]
    """
    itemId_num = itemId_link.split("/")
    return itemId_num.pop()

def save_image(path, url, item_id):
    """[summary]
    This method prepares our image before prediction on the .model files
    Args:
        path ([PATH]): [The path were want to save the image]
        url ([LINK]): [The link to the images we want to download]
        item_id ([STR]): [The item_id of the picture]
    """
    filename = slugify(itemId_get_num(item_id))+ ".jpeg"
    filepath = path / filename
    try:
        urllib.request.urlretrieve(url, filepath)
    except:
        print("Error something went wrong")

def create_csvfile(path, data):
    """[summary]
    Creates a csv file
    Args:
       path ([STR]): [The path we want to save the csv file]
       data ([DICT]): [The data we want to input to the csv file]
    """
    filepath = path / "validation_data.csv"
    with open(filepath, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)
        csvFile.close()

def service_org_list(service_organizations):
    """[summary]
    Takes all our inputed orgs and splits them into a list
    Args:
        service_organization ([STR]): [The org we want pictures from]
    """
    if(service_organizations == "all"):
        service_organizations ='s-vlm,kbg,enk,smvk-mm,shm,hallwylska museet,aero,vgm,osmu,smvk-om,smm-mm,bhm,socken,lsh,vm,nomu,jm,Kortnamn,arkm,blm,skoklosters slott,pm,s-tek,s-hm,rsms,shfa,jlm,slm,mili,imvg,heo,smm-sm,mm,s-fv,tum,s-om,soc,livrustkammaren,smm-vm,smvk-em,kulturen,jfl,vax,gnm,hem,vbg,tes,upmu,smha,gfm,dramawebben,smvk-vkm,sm,sk,dfh,litografiska,s-xlm,raä,arme,ajtte,wws,ablm,fmb,s-fbm,gsm,s-olm'
        return service_organizations.split(',')
    else:
        return service_organizations.split(',')

def sort_prediction_retrain(results,type_in):
    """[summary]
    Converts our google model result to int
    Args:
        results ([FLOAT]): [The value from the google model]
        type_in ([STR]): [What program is looking for]
    """
    if type_in == "objekt/föremål":
      result = results[1]
    else:
      result = results[0]
    if result < 0.5:
      result = 1
    else:
      result = 0
    return result

def kind_of_type(type_in):
    """[summary]
    Selects the kind of type we have choosen and converts it to the query language
    Args:
       type_in ([STR]): [The type we want for the query]
    """
    if type_in == "objekt/föremål":
        return "Föremål"
    elif type_in == "foto":
        return "Foto"
    else:
        return type_in

def create_model_name(model_in,inst,the_type):
    """[summary]
    Creates our model name
    Args:
       model_in ([STR]):[The name of the model]
       inst ([STR]): [The name of the instution]
       type_in ([STR]): [The type we want for the query]
    """
    modelname = model_in.split(".")
    time = datetime.now().strftime(r"%Y%m%d_%H%M%S")
    full_modelname = F"{time}_{the_type}_{inst}_{modelname[0]}"
    return full_modelname,modelname[1]

def create_folders(path):
    """[summary]
    Creates our folders
    Args:
       oath ([PATH]): [A path were want to create a folder at]
    """
    try:
        os.makedirs(MODEL_DIRECTORY)
    except:
        pass
    try:
        os.makedirs(RESULT_DIRECTORY)
    except:
        pass
    try:
        os.makedirs(path)
    except:
        pass

def save_data(path,image_data,csv_data):
    """[summary]
    Downloads a picture and inputs the data from the query into the csv file
    Args:
       path ([PATH]): [The path were we want to save the csv file and the pictures]
       image_data ([DIC]): [The imagedata of the image]
       csv_data ([LIST]): [The list we want in our csv file]
    """
    save_image(path, image_data["thumbnail"],image_data["itemId"])
    tempdata = [image_data["itemId"], image_data["thumbnail"], image_data["kringlaLink"]]
    csv_data.append(tempdata)

def validate_item(inst, type_in, model_in):
    """[summary]
    Validates our items and every wrong validate item it saves.
    This is like the main method of the valdiation_app.
    Args:
       inst ([STR]): [The name of the instution]
       type_in ([STR]): [The type we want for the query]
       model_in ([STR]):[The name of the model]
    """
    for org in service_org_list(inst):
        the_type = kind_of_type(type_in)
        name,model_type = create_model_name(model_in,inst,the_type)
        
        if(model_type == "model"):
            model = tf.keras.models.load_model(MODEL_DIRECTORY / model_in)
        else:
            model = validaton_retrain.load_graph(MODEL_DIRECTORY / model_in)
        
        path = RESULT_DIRECTORY / name
        create_folders(path)

        count = 1
        errorCount = 1
        csv_data = [['itemId', 'thumbnail', 'kringlaLink']]
        for image_data in get_validation_info.ksamsok_info(type_in, org):
            url_to_image(image_data["thumbnail"])
            if(model_type == "model"):
                prediction = model.predict([prepare("tmp.jpeg")])
                prediction_final = int(prediction[0][0])
            else:
                prediction = validaton_retrain.result("tmp.jpeg",model)
                prediction_final = sort_prediction_retrain(prediction,type_in)
            if CATEGORIES[prediction_final] != type:
                print(count,errorCount,CATEGORIES[prediction_final], image_data["kringlaLink"])
                save_data(path,image_data,csv_data)
                errorCount += 1
            count += 1
        if os.path.exists("tmp.jpeg"):
            os.remove("tmp.jpeg")
        print("\nantal funna felaktigheter: ",errorCount - 1)
        create_csvfile(path, csv_data)

#Run this method to validate
validate_item(INSTITUTION,ITEM_TYPE,MODEL_NAME)
    
