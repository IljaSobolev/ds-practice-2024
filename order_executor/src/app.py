import grpc
import queue
import time
import sys
import os 
import grpc
from concurrent import futures
from google.protobuf.json_format import MessageToJson
import json

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_executor'))
sys.path.insert(0, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/database'))
sys.path.insert(0, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment_system'))
sys.path.insert(0, utils_path)

import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc
import order_executor_pb2 as order_executor
import order_executor_pb2_grpc as order_executor_grpc
import database_pb2 as database
import database_pb2_grpc as database_grpc
import payment_system_pb2 as payment_system
import payment_system_pb2_grpc as payment_system_grpc

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ORDER_QUEUE_ADDRESS = 'order_queue:50054'
PAYMENT_SYSTEM_ADDRESS = 'payment_system:50065'
DATABASE_WRITE_ADDRESS = 'database1:50060'

vc = [0 for _ in range(3)]

def recv(event_vc):
    global vc
    vc[0] += 1
    for i in range(3):
        vc[i] = max(vc[i], event_vc[i])

def send():
    global vc
    vc[0] += 1

class OrderExecutorService(order_executor_grpc.OrderExecutorServicer):
    def Execute(self, request, context):
        logging.info("Received an execute request: %s", request)
        recv(request.clock)

        request_json = json.loads(MessageToJson(request))
        for i in request_json['checkoutData']['items']:
            i['quantity'] = int(i['quantity'])

        # 2PC coordinator
        logging.info("asking commitment from database ...")
        commit = True
        with grpc.insecure_channel(DATABASE_WRITE_ADDRESS) as channel:
            stub = database_grpc.DatabaseServiceStub(channel)

            send()
            response = stub.QueryToCommit(database.QueryRequest(query=request_json['checkoutData'], clock=vc))
            logging.info(f"database answered: {response.msg}")
            if response.msg != "yes":
                commit = False


        logging.info("asking commitment from payment system ...")
        with grpc.insecure_channel(PAYMENT_SYSTEM_ADDRESS) as channel:
            stub = payment_system_grpc.PaymentSystemStub(channel)

            send()
            response = stub.QueryToCommit(payment_system.QueryRequest(query=request_json['checkoutData'], clock=vc))
            logging.info(f"payment system answered: {response.msg}")
            if response.msg != "yes":
                commit = False

        if commit:
            logging.info("all participants answered yes, performing the commit ...")
            with grpc.insecure_channel(DATABASE_WRITE_ADDRESS) as channel:
                stub = database_grpc.DatabaseServiceStub(channel)

                newstock = int(time.time())
                logging.info(f"writing value {newstock} to database ...")

                send()
                response = stub.Write(database.WriteRequest(title='title', stock=newstock, clock=vc))

            # call payment processing methods ...

        send()
        response = order_executor.ExecuteResponse(error=not commit, clock=vc)
        logging.info("Execution response: %s", response)
        return response

def get_replica_index():
    return os.environ.get('REPLICA_INDEX', '')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    order_executor_grpc.add_OrderExecutorServicer_to_server(OrderExecutorService(), server)
    rid = get_replica_index()
    port = 50055 + int(rid)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info(f"Order Executor Service ({rid}) started. Listening on port {port}.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
