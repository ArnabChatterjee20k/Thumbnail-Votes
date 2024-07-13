from flask import Blueprint, request, jsonify, send_file
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound
from thumnbail.data.sd_models import sd_models
from thumnbail.utils.project import create_project_and_add_workers, get_project
from thumnbail.utils.thumbnails import get_thumbnail_image
import io
from thumnbail.decorators.is_loggedin import is_loggedin
router = Blueprint("thumbnail_generation", __name__)

ACCEPTABLE_COUNT = 4
DEFAULT_MODEL = sd_models[0]


@router.post("/")
@is_loggedin
def generate_images():
    body = request.get_json()
    if not body:
        raise BadRequest('Request body is missing.')

    message = body.get('message')
    name = body.get("name")
    email = body.get("email")
    if not message or not name:
        raise BadRequest('message and name is required.')

    count = body.get('count', 1)
    if not isinstance(count, int) or count < 1:
        count = 1
    count = min(count, ACCEPTABLE_COUNT)

    model = body.get('model', DEFAULT_MODEL)
    if model not in sd_models:
        model = DEFAULT_MODEL

    project_id = create_project_and_add_workers(email,name, message, model, count)
    if not project_id:
        return InternalServerError("some problem occured")
    return jsonify({"project": project_id}), 201


@router.get("/<project_id>")
def project_get(project_id):
    project = get_project(project_id)
    if not project:
        return NotFound()
    return project


@router.get("/thumbnails/<thumbnail_id>")
def get_thumbnail(thumbnail_id):
    image_name,image_bytes = get_thumbnail_image(thumbnail_id)
    return send_file(io.BytesIO(image_bytes),download_name=image_name)

@router.get("/models")
def get_models():
    return {"models": sd_models}
