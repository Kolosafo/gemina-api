from django.db import models
from django.conf import settings
from django.db.models import Manager

# Create your models here.

class CurriculumManager(Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('lessons').order_by('lessons__id')

LessonOptionChoices  = (
    ("options", "options"),
    ("input", "input"),
)
LessonTypeChoices  = (
    ("lesson", "lesson"),
    ("quiz", "quiz"),
)


class LessonDetails(models.Model):
  title = models.CharField(max_length=500)
  details = models.TextField(blank=True, null=True)
  image = models.ImageField(upload_to="uploads/", blank=True, null=True)
  question = models.CharField(max_length=1000, null=True, blank=True)
  answerType = models.CharField(max_length=1000, choices=LessonOptionChoices, null=True, blank=True) 
  options = models.JSONField(null=True, blank=True)
  answer = models.CharField(max_length=1000, null=True, blank=True)
  type = models.CharField(max_length=1000, null=True, blank=True, choices=LessonTypeChoices)
  timeout = models.IntegerField(null=True, blank=True)
  isComplete = models.BooleanField(default=False)

  def __str__(self):
    return self.title
  class Meta:
        verbose_name = 'Lesson Detail'
        

  



# /////// CURRICULUM MODELS
LearningTypeChoices  = (
    ("text", "text"),
    ("auditory", "auditory"),
    ("interactive", "interactive"),
)


class SubjectLesson(models.Model):
  title = models.CharField(max_length=500)
  isLesson_completed = models.BooleanField(default=False)
  exercise = models.CharField(max_length=500, blank=True, null=True)
  learning_type = models.CharField(max_length=500, blank=True, null=True, choices=LearningTypeChoices, default="interactive")
  def __str__(self):
    return self.title


class Course(models.Model):
  user= models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  subject = models.CharField(max_length=500)
  isCourse_completed = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add = True, blank=True, null=True)
  
  def __str__(self):
    return self.subject
  
  
class Curriculum(models.Model):
  course_obj = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="parent_course")
  section_title = models.CharField(max_length=500)
  lessons = models.ManyToManyField(SubjectLesson, related_name="curriculum_lessons")
  exercise = models.CharField(max_length=500, blank=True, null=True)
  learning_type = models.CharField(max_length=500)
  isSection_completed = models.BooleanField(default=False)
  objects = CurriculumManager()
  def __str__(self):
    return self.section_title
  

  
  # /// LESSON OBJECT
  
class LessonObject(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name="course_curriculum")
  parent_subject_lesson = models.ForeignKey(SubjectLesson, on_delete=models.CASCADE, blank=True, null=True, related_name="parent_subject_lesson")
  lesson_title = models.CharField(max_length=500)
  lesson_slug = models.CharField(max_length=500)
  lesson_id = models.CharField(max_length=500)
  lesson_details = models.ManyToManyField(LessonDetails, related_name="lesson_details", blank=True, null=True) 
  def __str__(self):
    return f"{self.course.subject}: {self.lesson_title}"