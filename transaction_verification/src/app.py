import sys
import os
import json
import logging
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import grpc
from concurrent import futures

FRAUD_DETECTION = 0
TRANSACTION_VERIFICATION = 1
SUGGESTIONS = 2

cache = dict()

def cache_insert(order_id, checkout_data):
    vc = [0 for _ in range(3)]
    cache[order_id] = checkout_data, vc

def recv(order_id, event_vc):
    vc = cache[order_id][1]
    vc[TRANSACTION_VERIFICATION] += 1
    for i in range(3):
        vc[i] = max(vc[i], event_vc[i])

def send(order_id, response):
    vc = cache[order_id][1]
    vc[TRANSACTION_VERIFICATION] += 1
    return transaction_verification.VerificationResponse(response=response, clock=vc)

# The verification service
class VerificationService(transaction_verification_grpc.VerificationServiceServicer):
    def Initialize(self, request, context):
        logging.info("Received a initialization request: %s", request)
        cache_insert(request.orderId, request.checkoutData)
        
        response = send(request.orderId, 'initialized')
        logging.info("Transaction verification initialization: %s", response)
        return response

    def VerifyNotEmpty(self, request, context):
        logging.info("Received a not empty verification request: %s", request)
        recv(request.orderId, request.clock)

        response = send(request.orderId, 'verified' if len(request.checkoutData.items) > 0 else 'rejected')
        logging.info("Transaction verification response: %s", response)
        return response

    def VerifyUserData(self, request, context):
        logging.info("Received a user data verification request: %s", request)
        recv(request.orderId, request.clock)

        response = send(request.orderId, 'verified')
        logging.info("Transaction verification response: %s", response)
        return response
        
    def VerifyCreditCard(self, request, context):
        logging.info("Received a credit card verification request: %s", request)
        recv(request.orderId, request.clock)
        
        # Check if request is not null
        if (request is None):
            logging.error("request is null")
            response = send(request.orderId, 'rejected')
            logging.info("Sending verification response: %s", response)
            return response

        # Check if creditcard number is valid
        if len(request.checkoutData.creditCard.number) != 16:
            logging.error("credit card number is not valid")
            response = send(request.orderId, 'rejected')
            logging.info("Sending verification response: %s", response)
            return response

        # Check if expiration date is mm/yy 
        if len(request.checkoutData.creditCard.expirationDate) != 5:
            logging.error("credit card expiration date is not valid")
            response = send(request.orderId, 'rejected')
            logging.info("Sending verification response: %s", response)
            return response

        # Check if card is not expired
        month, year = map(int, request.checkoutData.creditCard.expirationDate.split('/'))
        now = datetime.datetime.now()
        if year * 100 + month < (now.year % 100) * 100 + now.month:
            logging.error("credit card is expired")
            response = send(request.orderId, 'rejected')
            logging.info("Sending verification response: %s", response)
            return response

        # Check if CVV is valid.
        if len(request.checkoutData.creditCard.cvv) != 3:
            logging.error("credit card cvv is not valid")
            response = send(request.orderId, 'rejected')
            logging.info("Sending verification response: %s", response)
            return response

        response = send(request.orderId, 'verified')
        logging.info("Sending verification response: %s", response)
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add VerificationService
    transaction_verification_grpc.add_VerificationServiceServicer_to_server(VerificationService(), server)
    # Listen on port 50052
    port = "50052"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    logging.info("Server started. Listening on port 50052.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
