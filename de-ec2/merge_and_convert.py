#!/usr/bin/env python3

import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import csv

def merge_and_convert_to_parquet(type_A, type_B, type_C, destination_dir_path):
    """merge all 3 files and return dataframe and convert to parquet"""
    df1 = pd.read_csv(type_A)
    df2 = pd.read_csv(type_B)
    df3 = pd.read_csv(type_C)


    df4 = df1.merge(df2, left_on="id", right_on="movie_id")
    del df4["id"]

    df5 = df4.merge(df3, left_on='person_id', right_on='id')
    del df5["id"]

    df5 = df5.rename({'full_name': 'director_name'}, axis=1)
    table = pa.Table.from_pandas(df5)
    pq.write_table(table, destination_dir_path)


