import grpc
import queue
import time
import sys
import os 
import grpc
from concurrent import futures
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_executor'))
sys.path.insert(0, utils_path)

import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc
import order_executor_pb2 as order_executor
import order_executor_pb2_grpc as order_executor_grpc

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ORDER_QUEUE_ADDRESS = 'order_queue:50054'

class OrderExecutorService(order_executor_grpc.OrderExecutorServicer):
    pass

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
