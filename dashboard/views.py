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
    hw_avg = Grades.objects.all().filter(assessment_type='h').aggregate(Avg('grade'))['grade__avg']
    
    quizz = Grades.objects.all().filter(assessment_type='q').aggregate(Avg('grade'))['grade__avg']
    
    mt_avg = Grades.objects.all().filter(assessment_type='m').aggregate(Avg('grade'))['grade__avg']
    

    hw_weight = 1 if (Grades.objects.all().filter(assessment_type='h').count()>0) else 0
    qz_weight = 1 if (Grades.objects.all().filter(assessment_type='q').count()>0) else 0
    mt_weight = 1 if (Grades.objects.all().filter(assessment_type='m').count()>0) else 0
    fn_weight = 1 if (Grades.objects.all().filter(assessment_type='f').count()>0) else 0
    
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'student_name':student_name,'course_name':course_name,'homework_avg':hw_avg},
    )
