import os
import subprocess
import json

from modules.utils import create_directory, run_bash_command, delete_directory, get_random_string
from modules.core import update_profile, update_avatar, generate_vcf


# Importing configurations from "config.json"
config_file = 'config.json'

with open(config_file, 'r') as f:
    config_string = f.read()
config = json.loads(config_string)

remote_account = config["remote_account"]

# Importing the operations to be performed from the "operations.json" file
operations_file = 'operations/operations.json'

with open(operations_file, 'r') as f:
    operations_string = f.read()
operations = json.loads(operations_string)

repository_name = operations["repository"]

avatar_update = True if operations["update_avatar"] == "1" else False
vcf_generate = True if (operations.get('config').get('contact') is not None) \
                       and (operations.get('config').get('contact') != "") else False

# Creating temporary directory structure used for the updating operation
cwd = os.getcwd()
temp_dir = f'{cwd}/temp/'
create_directory(temp_dir)

random_string = get_random_string(10)
update_dir = f'{temp_dir}{repository_name}-{random_string}' 
create_directory(update_dir)

# Clone the remote git repository to update
remote_repo = f'{remote_account}{repository_name}'
clone_command = f'git clone {remote_repo} {update_dir}'
run_bash_command(clone_command)

updated = []

# Update profile _config file
update_profile(update_dir, operations)
updated.append("config")

# Update profile avatar
if avatar_update:
    update_avatar(update_dir, operations)
    updated.append("avatar")

if vcf_generate:
    generate_vcf(update_dir, operations)
    updated.append("vcard")

# Commit and push changes to remote repository
commit_message = f"updated: {updated}"
commit_command = f"cd {update_dir} && git add . && git commit -m '{commit_message}' && git push origin master"
subprocess.call(commit_command, shell=True)

delete_directory(update_dir)
