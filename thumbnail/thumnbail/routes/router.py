from flask import Blueprint, request, abort
from thumnbail.workers import workers
from thumnbail.data.sd_models import sd_models
router = Blueprint("thumbnail_generation", __name__)


@router.post("/<user_id>")
def generate(user_id):
    body = request.json
    message = body.get("message")
    count = int(body.get("count")) if body.get("count") else 1
    ACCECPTABLE_COUNT = 4
    model_to_use = body.get("model") if body.get(
        "model") in sd_models else sd_models[0]
    if not message:
        abort(401)
    task = workers.generate_image_group(
        message, model_to_use, count % ACCECPTABLE_COUNT)

    return {"task": task}


@router.get("/models")
def get_models():
    return {"models": sd_models}
