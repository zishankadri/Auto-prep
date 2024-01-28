from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

import pyrebase


# import io
# from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
import os


@deconstructible
class FirebaseStorage(Storage):
    def __init__(self):
        config = {
            "apiKey": "AIzaSyA2VYCK_i2ynmKDi7u3pRoYLQe-j_4UAyo",
            "authDomain": "teachers-app-5dff3.firebaseapp.com",
            "projectId": "teachers-app-5dff3",
            "storageBucket": "teachers-app-5dff3.appspot.com",
            "messagingSenderId": "828048730033",
            "appId": "1:828048730033:web:3c5bfd46428729e7c03f90",
            "measurementId": "G-3F8DFDSW8W",
            "databaseURL": "",
        }

        self.firebase = pyrebase.initialize_app(config)
        self.storage = self.firebase.storage()

    def _open(self, name, mode='rb'):
        # Implement if needed
        pass

    def _save(self, name, content):

        content_data = content.read()
        # content_io = io.BytesIO(content_data)
        # self.storage.child(name).put(/home/zishan/Desktop/Fiverr/Teachers app/project/Dockerfile)

        self.storage.child(name).put(content)

        print("_--------------------------")
        print("name: ", name)
        print("content: ", content, "type: ", type(content))
        print("_--------------------------")

        return name

    def my_url(self, name):
        # Return the URL of the file in Firebase Storage
        return self.storage.child(name).get_url(None)

    def exists(self, name):
        # Check if a file with the given name exists in Firebase Storage
        try:
            self.storage.child(name).get_metadata()
            return True
        except:
            return False