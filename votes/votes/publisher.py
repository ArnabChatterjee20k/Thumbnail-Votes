import pika
import json , os
from dotenv import load_dotenv
load_dotenv('.env')
EXCHANGE_INFO = {
    'THUMBNAILS': {
        'type': 'direct',
        'queue': 'thumbnail_sending_queue',
        'routing_key': 'thumbnail_details',
    },
    'VOTES': {
        'type': 'direct',
        'queue': 'votes_sending_queue',
        'routing_key': 'vote_update',
    }
}
user = os.environ.get("VOTE_RABBITMQ_USER")
password = os.environ.get("VOTE_RABBITMQ_PASS")
host = os.environ.get("VOTE_RABBITMQ_HOST")
credentials = pika.PlainCredentials(user,password)
params = pika.ConnectionParameters(host=host, credentials=credentials)


def publish_upvote(user_id, project_id, thumbnail_id):
    connection = pika.BlockingConnection(parameters=params)
    exchange = "VOTES"
    with connection:
        channel = connection.channel()
        channel.exchange_declare(
            exchange=exchange,
            exchange_type=EXCHANGE_INFO[exchange]["type"]
        )

        channel.queue_declare(queue=EXCHANGE_INFO[exchange]["queue"])

        channel.queue_bind(
            EXCHANGE_INFO[exchange]["queue"],
            exchange,
            EXCHANGE_INFO[exchange]["routing_key"]
        )

        channel.basic_publish(
            exchange=exchange,
            routing_key=EXCHANGE_INFO[exchange]["routing_key"],
            body=json.dumps({"user_id": user_id, "thumbnail_id": thumbnail_id , "project_id":project_id})
        )