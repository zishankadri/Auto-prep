from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Chapter
from core.models import Klass, Subject
from courses.models import SubChapter

@login_required
def courses(request, klass_id=None):
    klasses = Klass.objects.filter(user=request.user)
    
    context = {
        'klasses': klasses,
    }

    if klass_id:
        klass = Klass.objects.get(id=klass_id)
        
        chapters = Chapter.objects.filter(
            level=klass.level,
            subject=request.user.subject,
        ).order_by("number")

        context['chapters'] = chapters
        context['klass'] = klass

        # return render(request, "courses/select_chapter.html", context)

    return render(request, "courses/select_class.html", context)
    

from django.http import HttpResponse
from django.utils.encoding import uri_to_iri
from urllib.parse import urlparse
from django.http import JsonResponse

import requests
import os
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

    file_name = os.path.basename(uri_to_iri(urlparse(download_url).path))
    file_name = file_name.replace("sub_chapters%2F", "", 1)

    # Serve the file with appropriate headers
    response = HttpResponse(content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    # Fetch the file content directly from the storage URL
    download_response = requests.get(download_url)
    if download_response.status_code != 200:
        # Something went wrong, return an error response
        return 

    response.content = download_response.content

    return response