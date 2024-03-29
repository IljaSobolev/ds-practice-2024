import sys
import os
import logging
# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures

logging.basicConfig(level=logging.INFO)

FRAUD_DETECTION = 0
TRANSACTION_VERIFICATION = 1
SUGGESTIONS = 2

cache = dict()

def cache_insert(order_id, checkout_data):
    vc = [0 for _ in range(3)]
    cache[order_id] = checkout_data, vc

def recv(order_id, event_vc):
    vc = cache[order_id][1]
    vc[FRAUD_DETECTION] += 1
    for i in range(3):
        vc[i] = max(vc[i], event_vc[i])

def send(order_id, response):
    vc = cache[order_id][1]
    vc[FRAUD_DETECTION] += 1
    return fraud_detection.FraudDetectionResponse(response=response, clock=vc)

# The main service, performs fraud detection
class FraudDetectionService(fraud_detection_grpc.FraudDetectionServiceServicer):
    def Initialize(self, request, context):
        logging.info("Received a initialization request: %s", request)

        cache_insert(request.orderId, request.checkoutData)
        
        response = send(request.orderId, 'initialized')
        logging.info("Fraud detection initialization: %s", response)
        return response

    def PerformUserDataFraudDetection(self, request, context):
        logging.info("Received a user data fraud detection request: %s", request)
        recv(request.orderId, request.clock)

        response = send(request.orderId, 'not_fraud')
        logging.info("Fraud detection response: %s", response)
        return response

    def PerformCreditCardFraudDetection(self, request, context):
        logging.info("Received a fraud detection request: %s", request)
        recv(request.orderId, request.clock)

        response = send(request.orderId, 'not_fraud')
        logging.info("Fraud detection response: %s", response)

        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add FraudDetectionService
    fraud_detection_grpc.add_FraudDetectionServiceServicer_to_server(FraudDetectionService(), server)
    # Listen on port 50051
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    logging.info("Server started. Listening on port 50051.")

    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
