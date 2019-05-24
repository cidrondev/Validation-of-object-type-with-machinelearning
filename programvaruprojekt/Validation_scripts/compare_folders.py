import os
from pathlib import Path

"""[summary]
A simple program thats prints out the number of same images in two folders
Author: Daniel Persson 2019-05-23
"""

folder1 = "FOLDER_NAME_1"
folder2 = "FOLDER_NAME_2"

filepath1 = Path.cwd().parent / 'results' / folder1
filepath2 = Path.cwd().parent / 'results' / folder2

list1 = os.listdir(filepath1)
list2 = os.listdir(filepath2)

print("\nComparings folders")
count = 0
for item in list1:
    if item not in list2:
        print(item)
        count +=1
#Minus one for the validation.csv file
print("Photos in both folders:",count-1)

