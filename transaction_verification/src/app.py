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

# The verification service
class VerificationService(transaction_verification_grpc.VerificationServiceServicer):
    def Verify(self, request, context):
        logging.info("Received a verification request: %s", request)
        response = 'verified'
        
        # Check if request is not null
        if (request is None):
            response = 'rejected'

        # Check if creditcard number is valid
        if len(request.creditCard.number) != 16:
            response = 'rejected'

        # Check if expiration date is mm/yy 
        if len(request.creditCard.expirationDate) != 5:
            response = 'rejected'


        # Check if card is not expired
        month, year = map(int, request.creditCard.expirationDate.split('/'))
        now = datetime.datetime.now()
        if year * 100 + month < (now.year % 100) * 100 + now.month:
            response = 'rejected'

        # Check if CVV is valid.
        if len(request.creditCard.cvv) != 3:
            response = 'rejected'

        response = transaction_verification.VerificationResponse(response=response)
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
