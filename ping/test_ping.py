""" Example of service unit testing best practice. """

from nameko.testing.services import worker_factory
from ping import PingService
import json

def test_send():
    # create worker with mock dependencies
    service = worker_factory(PingService)

    # test send service rpc method
    result = service.send(num_messages=10, size=5)

    # Validate that we call kafka producer flush once
    service.producer.flush.assert_called_once()

    # Test stats returned
    stats = json.loads(result)
    assert sorted(list(stats.keys())) == \
        [
            'byte rate (MB/s)',
            'message rate (msg/s)',
            'num_messages',
            'size',
            'total time'
        ]

def test_compute_stats():
    # create worker with mock dependencies
    service = worker_factory(PingService)

    # test compute stats
    result = service.compute_consumer_stats(total_time=10, num_messages=3, size=3)
    assert result == {
        'num_messages': 3,
        'size': 3,
        'total time': 10,
        'byte rate (MB/s)': 9.000000000000001e-07,
        'message rate (msg/s)': 0.3
    }
