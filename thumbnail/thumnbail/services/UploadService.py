from pymongo import MongoClient
import gridfs
from thumnbail.utils.generate_random_name import generate_random_name
import os
class UploadService():
    def __init__(self):
        self.storage = self.__get_storage()
    def __get_storage(self):
        url = os.environ.get("MONGODB_URI")
        db = MongoClient(url).gridfs_example
        fs = gridfs.GridFS(db)
        return fs

    def upload(self,image:bytes,**metadata):
        name = generate_random_name()
        file_id = self.storage.put(image,filename=f"{name}.png",**metadata)
        return file_id