import grpc
import queue
import time
import sys
import os 
import grpc
from concurrent import futures
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/database'))
sys.path.insert(0, utils_path)

import database_pb2 as database
import database_pb2_grpc as database_grpc

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_1_ADDRESS = 'database:50060'
DATABASE_2_ADDRESS = 'database:50061'
DATABASE_3_ADDRESS = 'database:50062'

key_value = dict()
vc = [0 for _ in range(3)]

def recv(order_id, event_vc):
    global vc
    vc[get_replica_index()] += 1
    for i in range(3):
        vc[i] = max(vc[i], event_vc[i])

def send(order_id, response):
    global vc
    vc[get_replica_index()] += 1
    return database.Response(stock=response, clock=vc)

class DatabaseService(database_grpc.DatabaseServiceServicer):
    def Read(self, request, context):
        logging.info("Received a write request: %s", request)
        recv(request.orderId, request.clock)

        response = send(request.orderId, key_value[i] if i in key_value else -1)
        logging.info("Read response: %s", response)
        return response

    def Write(self, request, context):
        logging.info("Received a write request: %s", request)
        recv(request.orderId, request.clock)

        response = send(request.orderId, 'not_fraud')
        logging.info("Write response: %s", response)

        return response

def get_replica_index():
    return os.environ.get('REPLICA_INDEX', '')

def get_next_replica_index():
    return get_replica_index() + 1

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    database_grpc.add_DatabaseServiceServicer_to_server(DatabaseService(), server)
    rid = get_replica_index()
    port = 50060 + int(rid)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info(f"Database Service ({rid}) started. Listening on port {port}.")

if __name__ == '__main__':
    serve()
