from thumnbail.workers.thumbnail_tasks import generate_image, generate_prompt, map_prompt_generate_image
from celery import group, chain


def generate_image_group(message, model,count):
    # chain(task(arg),task(result_from_prev,arg))
    # here we are creating a chain of signatures
    job = chain(generate_prompt.s(message,count), map_prompt_generate_image.s(generate_image.s(model)))

    # task_workflow = chain()
    task_ids = job.delay()
    return str(task_ids)
