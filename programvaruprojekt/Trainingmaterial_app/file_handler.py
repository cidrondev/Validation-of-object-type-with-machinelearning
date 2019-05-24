import os
import re
import csv
import time
import requests
import datetime
import urllib.request
from PIL import Image
from tqdm import tqdm
from pathlib import Path
from django.template.defaultfilters import slugify


"""[summary]
This handels everything with files
Author: Petter Gullin & Daniel Persson 2019-05-21
"""
#Path we want files saved in
SAVE_PATH = Path.cwd().parent / 'trainingdata'
PATH_IMG = SAVE_PATH / "trainingdata_images"
PATH_CSV = SAVE_PATH / "trainingdata_csv"


def create_folders():
    """[summary]
    Creates folders for csv and images to save files in
    """
    time = datetime.datetime.now().strftime(r"%Y%m%d_%H%M%S")
    # Name on our main csv folder
    path_csv = PATH_CSV / time
    try:
        os.makedirs(path_csv)
    except:
        pass
    # Name on our main image folder 
    path_image = PATH_IMG / time
    try:
        os.makedirs(path_image)
    except:
        pass
    return path_csv,path_image

def remove_corrupt_files(image_folder):
    """[summary]
    https://opensource.com/article/17/2/python-tricks-artists
    Args:
        path_image ([type]): [description]
    """
    path_image = PATH_IMG / image_folder
    for filename in os.listdir(path_image):
            try:
                img = Image.open(path_image / filename)
                img.verify()
            except (IOError, SyntaxError):
                os.remove(path_image+filename)
                print('Removed corrupt file:',filename)

def save_all_files(items_dict,path_file):
    """[summary]
    Loop throught the whole dictonary and saves every file from an url (thumbnail in this case)
    Args:
        items_dict ([DICT]): [All our items from K-samsok]
        path_file ([STR]): [The path were to save the file]
    """
    #tqdm here to show progressbar
    for record in tqdm(items_dict):
        itemId_link = itemId_get_num(record.get("itemId"))
        save_file(record.get("thumbnail"),itemId_link,path_file)

def itemId_get_num(itemId_link):
    """[summary]
    Gets the itemId numbers from the full link that K-samsok gets
    Args:
        itemId_link ([String]): [The full itemId link from k-samsok]
    """
    itemId_num = itemId_link.split("/")
    return itemId_num.pop()

def list_data_csvfile(csv_folder_name):
    """[summary]
    Downloads images from a csvfile
    Args:
        csv_folder_name ([STR]): [The name of the folder where the csv file is located]
    """
    thumbnail_list = []
    #The path to the csv file
    csv_path_folder = PATH_CSV / csv_folder_name
    csv_path = csv_path_folder / "image_data.csv"
    with open (csv_path,mode="r") as csv_file:
        #Skips the header for our list
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            thumbnail_dict = {
                "itemId": row[0],
                "serviceOrganization":row[1],
                "thumbnail": row[2],
                "itemType": row[3],
                "kringlaLink": row[4]
            }
            thumbnail_list.append(thumbnail_dict)
        csv_file.close()
        return thumbnail_list
        

def downloaded_from_csv(csv_folder_name):
    """[summary]
    Download files from a csv file
    Args:
        csv_folder_name ([STR]): [Name of folder where csv is located]
    """
    #Name on our downloaded from csv folder
    folder_name = csv_folder_name+"-downloaded_from_csv"
    #Where we save the downloaded files
    path_file = PATH_IMG / folder_name
    #Create folder
    os.makedirs(path_file)
    save_all_files(list_data_csvfile(csv_folder_name),path_file)

def remove_data_csv(csv_folder_name):
    """[summary]
    Removes imagedata in csv file if it does not exists in folder
    Args:
        csv_folder_name ([STR]): [Name of the folder were the csv file is located]
    """
    csv_data = list_data_csvfile(csv_folder_name)
    #The path to the csv file
    csv_path = PATH_CSV / csv_folder_name
    image_path = PATH_IMG / csv_folder_name
    image_folder = os.listdir(image_path)
    csv_data_final = []
    for data in csv_data:
        itemId = slugify(itemId_get_num(data.get('itemId')))+".jpeg"
        if itemId in image_folder:
            csv_data_final.append(data)
        else:
            print("removed",data["itemId"])
    csvfile_from_dict(csv_data_final,csv_path)

def save_file(url,itemId,path):
    """[summary]
    Download a file to a specifed folder
    Args:
        url ([STR]): [Link to the file thats downloaded]
        itemId ([STR]): [Our itemId of the saved file]
        path ([STR]): [The path were want the file saved]
    """
    filename = slugify(itemId)+".jpeg"
    file_path = path / filename
    try:
        urllib.request.urlretrieve(url, file_path)
    except:
        print("Error: Host time out, download what I can\n")

def csvfile_from_dict(dict_data,path):
    """[summary]
    Create a csv file from the given dictonary
    Args:
        dict_data ([DICT]): [Our data from k-samsok]
        path ([STR]): [The path we want to save the csv file]
    """
    csv_columns = ["itemId","serviceOrganization","thumbnail","itemType","kringlaLink"]
    filename = path / "image_data.csv"
    if("image_data.csv" in os.listdir(path)):
        os.remove(filename)
    with open(filename, 'w',newline='',encoding='utf-8') as csvFile:
        writer = csv.DictWriter(csvFile,fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(dict_data)
        csvFile.close()