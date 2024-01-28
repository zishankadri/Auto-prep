from django.contrib import admin

from .models import Student, Klass, Level, Subject, Faq


# admin.site.register(Student)
# admin.site.register(Klass)
admin.site.register(Level)
admin.site.register(Subject)
admin.site.register(Faq)
