from django.shortcuts import render
from .models import Student, Evaluation, Course, Grades
from django.db.models import Avg
from django.views import generic

# calculate evaluation avrg
# evaluation_types: homework=h , quiz=q , midterm=m , final=f
def evaluation_avrg(evaluation_type, course_name):
    avrg = 0 if (Grades.objects.all().filter(course__name=course_name,evaluation_type=evaluation_type).count()==0) else Grades.objects.all().filter(course__name=course_name,evaluation_type=evaluation_type).aggregate(Avg('grade'))['grade__avg']
    return avrg
# calculate course weight
def evaluation_weight(evaluation_type, course_name):
    if evaluation_type=='h':
        return 0 if (Grades.objects.all().filter(course__name=course_name,evaluation_type=evaluation_type).count()==0) else Course.objects.get(name=course_name).evaluation.homeworks
    elif evaluation_type=='q':
        return 0 if (Grades.objects.all().filter(course__name=course_name,evaluation_type=evaluation_type).count()==0) else Course.objects.get(name=course_name).evaluation.quizzes
    elif evaluation_type=='m':
        return 0 if (Grades.objects.all().filter(course__name=course_name,evaluation_type=evaluation_type).count()==0) else Course.objects.get(name=course_name).evaluation.midterms
    else:
        return 0 if (Grades.objects.all().filter(course__name=course_name,evaluation_type=evaluation_type).count()==0) else Course.objects.get(name=course_name).evaluation.final

      
# calculate avrg given course name
def course_overall_avrg(course_name):
    # average grade calculations: homework, quiz, midterm
    hw_avrg = evaluation_avrg('h',course_name)
    qz_avrg = evaluation_avrg('q',course_name)
    mt_avrg = evaluation_avrg('m',course_name)
    fn_avrg = evaluation_avrg('f',course_name)
    # weight of evaluations
    hw_weight = evaluation_weight('h',course_name)
    qz_weight = evaluation_weight('q',course_name)
    mt_weight = evaluation_weight('m',course_name)
    fn_weight = evaluation_weight('f',course_name)
    # weighted average of the course based on grades achieved up to now
    overall_avrg = ((hw_avrg*hw_weight)+(qz_avrg*qz_weight)+(mt_avrg*mt_weight)+(fn_avrg*fn_weight))/(hw_weight+qz_weight+mt_weight+fn_weight)
    return round(overall_avrg,2)

# calculate avrg for all courses
def term_overall_avrg():
    course_averages = []
    for course in Course.objects.all():
        course_averages.append(course_overall_avrg(course.name))
    total = 0
    for grade in course_averages:
        total += grade
    return round(total/len(course_averages),2)

def index(request):
    """
    View function for home page of site.
    """
    student_name = Student.objects.get(last_name='naghibi').first_name
    course_name = Course.objects.get(name='MATH200').name
    # weighted average of the course based on grades achieved up to now
    course_grade_now = course_overall_avrg(course_name)

 
    context = {
        'student_name':student_name,
        'course_name':course_name,
        'overall_avrg':course_grade_now,
    }
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context = context,
    )

def coursePage(request):
    course_list = Course.objects.all()
    course_avrg = {}
    for course in course_list:
        course_avrg[course.name]=course_overall_avrg(course.name)
    context = {
        'term_avrg':term_overall_avrg(),
        'course_avrg':course_avrg,
    }

    return render(
        request,
        'courses.html',
        context = context,
    )



