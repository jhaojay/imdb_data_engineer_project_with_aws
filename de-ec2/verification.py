#!/usr/bin/env python
import csv
import os
import subprocess
import sys

class file_verification:
    def __init__(self, file_path):
        """check whether it's a csv file"""
        if file_path.lower().endswith(".csv"):
            self.file = file_path
        else:
            print("Please supply a csv file")

    def check_not_empty(self):
        """return true if file exists and is not empty"""
        file_exists = os.path.exists(self.file)
        if file_exists:
            with open(self.file) as csv_file:
                reader = csv.DictReader(csv_file)
                csv_dict = [row for row in reader]
                if len(csv_dict):
                    return True
        print("File doesn't exist or is empty")
        return False

    def check_header(self, headers_to_check):
        """supply headers_to_check in list format
        return true if the headers are complete"""
        with open(self.file) as csv_file:
            reader = csv.reader(csv_file)
            csv_headers = sorted(next(reader))  # using next() to get headers
            if csv_headers == sorted(headers_to_check):
                return True
            else:
                print("Headers don't match.")
                return False

    def check_UTF8(self):
        """return true is the file is likely to be UTF8 encoded"""
        command = r"file {0}".format(self.file)
        stdout = subprocess.check_output(["file", self.file]).decode("utf-8")
        if "ASCII" in stdout or "UTF-8" in stdout:  # ASCII is a subset of UTF8
            return True
        else:
            print("File is not UTF8 encoded")
            return False

def verify_folder(folder_path):
    """check whether 3 files exist and all other file_verification attributes"""
    type_A_h = ['id', 'imdb_movie_id', 'title', 'release_year', 'certificate', 'run_time_min', 'imdb_rating', 'metascore', 'description', 'num_voted_users', 'gross']
    type_B_h = ['movie_id', 'person_id']
    type_C_h = ['id', 'imdb_person_id', 'full_name']

    # check whether all files are present
    files_in_folder = []
    for root, dirs, files in os.walk(folder_path):
        for file_ in files:
            files_in_folder.append(root + '/' + file_)

    if len(files_in_folder) != 3:
        print("The number of files is {}, 3 are required".format(len(files_in_folder)))
        return False

    files_in_folder.sort()
    if "type_A.csv" in files_in_folder[0] and \
            "type_B.csv" in files_in_folder[1] and \
            "type_C.csv" in files_in_folder[2]:
                pass
    else:
        print("not all files are present")
        return False

    
    # check whether each file for emptiness and UTF8
    for file_ in files_in_folder:
        veri = file_verification(file_)
        if veri.check_not_empty() and veri.check_UTF8():
            pass
        else:
            return False

    # compare headers
    if file_verification(files_in_folder[0]).check_header(type_A_h) and \
            file_verification(files_in_folder[1]).check_header(type_B_h) and \
            file_verification(files_in_folder[2]).check_header(type_C_h):
                return True
    else:
        return False


