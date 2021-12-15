# Introduction


# Project Overview Diagram


# Code Flowcharts


# Dependency
Python 3.7.10 was used for this project, and the following non-standard libraries were used:
```
pyarrow==6.0.1, pandas==1.3.5
```
Use the following command to install the dependencies
```python
$ pip install -r requirements.txt
```
# Preparation of Raw Data
The imdb data were scrapped and stored in PostgreSQL using programs from my other project: [imdb_top50_by_genre](https://github.com/jhaojay/imdb_top50_by_genre/).
```python
$ python3 prepare_files.py
```
The folder "imdb_raw_data" will be generated, and it has the following structure:
```
imdb_raw_data
│   ├── 202112141930
│   │   ├── 202112141930_type_A.csv
│   │   ├── 202112141930_type_B.csv
│   │   └── 202112141930_type_C.csv
│   ├── 202112141940
│   │   ├── 202112141940_type_A.csv
│   │   ├── 202112141940_type_B.csv
│   │   └── 202112141940_type_C.csv
│   ├── 202112141950
│   │   ├── 202112141950_type_A.csv
│   │   ├── 202112141950_type_B.csv
│   │   └── 202112141950_type_C.csv
```
# Usage
(Note: Assuming the reader has the knowledge of AWS's EC2 and S3, only brief instructions are given here.)

1. Launch two instances, named imdb-ec2 and de-ec2, and create two buckets, named imdb-bkt and de-bkt.
<br /><br />
2. Grant imdb-ec2 access to imdb-bkt, and grant de-ec2 access to both de-bkt and imdb-bkt.
<br /><br />
3. Use scp command to copy scripts to the corresponding EC2:
```
$ sudo scp -i <key.pem> <from_local_dir> <to_ec2_dir>
```
<br /><br />
4. In the imdb-ec2, modify the crontab file:
```
$ crontab -e
```
and add the following task:
```python
*/10 * * * * <path to imdb_ec2_to_s3.py>
```
The EC2 will upload raw data at every 10th minute.

<br /><br />
5. In the de-ec2, add the following task to the crontab file:
```python
*/10 * * * * sleep 61; <path to main.py>
```
The EC2 will wait for 60 seconds after raw data are uploaded to imdb-bkt then start processing data.
