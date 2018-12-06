import os
import sys
import datetime

def file_name(file_dir):
# Read files under folder
    files_full_path = []
    files_name = []
    files_folder_path = []
    for root ,_, files_name in os.walk(file_dir):
        for file in files_name:
            if os.path.splitext(file)[1] == '.jpg':
                files_full_path.append(os.path.join(root,file))
        files_folder_path.append(root)
    files_folder_path.remove(files_folder_path[0])
    files_full_path.sort()
    files_name.sort()
    files_folder_path.sort()
    return files_full_path,files_folder_path,files_name

def type_file_name(file_dir,type):
# Read files under folder
    files_full_path = []
    files_name = []
    files_folder_path = []
    for root ,_, files_name in os.walk(file_dir):
        for file in files_name:
            if os.path.splitext(file)[1] == type:
                files_full_path.append(os.path.join(root,file))
        files_folder_path.append(root)
    files_folder_path.remove(files_folder_path[0])
    files_full_path.sort()
    files_name.sort()
    files_folder_path.sort()
    return files_full_path,files_folder_path,files_name

def list_dir(dir):
    path = os.listdir(dir)
    return path

# def create_folder(root, folder_name):
#     #root Current root directory
#     #folder To create directory names
#     #return Path to create files root+folder_name
#     if not os.path.exists(root):
#         print ('root path not exist...')
#         sys.exit()
#     if not os.path.exists(folder_name):
#         os.mkdir(root+'/'+folder_name)
#         print ('create ')
#         print (root+'/'+folder_name)
#         print ('...')
#         print ('\n')
#     else:
#         print ('folder_name exist...')
#     return root + '/' + folder_name
def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print ('create ')
        print (path)
        print (' ...')
        print ('\n')
    else:
        print ('folder_name exist...')
def get_system_time_to_string():
    now_time = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S')
    return now_time
