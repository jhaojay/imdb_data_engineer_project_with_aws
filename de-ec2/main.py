#!/usr/bin/env python3

import os
import subprocess
import shutil
import s3_to_de_ec2
import verification
import merge_and_convert
import athena_partition


local_raw_data_path = "/home/ec2-user/raw_data/"
local_log_path = "/home/ec2-user/unprocessed.log"
local_clean_files_folder = "/home/ec2-user/clean_files/"
local_archive_folder = "/home/ec2-user/archive/"
local_partitioned_folder = "/home/ec2-user/partitioned/"

s3_imdb_bkt_path = "s3://imdb-bkt/imdb_raw_data/"
s3_unprocessed_log_path = "s3://de-bkt/unprocessed.log"
s3_clean_files_folder_path = "s3://de-bkt/clean_files/"
s3_archive_path = "s3://de-bkt/archive/"
s3_partitioned_folder = "s3://de-bkt/partitioned/"

def clean_folders():
    """ Remove local raw data folder, clean files folder, archive and unprocessed log """
    
    print("Removimg local log, raw data folder, clean file folder, and archive.")
    # clear local log first
    if os.path.exists(local_log_path):
        os.remove(local_log_path)

    # rm raw_data folder first
    if os.path.exists(local_raw_data_path):
        shutil.rmtree(local_raw_data_path)  # rm folder and its contents

    # rm clean files folder
    if os.path.exists(local_clean_files_folder):
        shutil.rmtree(local_clean_files_folder)  # rm folder and its contents
    
    # rm archive
    if os.path.exists(local_archive_folder):
        shutil.rmtree(local_archive_folder)  # rm folder and its contents

    # rm partitioned
    if os.path.exists(local_partitioned_folder):
        shutil.rmtree(local_partitioned_folder)

def get_raw_data_folder_names():
    """ Get data folder names that are ready to process. Return a list """
    raw_data_folder_name_list = []
    # get new raw data folder name
    new_raw_data_folder_name = s3_to_de_ec2.get_new_folder_name(s3_imdb_bkt_path)
    if new_raw_data_folder_name:
        raw_data_folder_name_list.append(new_raw_data_folder_name)

    # get old unprocessed raw data folder name from "unprocessed.log" in S3
    command = f"aws s3 cp {s3_unprocessed_log_path} {local_log_path}"
    os.system(command)
    #-- if log downloaded, open it and read folder names
    if os.path.exists(local_log_path):
        with open(local_log_path, 'r') as log_file:
            line_list = log_file.read().splitlines()
            for line in line_list:
                if line and (line not in raw_data_folder_name_list):  # to get rid of empty and same lines
                    raw_data_folder_name_list.append(line)
    
    return raw_data_folder_name_list


def download_folders_from_s3(raw_data_folder_name_list):
    """ Download folders from imdb-bkt based on given folder names """

    print("Trying to download the following folders:")
    raw_data_folder_name_list.sort(reverse=True)  # process newest folder first
    print(raw_data_folder_name_list)
    for raw_data_folder_name in raw_data_folder_name_list:
        print(f"Downloading {raw_data_folder_name}")
        to_local_folder = local_raw_data_path + raw_data_folder_name
        from_path = s3_imdb_bkt_path + raw_data_folder_name
        s3_to_de_ec2.sync_s3_folder_to_local(from_path, to_local_folder)

def process():
    """
    Verifying, merging, and converting folders in local raw data folder.
    Save files in clearn files folder and archive.
    Return processed list and unprocessed list.
    """
    # create clean files folder and archive for processing
    os.mkdir(local_clean_files_folder)
    os.mkdir(local_archive_folder)

    # get folder names in local raw data folder
    raw_data_folder_name_list = []
    for root, dirs, files in os.walk(local_raw_data_path):
        for dir_ in dirs:
            raw_data_folder_name_list.append(dir_)

    processed_data_folder_list = []
    temp_raw_data_folder_name_list = raw_data_folder_name_list[:]
    for raw_data_folder_name in raw_data_folder_name_list:
        folder_path = local_raw_data_path + raw_data_folder_name + '/'
        verified = verification.verify_folder(folder_path)
        if verified:
            type_A_file_path = folder_path + raw_data_folder_name + "_type_A.csv"
            type_B_file_path = folder_path + raw_data_folder_name + "_type_B.csv"
            type_C_file_path = folder_path + raw_data_folder_name + "_type_C.csv"
            clean_files_name = local_clean_files_folder + raw_data_folder_name + ".parquet"

            print(f"{raw_data_folder_name} verified. Now processing.")
            #--  process and save to clean files folder
            merge_and_convert.merge_and_convert_to_parquet(
                    type_A_file_path,
                    type_B_file_path,
                    type_C_file_path,
                    clean_files_name
            )
            #-- save to archive
            shutil.move(local_raw_data_path + raw_data_folder_name, local_archive_folder + raw_data_folder_name)

            processed_data_folder_list.append(raw_data_folder_name)
            temp_raw_data_folder_name_list.remove(raw_data_folder_name)
            print(f"Processing completed. {raw_data_folder_name}.parquet available.")
        else:
            print(f"{raw_data_folder_name} not verified. Ignored.")

    raw_data_folder_name_list = temp_raw_data_folder_name_list[:]

    return processed_data_folder_list, raw_data_folder_name_list

def cp_clean_files_to_partitioned(cln_files_dir, partitioned_dir):
    """ cp clean parquet files to partitioned folder """

    os.mkdir(partitioned_dir)

    file_dict = {} # store file name and file path with name
    for root, dirs, files in os.walk(cln_files_dir):
        for file_ in files:
            file_dict[file_] = root + file_

    print(f"Moving {len(file_dict)} files to partitioned folder.")

    for file_name, file_dir in file_dict.items():
        partitioned_file_dir = partitioned_dir + f"filetime={file_name.split('.')[0]}/"
        print(f"Moving {file_name} into {partitioned_file_dir}")
        os.mkdir(partitioned_file_dir)
        shutil.copyfile(file_dir, partitioned_file_dir+file_name)
        print("Done!")


def update_and_upload_log(raw_data_folder_name_list):
    """ Update the local unprocessed log file and upload it to de-bkt """
    # update unprocessed.log
    with open(local_log_path, 'w') as log_file:
        log_file.write('\n'.join(raw_data_folder_name_list))
    # upload unprocessed.log to de-bkt in S3
    os.system(f"aws s3 cp {local_log_path} {s3_unprocessed_log_path}")
    print("unprocessed.log updated")


def upload_clean_files_and_archive():
    """ Sync folders to de-bkt in S3 """
    # sync clearn files
    command = f"aws s3 sync {local_clean_files_folder} {s3_clean_files_folder_path}"   
    os.system(command)

    # sync archive
    command = f"aws s3 sync {local_archive_folder} {s3_archive_path}"
    os.system(command)

    # sync partitioned
    command = f"aws s3 sync {local_partitioned_folder} {s3_partitioned_folder}"
    os.system(command)
    
    print("Finished syncing clearn files, archive and partitioned to de-bkt in S3")


def partition(processed_list):
    """ use boto3 to partition parquet in S3 """

    partition_column_name = "filetime"
    for partition_value in processed_list:
        print(f"Partitioning {partition_value}.")
        file_s3_location = f"{s3_partitioned_folder}{partition_column_name}={partition_value}/"
        athena_partition.partition_parquet("filetime", partition_value, file_s3_location)


clean_folders()
folder_list = get_raw_data_folder_names()
download_folders_from_s3(folder_list)
processed_list, unprocessed_list = process()
update_and_upload_log(unprocessed_list)
cp_clean_files_to_partitioned(local_clean_files_folder, local_partitioned_folder)
upload_clean_files_and_archive()
clean_folders()
partition(processed_list)

