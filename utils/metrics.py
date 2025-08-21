from prometheus_client import Counter, Histogram, Gauge

request_count = Counter(
    'legal_ai_requests_total',
    'Total number of requests processed',
    ['request_type', 'status']
)

processing_time = Histogram(
    'legal_ai_processing_seconds',
    'Time spent processing requests',
    ['request_type']
)

confidence_score = Gauge(
    'legal_ai_confidence_score',
    'Current confidence score of predictions'
)

def setup_monitoring():
    pass
