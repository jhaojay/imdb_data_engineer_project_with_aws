import csv
import datetime
import os
import shutil
import get_data_from_db


def generate_type_A():
    headers, db_data = get_data_from_db.get_movie_info()
    raw_data_chunk = []
    temp_raw_data = []
    count = 1
    for row in db_data:

        temp_raw_data.append(row)
        if count % int(len(db_data)/20) == 0:
            raw_data_chunk.append(temp_raw_data)
            temp_raw_data = []
        count += 1

    cur_dt = datetime.datetime.now()
    for i in range(len(raw_data_chunk)):
        cur_dt = cur_dt + datetime.timedelta(0,10*60)
        folder_name = cur_dt.strftime("%d%H%M")

        file_name = f"{target_dir}\\{folder_name}\\{folder_name}" + "_type_A.csv"
        with open(file_name, "w", newline="", encoding="utf-8") as read_into_csv:
            writer = csv.writer(read_into_csv)
            writer.writerow(headers)
            writer.writerows(raw_data_chunk[i])

def generate_type_BC():
    headers_B, db_data_B = get_data_from_db.get_movie_director()
    headers_C, db_data_C = get_data_from_db.get_person()

    cur_dt = datetime.datetime.now()
    for i in range(20):
        cur_dt = cur_dt + datetime.timedelta(0,10*60)
        folder_name = cur_dt.strftime("%d%H%M")

        file_name = f"{target_dir}\\{folder_name}\\{folder_name}" + "_type_B.csv"
        with open(file_name, "w", newline="", encoding="utf-8") as read_into_csv:
            writer = csv.writer(read_into_csv)
            writer.writerow(headers_B)
            writer.writerows(db_data_B)

        file_name = f"{target_dir}\\{folder_name}\\{folder_name}" + "_type_C.csv"
        with open(file_name, "w", newline="", encoding="utf-8") as read_into_csv:
            writer = csv.writer(read_into_csv)
            writer.writerow(headers_C)
            writer.writerows(db_data_C)

cur_dt = datetime.datetime.now()
cwd = os.getcwd()
target_dir = cwd + "\imdb_raw_data"

if os.path.exists(target_dir):
    try:
        shutil.rmtree(target_dir)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

if not os.path.exists(target_dir):
    os.mkdir("imdb_raw_data")

for i in range(20):
    cur_dt = cur_dt + datetime.timedelta(0,10*60) # increments for 10 mins
    folder_name = cur_dt.strftime("%d%H%M")

    os.mkdir(f"{target_dir}\\{folder_name}")

generate_type_A()
generate_type_BC()