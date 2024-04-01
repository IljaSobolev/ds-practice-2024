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

import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderQueueService(order_queue_grpc.OrderQueueServicer):
    def __init__(self):
        self.priority_queue = queue.PriorityQueue()

    def EnqueueOrder(self, request, context):
        # Calculate priority based on order value, number of books, or other criteria
        priority = -int(time.time()) - int(request.order.item.quantity)*100  

        # Enqueue the order with its priority
        self.priority_queue.put((priority, request))

        logger.info(f"Order {request} enqueued with priority {priority}")

        # Return the confirmation that the order is enqueued
        return order_queue.OrderResponse(status='enqueued')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    order_queue_grpc.add_OrderQueueServicer_to_server(OrderQueueService(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    logger.info("Order Queue Service started. Listening on port 50054.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
