from django.contrib import admin
from .models import LessonDetails, LessonObject, SubjectLesson, Curriculum, Course, QuickLearn
# Register your models here.
admin.site.register(LessonDetails)
admin.site.register(LessonObject)
admin.site.register(SubjectLesson)
admin.site.register(Curriculum)
admin.site.register(Course)
admin.site.register(QuickLearn)

