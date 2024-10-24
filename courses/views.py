from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Chapter
from core.models import Klass, Subject, Level
# from courses.models import SubChapter
from MCQs.AIQuestionGenerator import get_question_from_pdf
from MCQs.models import Question
from django.conf import settings



def extract_option(s):
    # Clean the string by removing spaces and periods
    cleaned_s = s.replace(' ', '').replace('.', '')

    # Check if A, B, C, or D is in the cleaned string
    for option in ['A', 'B', 'C', 'D']:
        if option in cleaned_s.upper():
            return option
    
    # Return None if no valid option is found
    return None

@login_required
def courses(request, klass_id=None):
    if request.method == "POST":
        if "delete_chapter" in request.POST:
            chapter_id = request.POST['chapter_id']
            chapter = Chapter.objects.get(id=chapter_id)
            chapter.delete()

        elif "add_chapter" in request.POST:
            name = request.POST['name']
            level_id = request.POST['level_id']
            number = request.POST['number']
            file = request.FILES['file']

            level = Level.objects.get(id=level_id)


            chapter = Chapter(
                name=name,
                number=number,
                level=level,
                file=file,
                subject=request.user.subject
            )
            chapter.save()

            print("chapter.file.url: ", chapter.file.path)
            question = get_question_from_pdf(os.path.join(str(settings.BASE_DIR), str(chapter.file.path)))
            generated_question = Question(
                question=question[0],
                ans_a=question[1],
                ans_b=question[2],
                ans_c=question[3],
                ans_d=question[4],
                correct_ans=extract_option(question[5]),
                chapter=chapter,
            )
            generated_question.save()

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
    # "apiKey": "AIzaSyA2VYCK_i2ynmKDi7u3pRoYLQe-j_4UAyo",
    # "authDomain": "teachers-app-5dff3.firebaseapp.com",
    # "projectId": "teachers-app-5dff3",
    # "storageBucket": "teachers-app-5dff3.appspot.com",
    # "messagingSenderId": "828048730033",
    # "appId": "1:828048730033:web:3c5bfd46428729e7c03f90",
    # "measurementId": "G-3F8DFDSW8W",
    # "databaseURL": "",

    "apiKey": "AIzaSyDm0usQwaWicoqaQfCeHaH7Kn4AxGEBtyc",
    "authDomain": "autoprep-b9b7a.firebaseapp.com",
    "projectId": "autoprep-b9b7a",
    "storageBucket": "autoprep-b9b7a.appspot.com",
    "messagingSenderId": "910993355982",
    "appId": "1:910993355982:web:53ff253f4230f2369f0c9f",
    "measurementId": "G-C3NH95CH5Z",
    "databaseURL": "",

})
storage = firebase.storage()
# auth = firebase.auth()
# user= auth.sign_in_with_email_and_password('zishankadri9@gmail.com', "Firebase@1234")


# def download_file(request, sub_chapter_id):
    # sub_chapter = SubChapter.objects.get(id=sub_chapter_id)
    # download_url = sub_chapter.file_url

    # file_name = os.path.basename(uri_to_iri(urlparse(download_url).path))
    # file_name = file_name.replace("sub_chapters%2F", "", 1)

    # # Serve the file with appropriate headers
    # response = HttpResponse(content_type='application/octet-stream')
    # response['Content-Disposition'] = f'attachment; filename={file_name}'

    # # Fetch the file content directly from the storage URL
    # download_response = requests.get(download_url)
    # if download_response.status_code != 200:
    #     # Something went wrong, return an error response
    #     return 

    # response.content = download_response.content

    # return response


@login_required
@csrf_exempt
def get_chapter_list(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        klass_id = data.get('klass_id', '')

        if klass_id:
            klass = Klass.objects.get(id=klass_id)
            print(klass)
            chapter_list = list(Chapter.objects.filter(
                level=klass.level,
                subject=klass.user.subject

            ).values_list('id', 'name'))

            # chapter_list = [[x.id, x.name] for x in Chapter.objects.filter(level=klass.level,subject=klass.user.subject)]
            print(chapter_list)

            return JsonResponse({'chapterList': chapter_list}, status=200)
        else:
            return JsonResponse({'error': f'klass_id is required'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)
