from celery import shared_task, group, subtask
from thumnbail.services.LLMService import LLMService
from thumnbail.services.UploadService import UploadService
from celery.result import AsyncResult
import json


@shared_task(ignore_result=False)
def generate_prompt(message, count) -> list[str]:
    model = LLMService()
    return model.generate_prompt(message, count)


@shared_task(ignore_result=False)
def generate_image(message, model_name):
    model = LLMService()
    filename = model.generate_image(message, model_name)
    return filename


@shared_task
def map_prompt_generate_image(prompts, sub_task_to_use):
    print(prompts, sub_task_to_use)
    task = subtask(sub_task_to_use)

    group_task = group(
        task.clone([prompt])
        for prompt in prompts
    )
    return group_task()


@shared_task
def save_images_to_storage(images: list):
    """
    it will receive an structure like this
    [
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
]
"""
    storage = UploadService()
    def get_ids(data):
        ids = []

        def traverse(data):
            if isinstance(data, list):
                for element in data:
                    traverse(element)

            if isinstance(data, str):
                ids.append(data)

        traverse(data)
        return ids
    logs = json.dumps(images)

    result_ids = get_ids(images)[1:] # as the first id is of no use

    for result_id in result_ids:
        image = AsyncResult(result_id).result
        storage.upload(image)