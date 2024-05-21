from celery import shared_task
from celery.signals import task_failure , task_success ,task_postrun , task_prerun
from thumnbail.services.LLMService import LLMService

@shared_task
def generate_image(message):
    model = LLMService()
    model.generate_image(message)