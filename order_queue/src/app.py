import grpc
import queue
import time

import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderQueueService(order_queue_grpc.OrderQueueServiceServicer):
    def __init__(self):
        self.priority_queue = queue.PriorityQueue()

    def Enqueue(self, request, context):
        # Calculate priority based on order value, number of books, or other criteria
        priority = self.calculate_priority(request)

        # Enqueue the order with its priority
        self.priority_queue.put((priority, request))

        logger.info(f"Order {request.orderId} enqueued with priority {priority}")

        # Return the confirmation that the order is enqueued
        return order_queue.OrderResponse(status='enqueued')

    def calculate_priority(self, request):
        # Example: Calculate priority based on order value
        # priority = request.orderValue
        # You can adjust this logic based on your specific requirements

        # For simplicity, let's use order timestamp as priority (earlier orders have higher priority)
        priority = -int(time.time())  # Negative sign for descending order (earlier timestamp gets higher priority)
        return priority

def serve():
    server = grpc.server(grpc.ThreadPoolExecutor())
    order_queue_grpc.add_OrderQueueServiceServicer_to_server(OrderQueueService(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    logger.info("Order Queue Service started. Listening on port 50054.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
