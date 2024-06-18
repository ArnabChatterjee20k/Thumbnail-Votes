from thumnbail.models import Thumbnail
from thumnbail.db import Session
from sqlalchemy import select

from thumnbail.services.UploadService import UploadService

def save_thumbnails(project_id, thumbnail_ids: list[str]):
    with Session() as session:
        thumbnails = [Thumbnail(image_id=image_id, project_id=project_id)
                      for image_id in thumbnail_ids]
        session.add_all(thumbnails)
        session.commit()

def get_thumbnail_image(thumbnail_id):
    storage = UploadService()
    with Session() as session:
        query = select(Thumbnail.image_id).where(Thumbnail.image_id ==thumbnail_id)
        image_id = session.execute(query).scalar_one()
        image = storage.get(image_id)
        return image.filename,image.read()