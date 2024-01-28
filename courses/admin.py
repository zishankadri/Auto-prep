from django.contrib import admin

from .models import Chapter, SubChapter
from django import forms

class SubChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'chapter':
            # Filter the Chapter dropdown based on subject and level
            subject_id = request.GET.get('chapter__subject__id')
            level_id = request.GET.get('chapter__level__id')

            if subject_id and level_id:
                kwargs['queryset'] = kwargs['queryset'].filter(subject_id=subject_id, level_id=level_id)
                
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Chapter)
admin.site.register(SubChapter, SubChapterAdmin)
# admin.site.register(SubChapter)