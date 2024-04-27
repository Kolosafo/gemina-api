from django.contrib.auth.models import  AbstractUser
from .managers import UserManager
from django.db import models


SchoolLevelChoices  = (
    ("high school", "high school"),
    ("middle school", "middle school"),
)

GenderChoices  = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Prefer not to say", "Prefer not to say"),
)


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=200, blank=True, null = True)
    profile_picture = models.CharField(max_length=500, blank=True, null = True)
    last_name = models.CharField(max_length=200, blank=True, null = True)
    gender = models.CharField(choices=GenderChoices, max_length=200, blank=True, null = True)
    DOB = models.DateField(blank=True, null = True)
    school_level = models.CharField(choices=SchoolLevelChoices, max_length=200, blank=True, null = True)
    grade_level = models.IntegerField( blank=True, null = True)
    country = models.CharField(max_length=300, blank=True, null = True)
    date_joined = models.DateTimeField(auto_now_add = True, blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
