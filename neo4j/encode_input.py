import json
import boto3
import jwt
import sys
from neo4j import GraphDatabase, basic_auth

def get_parameters(ParameterName):
    ssm = boto3.client('ssm', 'us-west-2')
    response = ssm.get_parameters( Names=[ParameterName], WithDecryption=True )
    for parameter in response['Parameters']:
        return parameter['Value']


def main ():
    try:
       database = sys.argv[1]
    except:
        return 'Error: please enter a database name that you want to connect'

    print('Database name: ' + database)

    try:
        jwt_secret = get_parameters('/development/database/JWT_SECRET')
    except Exception as e:
        return 'Error: jwt secret has not been set or cannot be fetched: ' + str(e)

    try:
        encoded = jwt.encode({'database' : database}, str(jwt_secret), algorithm='HS256')
    except Exception as e:
        return 'data encode: ' + str(e)

    print(encoded)
    return 0

if __name__ == "__main__":
   main()
