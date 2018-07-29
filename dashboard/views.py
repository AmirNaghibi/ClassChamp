from django.shortcuts import render
from .models import Student, Assessment, Course, Grades
from django.db.models import Avg

# Create your views here.

def index(request):
    """
    View function for home page of site.
    """
    student_name = Student.objects.get(last_name='naghibi').first_name
    course_name = Course.objects.get(name='CPSC317').name
    # average grade calculations: homework, quiz, midterm
    hw_avrg = 0 if (Grades.objects.all().filter(course__name=course_name,assessment_type='h').count()==0) else Grades.objects.all().filter(course__name=course_name,assessment_type='h').aggregate(Avg('grade'))['grade__avg']
    qz_avrg = 0 if (Grades.objects.all().filter(course__name=course_name,assessment_type='q').count()==0) else Grades.objects.all().filter(course__name=course_name,assessment_type='q').aggregate(Avg('grade'))['grade__avg']
    mt_avrg = 0 if (Grades.objects.all().filter(course__name=course_name,assessment_type='m').count()==0) else Grades.objects.all().filter(course__name=course_name,assessment_type='m').aggregate(Avg('grade'))['grade__avg']
    fn_avrg = 0 if (Grades.objects.all().filter(course__name=course_name,assessment_type='f').count()==0) else Grades.objects.all().filter(course__name=course_name,assessment_type='f').aggregate(Avg('grade'))['grade__avg']
    # weight of assessments
    hw_weight = 0 if (Grades.objects.all().filter(course__name=course_name,assessment_type='h').count()==0) else Course.objects.all().get(name=course_name).assessment.homeworks
    qz_weight = 0 if (Grades.objects.all().filter(course__name=course_name,assessment_type='q').count()==0) else Course.objects.all().get(name=course_name).assessment.quizzes
    mt_weight = 0 if (Grades.objects.all().filter(course__name=course_name,assessment_type='m').count()==0) else Course.objects.all().get(name=course_name).assessment.midterms
    fn_weight = 0 if (Grades.objects.all().filter(course__name=course_name,assessment_type='f').count()==0) else Course.objects.all().get(name=course_name).assessment.final
    # weighted average of the course based on grades achieved up to now
    course_grade_now = ((hw_avrg*hw_weight)+(qz_avrg*qz_weight)+(mt_avrg*mt_weight)+(fn_avrg*fn_weight))/(hw_weight+qz_weight+mt_weight+fn_weight)

 
    context = {
        'student_name':student_name,
        'course_name':course_name,
        'overall_avg':round(course_grade_now,2),
    }
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context = context,
    )
