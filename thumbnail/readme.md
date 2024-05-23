### Thumbnail service

[] Creating thumbnails
[] Storing it
[] Getting thumbnails

### starting the workers

> here celery_worker is the module name and celery_app is the object
```
celery -A celery_worker.celery_app worker --loglevel INFO -P solo
```

> starting the flower service to monitor celery
```
celery --broker=amqp://user:password@localhost:5672 flower 
```

### Celery workflow getting used here for executing the tasks
![alt text](woker_chain.png)

* Basically its a chain we have created
```python
from celery import shared_task , group , subtask
from thumnbail.services.LLMService import LLMService

@shared_task
def generate_prompt(message) -> list[str]:
    pass

@shared_task(ignore_result=True)
def generate_image(message,model_name):
    pass

@shared_task 
def map_prompt_generate_image(prompts,sub_task_to_use):
    print(prompts,sub_task_to_use)
    task = subtask(sub_task_to_use)
    
    group_task = group(
        task.clone([prompt])
        for prompt in prompts
    )
    return group_task()

@shared_task
def save_images_to_storage(images: list):
    pass

header = [chain(generate_prompt.s(message, count), map_prompt_generate_image.s(
        generate_image.s(model)))]
callback = save_images_to_storage.s()
job = chord(header)(callback)
```
* The core here is that signature does not execute in themselves
* We are first generating a set of 4 prompts
* Then we have to run 4 generate_image tasks with result from generate_prompts. And each worker should be assigned only one prompt and not the whole set
* So we made another worker which takes a set of prompts and task to perform. And map prompts to workers
* Here we have created a subtask because by creating a subtask, we can clone, group, or chain tasks together in different ways to create complex task workflows.
* Now we want to save all the result in the db as a batch. So we have created a chord. The header is group for parallel tasks. So I have created a chain and put it in an array. The result flows into the callback in the form of an array of result ids.