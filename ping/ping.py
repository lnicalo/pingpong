from nameko.dependency_providers import Config
from nameko.rpc import rpc
import logging
from nameko_kafka import KafkaProducer, consume
import json
import os
import time


def log_stats(func):
    def inner(self, message, stats={}):
        stats['num_messages'] = stats.get('num_messages', 0) + 1
        stats['total_bytes'] = stats.get('total_bytes', 0) + message.serialized_value_size
        if 'start' not in stats:
            stats['start'] = time.time()
        result = func(self, message)
        stats['total time'] = time.time() - stats['start'] + 0.00001
        stats['byte rate (MB/s)'] = stats['total_bytes'] / stats['total time'] / 1000000
        stats['message rate (msg/s)'] = stats['num_messages'] / stats['total time']
        if not stats['num_messages'] % int(os.environ.get('CONSUMER_METRIC_BATCH', 10000)):
            logging.info(f'Consumer performance stats: {stats}')
            with open('consumer_performance.json', 'w') as f:
                json.dump(stats, f, indent=4)
            stats['start'] = time.time()
            stats['num_messages'] = 0
            stats['total_bytes'] = 0
        return result
    return inner

class PingService:
    """
        Ping service
    """
    name = "ping"
    config = Config()
    producer = KafkaProducer(metrics_num_samples=1)
    debug=False
    
    def _on_send_error(self, excp):
        logging.error('Error sending message', exc_info=excp)
        # handle exception
        # Note: implement a retry logic, or a dead letter queue, ...

    def send_message(self, message_id, size):
        msg = b'\0' * size
        future = self.producer.send("pong", value=msg)
        future.add_errback(self._on_send_error)
    
    @log_stats
    def handle_message(self, message):
        # Expensive computation of around 0.025 seconds
        #for _ in range(1, 1000000):
        #    pass
        if self.debug:
            logging.info('#' * 30)
            logging.info(message)
            logging.info('#' * 30)

    def compute_consumer_stats(self, total_time, num_messages, size):
        stats = {
            'num_messages': num_messages,
            'size': size,
            'total time': total_time,
            'byte rate (MB/s)': size * num_messages / total_time / 1000000,
            'message rate (msg/s)': num_messages / total_time
        }
        return stats        

    @rpc
    def send(self, num_messages, size=10):
        start = time.time()
        for i in range(num_messages):
            self.send_message(message_id=i, size=size)
        self.producer.flush()
        end = time.time()
        stats = self.compute_consumer_stats(end-start, num_messages, size)
        logging.info(f'Sent messages stats: {stats}')
        return json.dumps(stats)
        


    @consume(
            "ping",
            group_id="ping-group")
    def consume_ping(self, message):
        # Your message handler
        self.handle_message(message) 
