import sys
import file_handler
import ksamsok_info
import ui

"""[summary]
This builds our menu and functionallity
Author:Daniel Persson 2019-05-21
"""

GUI_choice = 0

def get_pics(choice):
    """[summary]
    Builds our get picture program
    Args:
        choice ([STR]): [The sort of picture getting the user have choosen]
    """
    item_type = ui.input_item_type()
    service_organizations = ui.input_service_organization()
    path_csv,path_image = file_handler.create_folders()
    
    if(choice == "in_order"):
        num_pic = ui.input_num_order()
        req_pic = ui.input_req_pic()
        list_result = list(ksamsok_info.ksamsok_pics(num_pic,req_pic,item_type,service_organizations))
    elif(choice == "in_random"):
        num_pic = ui.input_num_rand()
        list_result = list(ksamsok_info.random_ksamsok_pics(num_pic,item_type,service_organizations))

    ui.print_download_start
    file_handler.save_all_files(list_result,path_image)
    file_handler.csvfile_from_dict(list_result,path_csv)
    ui.print_download_complete()

while GUI_choice != 5:
    ui.print_menu()
    GUI_choice = ui.input_gui_choice()
    if GUI_choice == 1:
        get_pics("in_order")

    elif GUI_choice == 2:
        get_pics("in_random")

    elif GUI_choice == 3:
        csv_folder = ui.input_folder()
        ui.print_download_start
        file_handler.downloaded_from_csv(csv_folder)
        ui.print_download_complete()

    elif GUI_choice == 4:
        csv_folder = ui.input_folder()
        ui.print_remove_corrupt_files
        file_handler.remove_corrupt_files(csv_folder)
        file_handler.remove_data_csv(csv_folder)

    elif GUI_choice == 5:
        sys.exit()