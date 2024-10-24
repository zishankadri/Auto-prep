from django.db import models
import pyrebase

# firebase = pyrebase.initialize_app({
#     "apiKey": "AIzaSyA2VYCK_i2ynmKDi7u3pRoYLQe-j_4UAyo",
#     "authDomain": "teachers-app-5dff3.firebaseapp.com",
#     "projectId": "teachers-app-5dff3",
#     "storageBucket": "teachers-app-5dff3.appspot.com",
#     "messagingSenderId": "828048730033",
#     "appId": "1:828048730033:web:3c5bfd46428729e7c03f90",
#     "measurementId": "G-3F8DFDSW8W",
#     "databaseURL": "",
# })
# storage = firebase.storage()
# auth = firebase.auth()
# user= auth.sign_in_with_email_and_password('zishankadri9@gmail.com', "Firebase@1234")

class Chapter(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField()
    file = models.FileField(upload_to="chapters/", max_length=100)

    subject = models.ForeignKey("core.Subject", on_delete=models.CASCADE)
    level = models.ForeignKey("core.Level", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    # def get_url(self):
    #     # Convert the URL for direct download with fl_attachment
    #     print(self.file.url)
    #     base_url = self.file.url.split('/upload/')[0]  # Get the base URL before /upload/
    #     file_path = self.file.url.split('/upload/')[1]  # Get the file path after /upload/

    #     # Construct the new URL with fl_attachment
    #     converted_url = f"{base_url}/upload/fl_attachment:{self.name}/{file_path}"

    #     return converted_url
