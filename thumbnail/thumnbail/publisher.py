import pika
EXCHANGE = 'THUMBNAILS'
EXCHANGE_TYPE = 'direct'
QUEUE_NAME = "thumbnail_sending_queue"
ROUTING_KEY = "thumbnail_details"

credentials = pika.PlainCredentials("user", "pass")
params = pika.ConnectionParameters(host="localhost", credentials=credentials)

def publish(message):
    connection = pika.BlockingConnection(parameters=params)
    with connection:
        channel = connection.channel()
        channel.exchange_declare(
            exchange=EXCHANGE,
            exchange_type=EXCHANGE_TYPE
        )

        channel.queue_declare(queue=QUEUE_NAME)

        channel.queue_bind(
            QUEUE_NAME,
            EXCHANGE,
            ROUTING_KEY
        )
        
        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=ROUTING_KEY,
            body=message
        )
