from django.contrib import admin
from django.conf import settings
from .models import Question, Test, CorrectAnswerList


admin.site.register(Test)
if settings.DEV_ENVIROMENT:
    admin.site.register(Question)
    admin.site.register(CorrectAnswerList)