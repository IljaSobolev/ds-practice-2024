import sys
import os
import logging
import queue
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path)

import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

import grpc
import threading

class WorkerThread(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__(target=target, args=args)
        self._result = None
        self.in_queue = queue.Queue()

    def run(self):
        self._result = self._target(*self._args)

    def send(self, msg, vc=None):
        self.in_queue.put((msg, vc))

    @property
    def result(self):
        return self._result

orchestrator_queue = queue.Queue()
def send_orchestrator(msg):
    orchestrator_queue.put(msg)

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
ORDER_QUEUE_ADDRESS = 'order_queue:50054'


FRAUD_DETECTION = 0
TRANSACTION_VERIFICATION = 1
SUGGESTIONS = 2

message_queue = queue.Queue()

def perform_fraud_detection(checkout_data, order_id, threads):
    with grpc.insecure_channel(FRAUD_DETECTION_ADDRESS) as channel:
        stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)

        stub.Initialize(fraud_detection.FraudDetectionRequest(checkoutData=checkout_data, clock=[0, 0, 0], orderId=order_id))

        while True:
            message, clock = threads[FRAUD_DETECTION].in_queue.get()
            if message == 'items_not_empty':
                response = stub.PerformUserDataFraudDetection(fraud_detection.FraudDetectionRequest(checkoutData=checkout_data, clock=clock, orderId=order_id))
                if response.response == 'fraud':
                    send_orchestrator(response.response)
                    return response

                threads[TRANSACTION_VERIFICATION].send('user_data_not_fraud', response.clock)

            elif message == 'credit_card_verified':
                response = stub.PerformCreditCardFraudDetection(fraud_detection.FraudDetectionRequest(checkoutData=checkout_data, clock=clock, orderId=order_id))
                if response.response == 'fraud':
                    send_orchestrator(response.response)
                    return response

                threads[SUGGESTIONS].send('credit_card_not_fraud', response.clock)

            elif message == 'stop':
                return

    return response

def perform_transaction_verification(checkout_data, order_id, threads):
    with grpc.insecure_channel(TRANSACTION_VERIFICATION_ADDRESS) as channel:
        stub = transaction_verification_grpc.VerificationServiceStub(channel)

        response = stub.Initialize(transaction_verification.VerificationRequest(checkoutData=checkout_data, clock=[0, 0, 0], orderId=order_id))

        response = stub.VerifyNotEmpty(transaction_verification.VerificationRequest(checkoutData=checkout_data, clock=response.clock, orderId=order_id))
        response = stub.VerifyUserData(transaction_verification.VerificationRequest(checkoutData=checkout_data, clock=response.clock, orderId=order_id))
        if response.response == 'rejected':
            send_orchestrator(response.response)
            return response

        threads[FRAUD_DETECTION].send('items_not_empty', response.clock)

        while True:
            message, clock = threads[TRANSACTION_VERIFICATION].in_queue.get()
            if message == 'user_data_not_fraud':
                response = stub.VerifyCreditCard(transaction_verification.VerificationRequest(checkoutData=checkout_data, clock=clock, orderId=order_id))
                if response.response == 'rejected':
                    send_orchestrator(response.response)
                    return response

                threads[FRAUD_DETECTION].send('credit_card_verified', response.clock)

            elif message == 'stop':
                return
    return response

def perform_suggestions(checkout_data, order_id, threads):
    with grpc.insecure_channel(SUGGESTIONS_ADDRESS) as channel:
        stub = suggestions_grpc.SuggestionServiceStub(channel)

        response = stub.Initialize(suggestions.SuggestionRequest(checkoutData=checkout_data, orderId=order_id))

        while True:
            message, clock = threads[SUGGESTIONS].in_queue.get()
            if message == 'credit_card_not_fraud':
                response = stub.Suggest(suggestions.SuggestionRequest(checkoutData=checkout_data, clock=clock, orderId=order_id))
                send_orchestrator(response.suggestions)
                return response

            elif message == 'stop':
                return

    return response
def enqueue_order(order_id, checkout_data):
    with grpc.insecure_channel(ORDER_QUEUE_ADDRESS) as channel:
        stub = order_queue_grpc.OrderQueueServiceStub(channel)
        response = stub.EnqueueOrder(order_queue.EnqueueOrderRequest(orderId=order_id, checkoutData=checkout_data))
        if response.status == 'success':
            logging.info(f"Order {order_id} enqueued successfully.")
        else:
            logging.error(f"Failed to enqueue order {order_id}. Reason: {response.message}")
@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    # Print request object data
    print("Request Data:", request.json)
    logger.info("Received a checkout request.")

    order_id = int(time.time() * 100000)

    checkout_data = request.json

    threads = [None for _ in range(3)]

    # Worker threads for parallel processing
    fraud_thread = WorkerThread(target=perform_fraud_detection, args=(checkout_data, order_id, threads))
    verification_thread = WorkerThread(target=perform_transaction_verification, args=(checkout_data, order_id, threads))
    suggestions_thread = WorkerThread(target=perform_suggestions, args=(checkout_data, order_id, threads))

    threads[FRAUD_DETECTION] = fraud_thread
    threads[TRANSACTION_VERIFICATION] = verification_thread
    threads[SUGGESTIONS] = suggestions_thread

    # Start the threads
    fraud_thread.start()
    verification_thread.start()
    suggestions_thread.start()

    approved = True

    msg = orchestrator_queue.get()
    if msg == 'fraud' or msg == 'rejected':
        approved = False
        logger.info(f"Rejected: {msg}")
    else:
        suggestions = msg

    fraud_thread.send('stop')
    verification_thread.send('stop')
    suggestions_thread.send('stop')

    # Wait for all threads to finish
    fraud_thread.join()
    verification_thread.join()
    suggestions_thread.join()

    # Process results and create response
    # Check results and make decision
    order_status_response = {}

    if not approved:
        # If fraud detected or transaction verification failed, reject the order
        order_status_response = {
            'orderId': order_id,
            'status': 'Order Rejected',
            'message': 'Fraud detected or transaction verification failed.'
        }
    else:
        # If no fraud detected and transaction verified, approve the order and include suggested books
        suggested_books = [{'bookId': s.id, 'title': s.title, 'author': s.author} for s in suggestions]
        order_queue_thread = WorkerThread(target=enqueue_order, args=(order_id, checkout_data))
        order_queue_thread.start()
        order_queue_thread.join() 
        
        order_status_response = {
            'orderId': order_id,
            'status': 'Order Approved',
            'suggestedBooks': suggested_books
        }
    logger.info("Sending order status response.")

    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0', debug = True)
