from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home ,name="home"),

    path('payment/', views.payment_page, name="payment"),
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('payment_successful/', views.payment_successful_view, name="payment_successful"),
    path('payment_failed/', views.payment_failed_view, name="payment_failed"),

    path('classes/', views.classes ,name="classes"),
    path('classes/<str:klass_id>/', views.classes ,name="classes"),
    path('create_class/', views.create_class ,name="create_class"),
    
    # APIs
    path('update_klass/', views.update_klass, name='update_klass'),
    path('update_student/', views.update_student, name='update_student'),
    path('update_student_grade/', views.update_student_grade, name='update_student_grade'),
    path('delete_student/', views.delete_student, name='delete_student'),

    # CGV URL
    path('cgv/', views.cgv, name="cgv")
    
]
