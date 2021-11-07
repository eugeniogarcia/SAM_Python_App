import json
import os

import boto3
import pandas as pd

import debugpy
#debugpy.listen(("127.0.0.1", 5890))
#debugpy.listen(("localhost", 5890))
debugpy.listen(("0.0.0.0", 5890))
# debugpy.listen(5890)
print('Esperando a que se conecte un cliente')
debugpy.wait_for_client()
print('Se conecto')


def lambda_handler(event, context):
    debugpy.breakpoint()
    print('## VARIABLES DE ENTORNO')
    print(os.environ)
    print('## EVENTO')
    print(event)

    s3 = boto3.client('s3')
    bucket = "egsmartin"
    key = "ratings/bloque=1/ratings1.csv"

    print('Lee datos del s3.')
    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        initial_df = pd.read_csv(data['Body'], sep=';', encoding='windows-1252')
    except Exception as e:
        print(e)
        raise(e)

    print('Contenido que he leido del s3:')
    print(initial_df.head(3))

    return {
        "statusCode": 200,
        "headers": {"x-custom-header": "mi cabecera custom"},
        "body": json.dumps({
            "message": "hello world",
            "tops": initial_df[initial_df['Rating'] > 4].head(10).to_string()
        }),
    }
