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

DATABASE_1_ADDRESS = 'database1:50060'
DATABASE_2_ADDRESS = 'database2:50061'
DATABASE_3_ADDRESS = 'database3:50062'
DATABASE_ADDRESS = [DATABASE_1_ADDRESS, DATABASE_2_ADDRESS, DATABASE_3_ADDRESS]

key_value = dict()
vc = [0 for _ in range(3)]

def recv(event_vc):
    global vc
    vc[get_replica_index()] += 1
    for i in range(3):
        vc[i] = max(vc[i], event_vc[i])

def send(stock):
    global vc
    vc[get_replica_index()] += 1
    return database.ReadWriteResponse(stock=stock, clock=vc)

class DatabaseService(database_grpc.DatabaseServiceServicer):
    def Read(self, request, context):
        logging.info("Received a read request: %s", request)
        recv(request.clock)

        response = send(key_value[request.title] if request.title in key_value else -1)
        logging.info("Read response: %s", response)
        return response

    def Write(self, request, context):
        logging.info("Received a write request: %s", request)
        recv(request.clock)

        key_value[request.title] = request.stock

        if get_next_replica_index() != 0:
            with grpc.insecure_channel(DATABASE_ADDRESS[get_next_replica_index()]) as channel:
                stub = database_grpc.DatabaseServiceStub(channel)

                send(int(request.stock))
                stub.Write(request)

        response = send(request.stock)
        logging.info("Write response: %s", response)

        return response

    def QueryToCommit(self, request, context):
        # 2PC participant
        logging.info("Received a query to commit: %s", request)
        recv(request.clock)

        vc[get_replica_index()] += 1
        response = database.Response(msg='yes', clock=vc)
        logging.info("Payment system query to commit response: %s", response)
        return response

def get_replica_index():
    return int(os.environ.get('REPLICA_INDEX', ''))

def get_next_replica_index():
    return (get_replica_index() + 1) % 3

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    database_grpc.add_DatabaseServiceServicer_to_server(DatabaseService(), server)
    rid = get_replica_index()
    port = 50060 + int(rid)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info(f"Database Service ({rid}) started. Listening on port {port}.")

    # initialize a random key
    key_value['title'] = 4
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
