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
# Usage
Note: Assuming the reader has the knowledge of AWS's EC2 and S3, only brief instructions are given here.

1. Launch two instances, named imdb-ec2 and de-ec2, and create two buckets, named imdb-bkt and de-bkt.
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
