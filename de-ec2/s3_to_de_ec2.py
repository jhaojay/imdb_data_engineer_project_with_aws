#!/usr/bin/env python
import datetime
import os
import re
import subprocess

def get_new_folder_name(bkt_path):
    """get the name of the new folder that is about to process"""
    cur_dt = datetime.datetime.now()
    vague_folder_name = cur_dt.strftime("%d%H%M")
    vague_folder_name = str(int(int(vague_folder_name)/10))

    command = "aws s3 ls {0}".format(bkt_path)
    print(command)
    command = command.split()
    file_list_raw = subprocess.check_output(command).decode("utf-8")
    file_list = re.findall("[0-9]+", file_list_raw)

    folder_name = ""
    for fl in file_list:
        if vague_folder_name in fl:
            folder_name = fl.strip()

    return folder_name

def sync_s3_folder_to_local(raw_data_bkt_folder_path, to_folder):
    """downloading all files inside the folder of S3 to files_to_be_processed"""
    command = "aws s3 sync {0} {1}".format(raw_data_bkt_folder_path, to_folder)
    os.system(command)

