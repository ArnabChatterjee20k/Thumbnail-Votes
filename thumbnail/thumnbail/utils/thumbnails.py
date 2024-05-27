from thumnbail.models import Thumbnail
from thumnbail.db import Session


def save_thumbnails(project_id, thumbnail_ids: list[str]):
    with Session() as session:
        thumbnails = [Thumbnail(image_id=image_id, project_id=project_id)
                      for image_id in thumbnail_ids]
        session.add_all(thumbnails)
        session.commit()
