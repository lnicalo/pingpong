from flask import Flask, Response
from flask_nameko import FlaskPooledClusterRpcProxy


rpc = FlaskPooledClusterRpcProxy()

def create_app():
    app = Flask(__name__)
    app.config.update(dict(
        NAMEKO_AMQP_URI='amqp://rabbit'
        )
    )

    rpc.init_app(app)
    return app

app = create_app()

@app.route('/healthcheck')
def healthcheck():
    return 'All good from api!'

@app.route('/benchmark/<int:num_messages>/<int:size>', methods=["GET"])
def benchmark(num_messages, size):
    if num_messages < 1 or size < 1:
        return Response(
            f'Invalid param: num_messages={num_messages} and size={size}',
            status=400,
        )
    result = rpc.ping.send(num_messages=num_messages, size=size)
    return Response(result, status=200)

@app.route('/ping/<int:num_messages>/<int:size>', methods=["GET"])
def ping(num_messages, size):
    if num_messages < 1 or size < 1:
        return Response(
            f'Invalid param: num_messages={num_messages} and size={size}',
            status=400,
        )
    result = rpc.ping.send(num_messages=num_messages, size=size)
    return Response(result, status=200)

@app.route('/pong/<int:num_messages>/<int:size>', methods=["GET"])
def pong(num_messages, size):
    if num_messages < 1 or size < 1:
        return Response(
            f'Invalid param: num_messages={num_messages} and size={size}',
            status=400,
        )
    result = rpc.pong.send(num_messages=num_messages, size=size)
    return Response(result, status=200)

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)