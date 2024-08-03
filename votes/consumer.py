import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika import spec

from votes.utils.vote import add_thumbnail , up_vote
import json
from votes import socketio

def thumbnail_callback(channel:BlockingChannel, method:spec.Basic.Deliver, properties, body):
    print("thumbnail")
    try:
        response = json.loads(body.decode())
        project_id = response.get("project_id")
        image_ids = response.get("image_ids")
        admin_id = response.get("admin_id")
        for image_id in image_ids:
            add_thumbnail(project_id=project_id,thumbnail_id=image_id,admin_id=admin_id)
        # channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        # channel.basic_nack(delivery_tag=method.delivery_tag) # do this with utmost knowledge what kind of exception should trigger this
        print(e)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def vote_db_callback(channel:BlockingChannel, method:spec.Basic.Deliver, properties, body):
    print("voting")
    try:
        response = json.loads(body.decode())
        user_id = response.get("user_id")
        thumbnail_id = response.get("thumbnail_id")
        project_id = response.get("project_id")
        # TODO: emit to a socket room of project_id
        # channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        # channel.basic_nack(delivery_tag=method.delivery_tag) # do this with utmost knowledge what kind of exception should trigger this
        print(e)
    # socketio.emit("message","hello",to=project_id)
    channel.basic_ack(delivery_tag=method.delivery_tag)


EXCHANGE_INFO = {
    'THUMBNAILS': {
        'type': 'direct',
        'queue': 'thumbnail_sending_queue',
        'routing_key': 'thumbnail_details',
        'callback':thumbnail_callback
    },
    'VOTES': {
        'type': 'direct',
        'queue': 'votes_sending_queue',
        'routing_key': 'vote_update',
        'callback':vote_db_callback
    }
}

def setup_exchange_queue_binding(channel:BlockingChannel, exchange, exchange_type, queue_name, routing_key,callback):
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    channel.queue_declare(queue=queue_name)
    channel.queue_bind(queue=queue_name, exchange=exchange, routing_key=routing_key)
    
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

credentials = pika.PlainCredentials("user","pass")
params = pika.ConnectionParameters(host="localhost", credentials=credentials)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

for exchange_name, exchange_info in EXCHANGE_INFO.items():
    setup_exchange_queue_binding(
        channel=channel,
        exchange=exchange_name,
        exchange_type=exchange_info['type'],
        queue_name=exchange_info['queue'],
        routing_key=exchange_info['routing_key'],
        callback=exchange_info['callback']
    )
channel.start_consuming()