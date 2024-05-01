import sys
import os
import logging
# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment_system'))
sys.path.insert(0, utils_path)
import payment_system_pb2 as payment_system
import payment_system_pb2_grpc as payment_system_grpc

import grpc
from concurrent import futures

logging.basicConfig(level=logging.INFO)

global vc

def recv(event_vc):
    global vc
    vc += 1
    vc = max(vc, event_vc)

def send(response):
    global vc
    vc += 1
    return payment_system.Response(response=response, clock=vc)

class PaymentSystem(payment_system_grpc.PaymentSystemServicer):
    def QueryToCommit(self, request, context):
        # 2PC participant
        logging.info("Received a query to commit: %s", request)
        recv(request.clock)

        response = send('yes')
        logging.info("Payment system query to commit response: %s", response)
        return response

    # actual functions for payment processing ...
    # def Process(self, request, context):
    # ...

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add FraudDetectionService
    payment_system_grpc.add_PaymentSystemServicer_to_server(PaymentSystem(), server)
    # Listen on port 50065
    port = "50065"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    logging.info(f"Payment System started. Listening on port {port}.")

    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
