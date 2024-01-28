from django.shortcuts import render

from .models import Chapter
from core.models import Klass, Subject
from courses.models import SubChapter

def courses(request, klass_id=None):
    klasses = Klass.objects.filter(user=request.user)
    
    context = {
        'klasses': klasses,
    }

    if klass_id:
        klass = Klass.objects.get(id=klass_id)
        # chapters = Chapter.objects.filter(level=klass.level)
        chapters = Chapter.objects.filter(level=klass.level, subject=request.user.subject)
        context['chapters'] = chapters
        context['klass'] = klass

        # return render(request, "courses/select_chapter.html", context)

    return render(request, "courses/select_class.html", context)
    

from django.views import View
from django.http import HttpResponse
import requests

import pyrebase

firebase = pyrebase.initialize_app({
    "apiKey": "AIzaSyA2VYCK_i2ynmKDi7u3pRoYLQe-j_4UAyo",
    "authDomain": "teachers-app-5dff3.firebaseapp.com",
    "projectId": "teachers-app-5dff3",
    "storageBucket": "teachers-app-5dff3.appspot.com",
    "messagingSenderId": "828048730033",
    "appId": "1:828048730033:web:3c5bfd46428729e7c03f90",
    "measurementId": "G-3F8DFDSW8W",
    "databaseURL": "",
})
storage = firebase.storage()
auth = firebase.auth()
user= auth.sign_in_with_email_and_password('zishankadri9@gmail.com', "Firebase@1234")


def download_file(request, sub_chapter_id):
    sub_chapter = SubChapter.objects.get(id=sub_chapter_id)
    download_url = sub_chapter.file_url
    file_name = sub_chapter.name
    # Serve the file with appropriate headers
    response = HttpResponse(content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    # Fetch the file content directly from the storage URL
    response.content = requests.get(download_url).content

    return response