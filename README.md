# Introduction
In this project, I emulated an automated ETL processes with AWS's EC2 and S3 services. The client company sends 3 types of raw data files containing imdb movie info for every 10 minutes. A data engineering team retrieves the raw data files for every 10 minutes, verifies, merges, and converts the files into parquet format. If the raw data files are unable to be verified, they will be re-verified in the next processing cycle. After parquet files are ready, they will be uploaded to de-bkt for the data science team to analyze.

# Project Overview Diagram
![alt text](https://github.com/jhaojay/imdb_data_engineer_project_with_aws/blob/main/jpg/overview.JPG?raw=true)
imdb-bkt has the following directory structure:
```python
imdb-bkt
└── imdb_raw_data
	├── 202112141930
	│   ├── 202112141930_type_A.csv
	│   ├── 202112141930_type_B.csv
	│   └── 202112141930_type_C.csv
	├── 202112141940
	│   ├── 202112141940_type_A.csv
	│   ├── 202112141940_type_B.csv
	│   └── 202112141940_type_C.csv
	├── 202112141950
	│   ├── 202112141950_type_A.csv
	│   ├── 202112141950_type_B.csv
	│   └── 202112141950_type_C.csv
	└── …

```
<br /><br />
de-bkt has the following directory structure:
```python
de-bkt
│
├── archive  # store verified data
│   ├── 202112141930
│   │   ├── 202112141930_type_A.csv
│   │   ├── 202112141930_type_B.csv
│   │   └── 202112141930_type_C.csv
│   ├── 202112141940
│   │   ├── 202112141940_type_A.csv
│   │   ├── 202112141940_type_B.csv
│   │   └── 202112141940_type_C.csv
│   └── …
├── clean_files  # store processed files
│   ├── 202112141930.parquet
│   ├── 202112141940.parquet
│   └── …
└── unprocessed.log  # contain info of data that can’t be processed
```
# Design Flowchart
![alt text](https://github.com/jhaojay/imdb_data_engineer_project_with_aws/blob/main/jpg/main_flowchart.JPG?raw=true)


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
<br /><br />
Run the following command to retrieve 3 tables of data and save to csv files:
```python
$ python3 prepare_files.py
```


# Usage
(Note: Assuming the reader has the knowledge of AWS's EC2 and S3, only brief instructions are given here.)

1. Launch two instances, named imdb-ec2 and de-ec2, and create two buckets, named imdb-bkt and de-bkt.
<br /><br />
2. Grant imdb-ec2 access to imdb-bkt, and grant de-ec2 access to both de-bkt and imdb-bkt.
<br /><br />
3. Use scp command to copy the Python scripts to the corresponding EC2:
```
$ sudo scp -i <key.pem> <from_local_dir> <to_ec2_dir>
```
<br /><br />
4. Copy the imdb_raw_data directory to imdb-ec2:
```python
$ sudo scp -i <key.pem> <local_imdb_raw_data_dir> -r <to_imdb_ec2_dir>
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
