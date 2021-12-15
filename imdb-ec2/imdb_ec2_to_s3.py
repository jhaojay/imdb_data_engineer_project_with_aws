#!/usr/bin/env python
import datetime
import os

if __name__ == "__main__":
    cur_dt = datetime.datetime.now()
    vague_folder_name = cur_dt.strftime("%d%H%M")
    vague_folder_name = str(int(int(vague_folder_name)/10))


    source_dir = "/home/ec2-user/imdb_raw_data"
    folder_name = ""
    for root, dirs, files in os.walk(source_dir):
        for dir_ in dirs:
            if vague_folder_name in dir_:
                folder_name = dir_
                break

    if(folder_name):
        command = "aws s3 sync {0}/{1}/ s3://imdb-bkt/imdb_raw_data/{1}".format(source_dir, folder_name)
        print(os.system(command))

