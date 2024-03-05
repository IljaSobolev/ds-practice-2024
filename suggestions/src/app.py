import sys
import os
import json

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, utils_path)
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

import grpc
from concurrent import futures

books = json.loads(open('./suggestions/src/books.json', 'r').read())

# The book suggestion service
class SuggestionService(suggestions_grpc.SuggestionServiceServicer):
    def Suggest(self, request, context):
        logging.info("Received a suggestion request: %s", request)

        book_suggestions = [{'id': int(books[b]['id']), 'title': books[b]['title'], 'author': books[b]['author']} for b in books]
        logging.info("Sending book suggestions: %s", book_suggestions)

        response = suggestions.SuggestionResponse(suggestions=book_suggestions)
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add SuggestionService
    suggestions_grpc.add_SuggestionServiceServicer_to_server(SuggestionService(), server)
    # Listen on port 50053
    port = "50053"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    logging.info("Server started. Listening on port 50053.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
