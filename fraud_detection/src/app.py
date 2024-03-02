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


# The main service, performs fraud detection
class FraudDetectionService(fraud_detection_grpc.FraudDetectionServiceServicer):
    def PerformDetection(self, request, context):
        logging.info("Received a fraud detection request: %s", request)
        response = fraud_detection.FraudDetectionResponse(response='not_fraud')
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
