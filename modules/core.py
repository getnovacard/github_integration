import os
import shutil

from .utils import empty_directory, convert_file_to_base64


# Replace a line inside the config file
def update_profile(update_dir, operations_dict):
    config_operations_dict = operations_dict["config"]

    original_file = f'{update_dir}/_config.yml'
    updated_file = f'{update_dir}/config.yml_TEMP'

    f1 = open(original_file, "r")
    f2 = open(updated_file, "w")

    for line in f1:
        line_key = line.split(":", 1)[0]

        if line_key in config_operations_dict.keys():
            f2.write(line_key + ": " + config_operations_dict[line_key] + "\n")
        elif line_key in config_operations_dict["contact"].keys():
            f2.write(line_key + ": " + config_operations_dict["contact"][line_key] + "\n")

    f1.close()
    f2.close()

    if os.path.exists(original_file):
        os.remove(original_file)
    else:
        print(f"The {original_file} file does not exist")

    if os.path.exists(updated_file):
        os.rename(updated_file, original_file)
    else:
        print(f"The {updated_file} file does not exist")


def update_avatar(update_dir, operations_dict):
    avatar_dir = f'{update_dir}/assets/images/avatar/'
    operations_dir = 'operations/'
    empty_directory(avatar_dir)

    new_avatar_filename = operations_dict["config"]["avatar"]
    new_avatar_extension = os.path.splitext(new_avatar_filename)[1]
    new_avatar_path = f'{operations_dir}{new_avatar_filename}'

    avatar_file = f'{avatar_dir}avatar{new_avatar_extension}'
    shutil.copyfile(new_avatar_path, avatar_file)


def generate_vcf(update_dir, operations_dict):
    # Read the _config.yml file of the profile into a dict
    profile_config_file = f'{update_dir}/_config.yml'
    config_lines = []
    contact = {}

    with open(profile_config_file, 'r') as f:
        for ln in f.readlines():
            line = ln.strip().split(":")
            line[1] = line[1].strip()
            config_lines.append(line)

    for element in config_lines:
        if "contact-" in element[0]:
            contact.update({element[0]: element[1]})

    # Delete existing vcards
    avatar_dir = f'{update_dir}/assets/images/avatar/'
    avatar_file = f'{avatar_dir}{operations_dict["config"]["avatar"]}'
    vcard_dir = f'{update_dir}/assets/vcard/'
    empty_directory(vcard_dir)

    # Define social profiles list to be used during the update procedure
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

    # Write to the new vcard file
    vcf_file = f'{vcard_dir}vcard.vcf'
    f_vcf = open(vcf_file, "w")

    line = "BEGIN:VCARD\n"
    f_vcf.write(line)

    line = "VERSION:3.0\n"
    f_vcf.write(line)

    first_name = contact["contact-first_name"]
    last_name = contact["contact-last_name"]
    line = "N:" + last_name + ";" + first_name + ";;;\n"
    f_vcf.write(line)
    line = "FN:" + first_name + " " + last_name + "\n"
    f_vcf.write(line)

    if len(os.listdir(avatar_dir)) > 0:
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
            if c_value != "":
                line = "X-SOCIALPROFILE;type=" + social_profile + ":" + c_value + "\n"
                f_vcf.write(line)

    line = "END:VCARD"
    f_vcf.write(line)
