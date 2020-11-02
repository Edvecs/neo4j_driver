import json
import boto3
import jwt
from neo4j import GraphDatabase, basic_auth

class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed: ",  e)
        finally: 
            if session is not None:
                session.close()
        return response

def get_parameters(ParameterName):
    ssm = boto3.client('ssm', 'us-west-2')
    response = ssm.get_parameters( Names=[ParameterName], WithDecryption=True )
    for parameter in response['Parameters']:
        return parameter['Value']


def connect_to_driver(event_body):
    try:
        neo4j_uri = get_parameters('/development/database/NEO4J_URI')
    except Exception as e:
        return 'Uri has not been set or cannot be fetched: ' + str(e)
    try:
        neo4j_user = get_parameters('/development/database/NEO4J_USER')
    except Exception as e:
        return 'User has not been set or cannot be fetchedi: '+ str(e)

    try:
        neo4j_password = get_parameters('/development/database/NEO4J_PASSWORD')
    except Exception as e:
        return 'Password has not been set or cannot be fetched: ' + str(e)

    try:
        jwt_secret = get_parameters('/development/database/JWT_SECRET')
    except Exception as e:
        return 'jwt secret has not been set or cannot be fetched: ' + str(e)

#    try:
#        data_decode = jwt.decode(event_body['token'], jwt_secret, algorithms=['HS256'])
#    except Exception as e:
#        return 'data decode: ' + str(e)


    try:
        conn = Neo4jConnection(uri=neo4j_uri, user=neo4j_user, pwd=neo4j_password)
    except Exception as e:
        return "connection error: " + str(e) 

    query_string = "MATCH (n) RETURN COUNT(n) AS num"

    result = ''
    try:
        results = conn.query(query_string, db=event_body['database'])
        for record in results:
            result = record["num"]
    except Exception as e:
        return "query failed: " + str(e)

    return result

def verify_token():
   return true

def execute_select(event, context):
    event_body = json.loads(event['body'])

    event = connect_to_driver(event_body)

    response = {
        "statusCode": 200,
        "body": json.dumps({ 'result': event })
    }

    return response
