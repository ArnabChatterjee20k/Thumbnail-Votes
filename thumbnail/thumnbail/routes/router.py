from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, InternalServerError , NotFound
from thumnbail.data.sd_models import sd_models
from thumnbail.utils.project import create_project_and_add_workers , get_project
router = Blueprint("thumbnail_generation", __name__)

ACCEPTABLE_COUNT = 4
DEFAULT_MODEL = 'stable-diffusion'


@router.post("/")
def generate_images():
    body = request.get_json()
    if not body:
        raise BadRequest('Request body is missing.')

    message = body.get('message')
    name = body.get("name")
    if not message or not name:
        raise BadRequest('message and name is required.')

    count = body.get('count', 1)
    if not isinstance(count, int) or count < 1:
        count = 1
    count = min(count, ACCEPTABLE_COUNT)

    model = body.get('model', DEFAULT_MODEL)
    if model not in sd_models:
        model = DEFAULT_MODEL

    project_id = create_project_and_add_workers(name,message,model,count)
    if not project_id:
        return InternalServerError("some problem occured")
    return jsonify({"project": project_id}), 201

@router.get("/<project_id>")
def project_get(project_id):
    project = get_project(project_id)
    if not project:
        return NotFound()
    return project

@router.get("/models")
def get_models():
    return {"models": sd_models}
