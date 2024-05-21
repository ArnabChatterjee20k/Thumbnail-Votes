from flask import Blueprint ,request , abort
from thumnbail.workers import workers
router = Blueprint("thumbnail_generation",__name__)

@router.post("/<user_id>")
def generate(user_id):
    body = request.json
    message = body.get("message")
    if not message:
        abort(401)
    task = workers.generate_image.delay(message)


    return {"task":str(task)}