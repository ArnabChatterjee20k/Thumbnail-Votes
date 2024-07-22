from celery import shared_task
from flask import jsonify
import requests
from celery.utils.log import get_task_logger
from votes import socketio
import os

logger = get_task_logger(__name__)

@shared_task(queue='scheduler_queue')
def emit_to_rooms():
    # Get the server's host and port from environment variables
    # You should set these in your Celery worker's environment
    server_host = os.environ.get('SERVER_HOST', 'localhost')
    server_port = os.environ.get('SERVER_PORT', '5000')
    
    # Construct the full URL
    cache_url = f"http://{server_host}:{server_port}/cache"
    
    try:
        response = requests.get(cache_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        cache = response.json()  # Assuming the response is JSON
        logger.info(f"Retrieved cache: {cache}")
        
        for room in cache:
            vote_status = {}
            for thumbnail in cache[room]:
                vote_status[thumbnail] = len(cache[room][thumbnail])
            
            socketio.emit("vote_status",jsonify(vote_status),room=room)
        
        return cache
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve cache: {str(e)}")
        return None