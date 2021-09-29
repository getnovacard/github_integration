import subprocess
import os
import shutil
import random
import string
import base64


def create_directory(directory):
    check_dir = os.path.isdir(directory)

    if not check_dir:
        os.makedirs(directory)
        print("created folder : ", directory)
    else:
        print(directory, "folder already exists.")


def run_bash_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    output, error = process.communicate()
    print(output)


def empty_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def delete_directory(directory_path):
    if os.path.exists(directory_path):
        if len(os.listdir(directory_path)) == 0:
            os.rmdir(directory_path)
        else:
            empty_directory(directory_path)
            os.rmdir(directory_path)
    else:
        print("Directory not found.")    


def get_random_string(length):
    source = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(source) for i in range(length)))
    
    return result_str


def convert_file_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    
    return encoded_string.decode('utf-8')
