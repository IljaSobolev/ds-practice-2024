import sys
import os
import json


from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer
import logging
import time
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, utils_path)
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)

trace.set_tracer_provider(TracerProvider())
span_exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
span_processor = BatchSpanProcessor(span_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Configure OpenTelemetry Metrics
metric_exporter = OTLPMetricExporter(endpoint="http://localhost:4317")
metric_reader = PeriodicExportingMetricReader(metric_exporter)
metrics.set_meter_provider(MeterProvider(metric_readers=[metric_reader]))

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Instrument gRPC server
grpc_server_instrumentor = GrpcInstrumentorServer()
grpc_server_instrumentor.instrument()

# Define Metrics
suggestion_counter = meter.create_counter(
    "suggestion_counter",
    unit="1",
    description="Counts the number of suggestions generated",
)

active_requests = meter.create_up_down_counter(
    "active_requests",
    unit="1",
    description="Tracks the number of active requests",
)

suggestion_time_histogram = meter.create_histogram(
    "suggestion_time_histogram",
    unit="ms",
    description="Measures the time taken to generate suggestions",
)

def get_active_sessions():
    # Logic to get the number of active sessions
    return len(cache)

meter.create_observable_gauge(
    "active_sessions",
    callbacks=[get_active_sessions],
    unit="1",
    description="Reports the number of active sessions",
)

# Configure logging
logging.basicConfig(level=logging.INFO)


import grpc
from concurrent import futures

books = json.loads(open('./suggestions/src/books.json', 'r').read())

FRAUD_DETECTION = 0
TRANSACTION_VERIFICATION = 1
SUGGESTIONS = 2

cache = dict()

def cache_insert(order_id, checkout_data):
    vc = [0 for _ in range(3)]
    cache[order_id] = checkout_data, vc

def recv(order_id, event_vc):
    vc = cache[order_id][1]
    vc[SUGGESTIONS] += 1
    for i in range(3):
        vc[i] = max(vc[i], event_vc[i])

def send(order_id, response):
    vc = cache[order_id][1]
    vc[SUGGESTIONS] += 1
    return suggestions.SuggestionResponse(suggestions=response, clock=vc)



# The book suggestion service
# The book suggestion service
# The book suggestion service
class SuggestionService(suggestions_grpc.SuggestionServiceServicer):
    def Initialize(self, request, context):
        with tracer.start_as_current_span("Initialize") as span:
            logging.info("Received an initialization request: %s", request)
            cache_insert(request.orderId, request.checkoutData)
            
            active_requests.add(1)
            start_time = time.time()
            
            response = send(request.orderId, [])
            
            active_requests.add(-1)
            suggestion_time_histogram.record((time.time() - start_time) * 1000)
            logging.info("Suggestions initialization: %s", response)
            return response
        
    def Suggest(self, request, context):
        with tracer.start_as_current_span("Suggest") as span:
            logging.info("Received a suggestion request: %s", request)

            active_requests.add(1)
            start_time = time.time()
            
            recv(request.orderId, request.clock)
            book_suggestions = [{'id': int(books[b]['id']), 'title': books[b]['title'], 'author': books[b]['author']} for b in books]
            logging.info("Sending book suggestions: %s", book_suggestions)
            
            response = send(request.orderId, book_suggestions)
            
            active_requests.add(-1)
            suggestion_time_histogram.record((time.time() - start_time) * 1000)
            suggestion_counter.add(1)
            
            return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    grpc_server_instrumentor.instrument()
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