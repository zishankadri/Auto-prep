from django.contrib import admin
from django.urls import path

from . import views 

urlpatterns = [
    path('download-file/<str:sub_chapter_id>/', views.download_file, name='download_file'),
    path('', views.courses ,name="courses"),
    path('<str:klass_id>/', views.courses ,name="courses"),
    # path('<str:level>/<str:chapter>', views.courses ,name="courses"),

]
