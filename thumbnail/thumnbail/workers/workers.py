from thumnbail.workers.thumbnail_tasks import generate_image, generate_prompt, map_prompt_generate_image, save_images_to_storage, save_thumbnail_ids_to_project
from celery import chain, chord
from celery.result import AsyncResult


def generate_image_group(project_id, message, model, count,admin_id):
    # chain(task(arg),task(result_from_prev,arg))
    # here we are creating a chain of signatures

    # header is a group of task running parallely in chord. And it takes an array . So making it a chain
    header = [chain(generate_prompt.s(message, count), map_prompt_generate_image.s(
        generate_image.s(model)))]
    callback = chain(save_images_to_storage.s(),
                     save_thumbnail_ids_to_project.s(project_id,admin_id))
    """the callback will receive an structure like this
    and they are ids. Take the data from 1st index array
    nested_list = [
    ['39e05a1c-5c61-4d0e-93c6-776f957c6919', None],
    [
        ['d3de3eed-c200-4349-b173-cc500ac1e30e', None],
        None
    ],
    [
        ['144026a9-2bf1-4a8c-a965-5d2e451b2c0f', None],
        None
    ],
    [
        ['f45b40cb-4d81-4169-a365-819fcf430b74', None],
        None
    ]
]"""
    job = chord(header)(callback)

    # task_workflow = chain()
    task_ids: AsyncResult = job
    return str(task_ids.task_id)


def get_workers_status(task_id):
    return AsyncResult(task_id).state
