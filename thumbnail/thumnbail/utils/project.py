from sqlalchemy import select, insert
from thumnbail.models import Project, Thumbnail, Workers
from thumnbail.db import Session
from thumnbail.workers import workers
from celery.result import AsyncResult


def create_project(session, email, name, message, model, count):
    project = Project(email=email, name=name, message=message,
                      count=count, model=model)
    session.add(project)
    session.flush()
    return project.id


def add_workers_to_project(session, worker_id, project_id):
    worker = Workers(worker_id=worker_id, project_id=project_id)
    session.add(worker)
    session.flush()
    return worker.id


def create_project_and_add_workers(email, name, message, model, count):
    with Session() as session:
        task_id = None
        try:
            project_id = create_project(
                session, email, name, message, model, count)
            if not project_id:
                return None
            task_id = workers.generate_image_group(
                project_id, message, model, count, email)
            generated_task = add_workers_to_project(
                session, task_id, project_id)
            session.commit()
            return project_id
        except Exception as e:
            print(e, type(e))
            session.rollback()
            task = AsyncResult(task_id)
            task.revoke(terminate=True)
            return None


def get_project(project_id):
    with Session() as session:
        query = select(Project).where(Project.id == project_id)
        project = session.execute(query).scalar_one_or_none()
        if not project:
            return None
        thumbnail_images = [image.image_id for image in project.thumbnails]
        latest_worker_id = [worker.worker_id for worker in project.workers][-1]
        workers_status = workers.get_workers_status(latest_worker_id)
        return {
            "status": workers_status,
            "title": project.name,
            "thumbnails": thumbnail_images,
            "email": project.email
        }
