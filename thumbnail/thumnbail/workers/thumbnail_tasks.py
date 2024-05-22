from celery import shared_task , group , subtask
from thumnbail.services.LLMService import LLMService

@shared_task
def generate_prompt(message) -> list[str]:
    model = LLMService()
    return model.generate_prompt(message)

@shared_task(ignore_result=True)
def generate_image(message,model_name):
    model = LLMService()
    model.generate_image(message,model_name)


@shared_task 
def map_prompt_generate_image(prompts,sub_task_to_use):
    print(prompts,sub_task_to_use)
    task = subtask(sub_task_to_use)
    
    group_task = group(
        task.clone([prompt])
        for prompt in prompts
    )
    return group_task()