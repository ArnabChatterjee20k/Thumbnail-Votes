import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika import spec

EXCHANGE = 'THUMBNAILS'
EXCHANGE_TYPE = 'direct'
QUEUE_NAME = "thumbnail_sending_queue"
ROUTING_KEY = "thumbnail_details"
from votes.utils.vote import add_thumbnail
import json

def callback(channel:BlockingChannel, method:spec.Basic.Deliver, properties, body):
    try:
        response = json.loads(body.decode())
        message = response.get("message")
        print(f"Received {message}")
        project_id = response.get("project_id")
        image_ids = response.get("image_ids")
        for image_id in image_ids:
            add_thumbnail(project_id=project_id,thumbnail_id=image_id)

        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        channel.basic_nack(delivery_tag=method.delivery_tag)
        print(e)

credentials = pika.PlainCredentials("user","pass")
params = pika.ConnectionParameters(host="localhost", credentials=credentials)

connection = pika.BlockingConnection(parameters=params)

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

channel.basic_consume(
    queue=QUEUE_NAME,
    on_message_callback=callback,
    auto_ack=False
)

channel.start_consuming()