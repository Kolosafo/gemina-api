from rest_framework import serializers
from .models import LessonObject, LessonDetails, Curriculum, Course, SubjectLesson, QuickLearn



# /////// CURRICULUM MODELS

class SubjectLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectLesson
        fields = '__all__'
        
class CurriculumSerializer(serializers.ModelSerializer):
    lessons =  SubjectLessonSerializer(many=True)
    class Meta:
        model = Curriculum
        fields = '__all__'
    
    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons')  # Extract lesson details
        course_curriculim = Curriculum.objects.create(
            course_obj=validated_data['course_obj'],
            section_title=validated_data['section_title'],
            learning_type=validated_data['learning_type'],
        )
        for lesson_detail_data in lessons_data:
            lesson_detail = SubjectLesson.objects.create(**lesson_detail_data)  # Create lesson detail
            course_curriculim.lessons.add(lesson_detail)  # Add detail to lesson's M2M field 
        return course_curriculim
    
    

class QuickLearnSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickLearn
        fields = '__all__'
        
        
        

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        
        
        
# /////// LESSON MODELS

class LessonDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonDetails
        fields = '__all__'

class LessonObjectSerializer(serializers.ModelSerializer):
    # subject = CourseSerializer(read_only=True)
    lesson_details = LessonDetailsSerializer(many=True)

    class Meta:
        model = LessonObject
        fields = '__all__'
        

    def create(self, validated_data):
        lesson_details_data = validated_data.pop('lesson_details')  # Extract lesson details
        lesson = LessonObject.objects.create(
            course=validated_data['course'],
            lesson_title=validated_data['lesson_title'],
            lesson_slug=validated_data['lesson_slug'],
            lesson_id=validated_data['lesson_id'],
            parent_subject_lesson=validated_data['parent_subject_lesson'],
        )
        for lesson_detail_data in lesson_details_data:
            lesson_detail = LessonDetails.objects.create(**lesson_detail_data)  # Create lesson detail
            lesson.lesson_details.add(lesson_detail)  # Add detail to lesson's M2M field 
        return lesson



