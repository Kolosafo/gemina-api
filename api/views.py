from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
# from django.contrib.auth.models import User
from account.models import User
from .models import LessonObject, Course, Curriculum,SubjectLesson
from rest_framework.permissions import IsAuthenticated
from . serializers import LessonObjectSerializer, CourseSerializer, CurriculumSerializer
import time

# Create your views here.



@api_view(['GET'])
def pulse_check(request):
    
    return Response("Okay!", status=status.HTTP_200_OK)  # Use 201 for creation
    
  
  
@api_view(['GET'])
def get_all_lesson_objects(request):
    all_lessons = LessonObject.objects.all()
    serializer = LessonObjectSerializer(all_lessons, many=True)
    return Response(
                {
                    'message': 'success',
                    'data': serializer.data,
                    'status': "success",
                    'error': "none"
                },
                status=status.HTTP_200_OK
            )
    

# COURSE VIEW OBJECTS 
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_user_courses(request):
    fetch_user = request.user
    response_obj = []
    all_user_courses = Course.objects.filter(user = fetch_user).order_by('-created_at')
    for course in all_user_courses:
        get_all_course_curriculum = Curriculum.objects.filter(course_obj = course).order_by('id')
        # print("USER COURSES: ",{'course': CourseSerializer(course).data, 'curriculum':CurriculumSerializer(get_all_course_curriculum, many =True).data })
        response_obj.append({'course': CourseSerializer(course).data, 'curriculum':CurriculumSerializer(get_all_course_curriculum, many =True).data})
        
    return Response(
        {
            'message': 'success',
            'data': response_obj,
            'status': "success",
            'error': "none"
        },
        status=status.HTTP_200_OK
    )
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_courses(request):
    auth_user = request.user
    # CHECK IF COURSE ALREADY EXISTS
    data = request.data
    if Course.objects.filter(user=auth_user, subject=data['subject']):
        return Response("You have already started learning this course", status=status.HTTP_409_CONFLICT)
    data['user'] = auth_user.id
    serializer = CourseSerializer(data=data)
    if serializer.is_valid():
        try:
            serializer.save(user=auth_user)
            # all_user_courses = Course.objects.filter(user = auth_user)
            # courses_serializer = CourseSerializer(all_user_courses, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])    
def add_curriculm_to_course(request):
    subject = request.data['subject']
    user = request.user
    
    get_course = Course.objects.get(user=user, subject=subject)


# CURRICULUM VIEW OBJECTS 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course_curriculum(request): # THIS SHOULD BE AN ARRAY OF COURSE CURRICULUMS
    auth_user = request.user
    curriculum_list = request.data
    response_object = []
    try:
        for curriculum in curriculum_list:
            serializer = CurriculumSerializer(data=curriculum)
            get_parent_course = Course.objects.get(id=curriculum['course_obj'])
            curriculum['course_obj'] = get_parent_course.id
            if serializer.is_valid():
                    serializer.save(user=auth_user)
                    response_object.append(serializer.data)
            else:
                # Return validation errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_object, status=status.HTTP_201_CREATED) 
    
    except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_course_curriculum(request):
    # time.sleep(10)
    parent_course_id = request.data['course_id']
    get_parent_course = Course.objects.get(id=parent_course_id)
    course_curriculum = Curriculum.objects.filter(course_obj = get_parent_course).order_by('id')
    try:
        serializer = CurriculumSerializer(course_curriculum, many = True)
        return Response({"data":serializer.data, "status" : status.HTTP_200_OK, "message": "success"}) 
    except Exception as E:
        return Response({"data":None, "status" : status.HTTP_400_BAD_REQUEST, "message": str(E)})
    
    
    
# LESSON VIEW OBJECTS 

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_lesson(request): 
    user = request.user
    data = request.data
    course = Course.objects.get(id=data['course'])    
    subject_lesson = SubjectLesson.objects.get(id=data['parent_subject_lesson'])    
    subject_lesson.isLesson_completed = True
    data['course'] = course.pk
    data['parent_subject_lesson'] = subject_lesson.pk
    serializer = LessonObjectSerializer(data=data)
    if serializer.is_valid():
        try:
            print("THIS WORKS!")
            serializer.save(user=user)
            subject_lesson.save()
            serializer_object = serializer.data
            serializer_object['course'] = { 
                'id': course.id,
                'user': course.user.id,
                'user_email': course.user.email,
                'subject': course.subject,
                'isCourse_completed': course.isCourse_completed,
            }
            return Response(serializer_object, status=status.HTTP_201_CREATED) 
        except Exception as e:
            print("ERROR: ", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Return validation errors
        print("SERIALIZER ERROR: ", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_lesson(request):
    data = request.data
    get_parent_course = Course.objects.get(id=data['course_id'])
    get_parent_subject_lesson = SubjectLesson.objects.get(id=data['parent_subject_lesson'])
    try:
        lesson = LessonObject.objects.get(course = get_parent_course, parent_subject_lesson = get_parent_subject_lesson)
        serializer = LessonObjectSerializer(lesson)
        return Response({"data":serializer.data, "status" : status.HTTP_200_OK, "message": "success"}) 
    except Exception as E:
        return Response({"data":None, "status" : status.HTTP_400_BAD_REQUEST, "message": "An Unknown Error occurred"})
  
  
  
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def calculate_course_complete_percentage(request):
#     get_parent_course = Course.objects.get(id=data['course_id'])
#     get_all_curriculum_under_course = Curriculum.objects.filter(course_obj = get_parent_course)
#     curriculum_lesson_length = None
#     for curriculum in get_all_curriculum_under_course:
#         curriculum_lesson_length = len(curriculum.lessons)
#     data = request.data
#     curriculum = Curriculum.objects.get(id=data['curriculum_id'])
#     curriculum.isSection_completed = True
#     curriculum.save()
#     return Response("success") 
    
    