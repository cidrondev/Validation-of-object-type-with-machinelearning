"""[summary]
This handels all our UI
Author: Daniel Persson 2019-05-21
"""

def print_menu():
    """[summary]
    Prints our menu
    """
    print(
        "\nGet pictures from K-samsok options\n"+
        "Choose options below\n"+
        "1.Get pictures\n"+
        "2.Get random pictures\n"+
        "3.Download pictures from csv file\n"+
        "4.Delete removed picture information in csv file and delete corrupted jpeg image files\n"
        "5.Exit program"
        )

def print_download_start():
    """[summary]
    Prints that our download has started
    """
    print("\n Started downloading please wait... \n")

def print_download_complete():
    """[summary]
    Prints our download is complete
    """
    print("\n Download complete \n")

def print_remove_corrupt_files():
    """[summary]
    Prints we are removing corrupt files
    """
    print("\n Removing corrupt files... \n")

def input_gui_choice():
    """[summary]
    Prints to the user to input a choice
    """
    return int(input('Choose a choice:\n'))

def input_item_type():
    """[summary]
    Prints to the user to choose an itemType
    """
    return input('\nInput itemType "Objekt/föremål" or "Foto":')

def input_service_organization():
    """[summary]
    Prints to the user to choose an service org
    """
    return input('Choose service organizations comma seperated ("all"= Gets pictures from all orgs, "smha,gfm"= Gets picture from two orgs):')

def input_num_rand():
    """[summary]
    Prints to the user to choose how many pictures they want from the random query
    """
    return int(input('\nHow many pictures do you want? (requesting 1 picture does not work):'))

def input_num_order():
    """[summary]
    Prints to the user to choose how many pictures they want from the order query
    """
    return int(input('\nHow many pictures do you want? (requesting 1 picture does not work, max 500 pictures):'))

def input_req_pic():
    """[summary]
    Prints to the user choose how many times the want to multiply the order pictures
    """
    return int(input('\nHow many times do you want to muliply the pictures?:'))

def input_folder():
    """[summary]
    Tells the user to choose a folder were a csv file is locacted
    """
    return input('\nChoose a folder were csv file "image_data.csv" is located:')