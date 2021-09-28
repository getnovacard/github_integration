from github import Github
import os, subprocess, json, shutil, base64


def create_directory(dir):
    check_dir = os.path.isdir(dir)

    if not check_dir:
        os.makedirs(dir)
        print("created folder : ", dir)

    else:
        print(dir, "folder already exists.")


def run_bash_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    output, error = process.communicate()
    print(output)


def read_json(input_file):
    with open(input_file) as json_file:
        data = json.load(json_file)

        return data


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


# Generate a random string that will be used for generating temporary directories
def get_random_string(length):
    import random
    import string

    source = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(source) for i in range(8)))
    
    return result_str


def convert_file_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    
    return encoded_string.decode('utf-8')


"""
def init_github():   
    github_token = os.environ['GITHUB_TOKEN']
    return Github(github_token)
"""


# Replace a line inside the config file
def update_profile(update_dir, config_operations_dict, generate_vcf, contact):
    # Update profile _config.yml file
    input_file = update_dir + "/_config.yml"
    output_file = update_dir + "/config.yml_TEMP"

    f1 = open(input_file, "r")
    f2 = open(output_file, "w")
    updated = []

    for line in f1:
        line_key = line.split(":", 1)[0]

        if line_key in config_operations_dict.keys():
            updated.append(line_key)
            f2.write(line_key + ": " + config_operations_dict[line_key] + "\n")
        else:
            f2.write(line)

    f1.close()
    f2.close()        

    if os.path.exists(input_file):
        os.remove(input_file)
    else:
        print("The file does not exist")

    if os.path.exists(output_file):
        os.rename(output_file, input_file)
    else:
        print("The file does not exist")

    # Update avatar image if needed
    if avatar_update == True:
        empty_directory(update_dir + "/assets/images/avatar")
        
        filename = config_operations_dict["avatar"]
        source = os.getcwd() + "/operations/" + filename 
        target = update_dir + "/assets/images/avatar/" + filename
        shutil.copyfile(source, target)

    # Update vcard if needed
    if generate_vcf == True:
        empty_directory(update_dir + "/assets/vcard")
        social_profiles = [
            "contact-facebook_url", 
            "contact-linkedin_url", 
            "contact-instagram_url", 
            "contact-pinterest_url", 
            "contact-twitter_url", 
            "contact-youtube_url", 
            "contact-snapchat_url", 
            "contact-whatsapp_url", 
            "contact-tiktok_url", 
            "contact-telegram_url", 
            "contact-skype_url", 
            "contact-github_url", 
            "contact-gitlab_url"
            ]

        vcf_file = update_dir + "/assets/vcard/vcard.vcf"
        f_vcf = open(vcf_file, "w")

        line = "BEGIN:VCARD\n" 
        f_vcf.write(line)
        f2.close()

        line = "VERSION:3.0\n" 
        f_vcf.write(line)
        
        first_name = contact["contact-first_name"]
        last_name = contact["contact-last_name"]
        line = "N:" + last_name + ";" + first_name + ";;;\n" 
        f_vcf.write(line)
        line = "FN:" + first_name + " " + last_name + "\n" 
        f_vcf.write(line)

        avatar_dir = update_dir + "/assets/images/avatar"
        avatar_file = avatar_dir + "/" + config_operations_dict["avatar"]
        if len(os.listdir()) > 0:
            avatar_base64 = convert_file_to_base64(avatar_file)

            line = "PHOTO;ENCODING=b;TYPE=JPEG:" + avatar_base64 + "\n"
            f_vcf.write(line)


        if contact["contact-title"] != "":
            line = "TITLE:" + contact["contact-title"] + "\n"
            f_vcf.write(line)

        if contact["contact-company"] != "":
            line = "ORG:" + contact["contact-company"] + ";\n"
            f_vcf.write(line)

        if contact["contact-email"] != "":
            line = "EMAIL;type=INTERNET;type=HOME;type=pref:" + contact["contact-email"] + "\n"
            f_vcf.write(line)

        if contact["contact-phone"] != "":
            line = "TEL;type=CELL;type=VOICE;type=pref:" + contact["contact-phone"] + "\n"
            f_vcf.write(line)

        if contact["contact-website"] != "":
            line = "item1.URL;type=pref:" + contact["contact-website"] + "\n"
            f_vcf.write(line)
            line = "item1.X-ABLabel:_$!<HomePage>!$_\n"
            f_vcf.write(line)

        for c_key, c_value in contact.items():
            if c_key in social_profiles:
                social_profile = c_key.split("-")[1].split("_")[0]
                line = "X-SOCIALPROFILE;type=" + social_profile + ":" + c_value + "\n"
                f_vcf.write(line)

        line = "END:VCARD" 
        f_vcf.write(line)

        f2.close()

        updated.append("vcard")

    return ", ".join(updated)  




# Importing the operations to be performed from the "operations.json" file
for o_id, o_info in read_json("operations/operations.json").items():
    operation_id = o_id

    config = {}
    contact = {}
    for key in o_info:
        if key == "config":
            for c_key, c_value in o_info[key].items():
                if c_value != "":
                    config.update({c_key: c_value})
                    if "contact-" in c_key:
                        contact.update({c_key: c_value})

        elif key == "repository":
            repository_name = o_info[key]
        elif key == "generate_vcf":
            if o_info[key] == "0":
                generate_vcf = False
            elif o_info[key] == "1":
                generate_vcf = True
            else:
                raise ValueError('Illegal value assigned to "generate_vcf". The value for the "generate_vcf" field can be either 0 (False) or 1 (True).')
        elif key == "avatar_update":
            if o_info[key] == "0":
                avatar_update = False
            elif o_info[key] == "1":
                avatar_update = True
            else:
                raise ValueError('Illegal value assigned to "avatar_update". The value for the "generate_vcf" field can be either 0 (False) or 1 (True).')


    # Creating temporary directory structure used for the updating operation
    cwd = os.getcwd()
    create_directory(cwd + "/temp")

    random_string = get_random_string(10)
    update_dir = cwd + "/temp/" + repository_name + "-" + random_string 
    create_directory(update_dir)

    github_repo = "https://github.com/getnovacard/" + repository_name
    clone_command = "git clone " + github_repo + " " + update_dir
    run_bash_command(clone_command)

    updated = update_profile(update_dir, config, generate_vcf, contact)

    #g = init_github()

    #for repo in g.get_user().get_repos():
    #    print(repo.name)
    #    repo.edit(has_wiki=False)

    commit_message = f"updated: {updated}"
    commit_command = f"cd {update_dir} && git add . && git commit -m '{commit_message}' && git push origin master"
    subprocess.call(commit_command, shell=True)

    delete_directory(update_dir)
