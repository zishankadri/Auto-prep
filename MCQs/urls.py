from django.contrib import admin
from django.urls import path

from . import views 
 
urlpatterns = [
    # MCQs Main Page
    path('', views.mcqs ,name="mcqs"),

    # Create New Questions
    path('create_test/<str:klass_id>/<str:test_name>/<str:no_of_questions>/<str:answer_sheet_type>/<str:is_public>/<str:chapter_id>/', views.create_test ,name="create_test"),
    path('delete_test/<str:test_id>', views.delete_test ,name="delete_test"),
    # Download the test images
    path('download_test/<str:test_id>/', views.download_test ,name="download_test"),
    
    # Upload Answer Sheets
    path('checkout_test/<str:test_id>/', views.checkout_test ,name="checkout_test"),

    # Like/Dislike a Question (APIs)
    path('like_unlike_question/', views.like_question ,name="like_question"),
    path('dislike_undislike_question/', views.dislike_question ,name="dislike_question"),

]
