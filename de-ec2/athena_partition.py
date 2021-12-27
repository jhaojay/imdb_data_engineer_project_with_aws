#!/usr/bin/env python3

import boto3
import time
import configparser

def execute_athena_query(client, dbname, out_location, query):
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': dbname
        },
        ResultConfiguration={
            'OutputLocation': out_location
        }
    )

    while True:
        try:
            query_results = client.get_query_results(
                QueryExecutionId=response['QueryExecutionId']
            )
            print("Query finished.")
            return query_results
        except Exception as err:
            if 'Query has not yet finished' in err.args[0]:
                time.sleep(3)
            else:
                raise(err)


def partition_parquet(partition_column_name, partition_value, file_s3_location):
    config = configparser.ConfigParser()
    config.read("athena_config.ini")

    # load config
    id = config.get("athena_section", "access_id")
    key = config.get("athena_section", "access_key")
    region = config.get("athena_section", "region")
    dbname = config.get("athena_section", "database_name")
    tbname = config.get("athena_section", "table_name")
    out_s3 = config.get("athena_section", "output_s3_location")

    query = """ALTER TABLE {0}.{1} ADD PARTITION ({2}='{3}') LOCATION '{4}'""".format(
        dbname,
        tbname,
        partition_column_name,
        partition_value,
        file_s3_location
    )

    athena_client = boto3.client(
        'athena',
        region_name=region,
        aws_access_key_id=id,
        aws_secret_access_key=key
    )

    execute_athena_query(athena_client, dbname, out_s3, query)


