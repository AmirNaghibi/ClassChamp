from django.shortcuts import render
from .models import Student, Assessment, Course, Grades
from django.db.models import Avg

# Create your views here.

def index(request):
    """
    View function for home page of site.
    """
    student_name = Student.objects.get(last_name='naghibi').first_name
    course_name = Course.objects.get(name='CPSC 317').name
    
    # average grade calculations: homework, quiz, midterm
    hw_avrg = 0 if (Grades.objects.all().filter(assessment_type='h').count()==0) else Grades.objects.all().filter(assessment_type='h').aggregate(Avg('grade'))['grade__avg']
    
    qz_avrg = 0 if (Grades.objects.all().filter(assessment_type='q').count()==0) else Grades.objects.all().filter(assessment_type='q').aggregate(Avg('grade'))['grade__avg']
    
    mt_avrg = 0 if (Grades.objects.all().filter(assessment_type='m').count()==0) else Grades.objects.all().filter(assessment_type='m').aggregate(Avg('grade'))['grade__avg']

    fn_avrg = 0 if (Grades.objects.all().filter(assessment_type='f').count()==0) else Grades.objects.all().filter(assessment_type='f').aggregate(Avg('grade'))['grade__avg']
    
    # determine if we need to use the weight of an assessment
    hw_presence = 1 if (Grades.objects.all().filter(assessment_type='h').count()>0) else 0
    qz_presence = 1 if (Grades.objects.all().filter(assessment_type='q').count()>0) else 0
    mt_presence = 1 if (Grades.objects.all().filter(assessment_type='m').count()>0) else 0
    fn_presence = 1 if (Grades.objects.all().filter(assessment_type='f').count()>0) else 0

    # weight of assessments
    hw_weight = Assessment.objects.all().get(course_name='cpsc 317').homeworks
    qz_weight = Assessment.objects.all().get(course_name='cpsc 317').quizzes
    mt_weight = Assessment.objects.all().get(course_name='cpsc 317').midterms
    fn_weight = Assessment.objects.all().get(course_name='cpsc 317').final

    course_grade_now = ((hw_avrg*hw_weight)+(qz_presence*qz_avrg*qz_weight)+(mt_avrg*mt_weight)+(fn_presence*fn_avrg*fn_weight))/((hw_weight*hw_presence)+(qz_weight*qz_presence)+(mt_weight*mt_presence)+(fn_weight*fn_presence))
    # course_grade_now = ((hw_avrg*hw_weight)+(mt_avrg*mt_weight))/((hw_weight*hw_presence)+(mt_weight*mt_presence))

 
    
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'student_name':student_name,'course_name':course_name,'homework_avg':round(course_grade_now,2)},
    )
