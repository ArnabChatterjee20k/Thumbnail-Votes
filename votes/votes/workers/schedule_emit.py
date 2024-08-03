from celery import shared_task
from flask import jsonify
from flask_socketio import rooms
import requests
from celery.utils.log import get_task_logger
from votes import socketio
import os

logger = get_task_logger(__name__)

def get_cache():
    # Get the server's host and port from environment variables
    # You should set these in your Celery worker's environment
    server_host = os.environ.get('SERVER_HOST', 'localhost')
    server_port = os.environ.get('SERVER_PORT', '5000')
    
    # Construct the full URL
    cache_url = f"http://{server_host}:{server_port}/cache"
    response = requests.get(cache_url)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    cache = response.json()  # Assuming the response is JSON
    logger.info(f"Retrieved cache: {cache}")
    return cache

def get_rooms():
    # Get the server's host and port from environment variables
    # You should set these in your Celery worker's environment
    server_host = os.environ.get('SERVER_HOST', 'localhost')
    server_port = os.environ.get('SERVER_PORT', '5000')
    
    # Construct the full URL
    cache_url = f"http://{server_host}:{server_port}/rooms"
    response = requests.get(cache_url)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    rooms = response.json()  # Assuming the response is JSON
    logger.info(f"Retrieved rooms: {rooms}")
    return rooms
@shared_task(queue='scheduler_queue')
def emit_to_rooms():
    cache = get_cache()
    rooms = get_rooms()
    try:
        for project_id in cache:
            vote_status = {}
            for thumbnail in cache[project_id]:
                vote_status[thumbnail] = len(cache[project_id][thumbnail])
            for client in rooms.get(project_id):
                print(client)
                socketio.emit("vote_status",vote_status,to=client,callback=lambda e:print(e))
        
        return cache
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve cache: {str(e)}")
        return None