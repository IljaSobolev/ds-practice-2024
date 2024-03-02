import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

import grpc
import threading

class WorkerThread(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__(target=target, args=args)
        self._result = None

    def run(self):
        self._result = self._target(*self._args)

    @property
    def result(self):
        return self._result

"""
def greet(name='you'):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.HelloServiceStub(channel)
        # Call the service through the stub object.
        response = stub.SayHello(fraud_detection.HelloRequest(name=name))
    return response.greeting
"""

# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request, jsonify
from flask_cors import CORS

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app)

# Define a GET endpoint.
@app.route('/', methods=['GET'])
def index():
    """
    Responds with 'Hello, [name]' when a GET request is made to '/' endpoint.
    """
    # Test the fraud-detection gRPC service.
    #response = greet(name='orchestrator')
    # Return the response.
    return 'index'

# gRPC server addresses
FRAUD_DETECTION_ADDRESS = 'fraud_detection:50051'
TRANSACTION_VERIFICATION_ADDRESS = 'transaction_verification:50052'
SUGGESTIONS_ADDRESS = 'suggestions:50053'

def perform_fraud_detection(checkout_data):
    with grpc.insecure_channel(FRAUD_DETECTION_ADDRESS) as channel:
        stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
        response = stub.PerformDetection(fraud_detection.FraudDetectionRequest(checkoutData=checkout_data))
    return response

def perform_transaction_verification(credit_card):
    with grpc.insecure_channel(TRANSACTION_VERIFICATION_ADDRESS) as channel:
        stub = transaction_verification_grpc.VerificationServiceStub(channel)
        response = stub.Verify(transaction_verification.VerificationRequest(creditCard=credit_card))
    return response

def perform_suggestions(checkout_data):
    with grpc.insecure_channel(SUGGESTIONS_ADDRESS) as channel:
        stub = suggestions_grpc.SuggestionServiceStub(channel)
        response = stub.Suggest(suggestions.SuggestionRequest(checkoutData=checkout_data))
    return response
@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    # Print request object data
    print("Request Data:", request.json)

    checkout_data = request.json

    # Worker threads for parallel processing
    fraud_thread = WorkerThread(target=perform_fraud_detection, args=(checkout_data,))
    verification_thread = WorkerThread(target=perform_transaction_verification, args=(checkout_data['creditCard'],))
    suggestions_thread = WorkerThread(target=perform_suggestions, args=(checkout_data,))

    # Start the threads
    fraud_thread.start()
    verification_thread.start()
    suggestions_thread.start()

    # Wait for all threads to finish
    fraud_thread.join()
    verification_thread.join()
    suggestions_thread.join()

    # Get results from threads
    fraud_result = fraud_thread.result
    verification_result = verification_thread.result
    suggestions_result = suggestions_thread.result

    print(f"fraud result: {fraud_result}")
    print(f"verification result: {verification_result}")
    # Process results and create response
    # Check results and make decision
    order_status_response = {}

    if fraud_result.response == "fraud" or verification_result.response == "rejected":
        # If fraud detected or transaction verification failed, reject the order
        order_status_response = {
            'orderId': '12345',
            'status': 'Order Rejected',
            'message': 'Fraud detected or transaction verification failed.'
        }
    else:
        # If no fraud detected and transaction verified, approve the order and include suggested books
        suggested_books = [{'bookId': s.id, 'title': s.title, 'author': s.author} for s in suggestions_result.suggestions]

        order_status_response = {
            'orderId': '12345',
            'status': 'Order Approved',
            'suggestedBooks': suggested_books
        }

    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
