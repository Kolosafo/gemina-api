from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


app_name = 'api'
urlpatterns = [
    # url path to get posts
    path('test/',
         views.pulse_check, name="test"),
    path('all_lessons/', views.get_all_lesson_objects, name="all_lessons"),
    path('get_user_courses/', views.get_user_courses, name="get_user_courses"),
    path('create_course/', views.create_courses, name="create_course"),
    path('create_course_curriculum/', views.create_course_curriculum, name="create_course_curriculum"),
    path('get_course_curriculum/', views.get_course_curriculum, name="get_course_curriculum"),
    path('create_lesson/', views.create_lesson, name="create_lesson"),
    path('get_lesson/', views.get_lesson, name="get_lesson"),
    path('create_quick_learn/', views.create_quick_learn, name="create_quick_learn"),
    path('get_user_quick_learns/', views.get_user_quick_learns, name="get_user_quick_learns"),
    path('get_single_quick_learn/', views.get_single_quick_learn, name="get_single_quick_learn"),
    path('update_quick_learn/', views.update_quick_learn, name="update_quick_learn"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
