# Quick Poc with Nameko, Kafka and Flask

## Architecture

### Services

- API (flask):
  - Make asynchronous calls to nameko services ping and pong.
  - Endpoints are synchronous. 
  TODO: They should be asynchronous and return a 202. 
- Ping (nameko service):
  - exposes a RPC endpoint to send messages to pong topic.
  - consumes messages from ping topic
- Pong (nameko service):
  - exposes a RPC endpoint to send messages to pong topic.
  - consumes messages from pong topic and sends another message to ping topic

### Brokers

- Zookeeper: Required by kafka
- Kafka: Messages
- Rabbit: Async communication between services

## Run with docker compose

Run brokers with `docker-compose up --build broker zookeeper rabbit`

In a separate terminal, run the services:

Run `docker-compose up --build ping pong api`

## Test

Create one example of test for ping service. Run `pytest`

## Benchmarking

Very simple metrics:

- Producers:

    To send messages from ping to pong: `curl localhost:8000/ping/<num_messages>/<size>`. Then pong will generate a response to ping.

    To send messages from pong to ping: `curl localhost:8000/pong/<num_messages>/<size>`
    Ping will not generate a response to pong to break the look

    Endpoint response returns the metrics e.g:

    ```
        {
            "num_messages": 100,
            "size": 100,
            "total time": 3.14684796333313,
            "byte rate (MB/s)": 0.0031777830122457,
            "message rate (msg/s)": 31.777830122457
        }
    ```

- Consumers:

    We have to look at the logs produced by the consumer. There are better ways to track this with Confluent:

    Stats are computed in batches of 100 messages. Batch size can be modified in docker compose: `CONSUMER_METRIC_BATCH: "100"`

    Run `curl localhost:8000/ping/<num_messages>/<size>` to see the performance of the consumers in `ping` and `pong` services

    Run `curl localhost:8000/pong/<num_messages>/<size>` to see only the performance of the consumer in `ping` when sending messages from `pong`.

Kafka metrics are complicated. Next I list the most important metrics to track in production:

Key metrics:

- Producer:
  - Rate
  - Transmission failure

- Brokers
  - Load skew
  - Capacity
  
- Topics
  - Load skew. Some topics can be overloaded

- Consumers
  - Consumer rate
  
## Local development env

Developement enviroment can be created with `pipenv install` 

