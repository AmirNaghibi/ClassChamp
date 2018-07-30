from django.shortcuts import render
from .models import Student, Assessment, Course, Grades
from django.db.models import Avg
from django.views import generic

# calculate assessment avg
# assessment_types: homework=h , quiz=q , midterm=m , final=f
def assess_avg(assess_type, course_name):
    avg = 0 if (Grades.objects.all().filter(course__name=course_name,assessment_type=assess_type).count()==0) else Grades.objects.all().filter(course__name=course_name,assessment_type=assess_type).aggregate(Avg('grade'))['grade__avg']
    return avg
# calculate course weight
def assess_weight(assess_type, course_name):
    weight = 0 if (Grades.objects.all().filter(course__name=course_name,assessment_type=assess_type).count()==0) else Course.objects.all().get(name=course_name).assessment.homeworks
    return weight

# calculate avg given course name
def calculate_overall_avg(course_name):
    # average grade calculations: homework, quiz, midterm
    hw_avrg = assess_avg('h',course_name)
    qz_avrg = assess_avg('q',course_name)
    mt_avrg = assess_avg('m',course_name)
    fn_avrg = assess_avg('f',course_name)
    # weight of assessments
    hw_weight = assess_weight('h',course_name)
    qz_weight = assess_weight('q',course_name)
    mt_weight = assess_weight('m',course_name)
    fn_weight = assess_weight('f',course_name)
    # weighted average of the course based on grades achieved up to now
    overall_avg = ((hw_avrg*hw_weight)+(qz_avrg*qz_weight)+(mt_avrg*mt_weight)+(fn_avrg*fn_weight))/(hw_weight+qz_weight+mt_weight+fn_weight)
    return overall_avg

def index(request):
    """
    View function for home page of site.
    """
    student_name = Student.objects.get(last_name='naghibi').first_name
    course_name = Course.objects.get(name='CPSC317').name
    # weighted average of the course based on grades achieved up to now
    course_grade_now = calculate_overall_avg(course_name)

 
    context = {
        'student_name':student_name,
        'course_name':course_name,
        'overall_avg':round(course_grade_now,3),
    }
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context = context,
    )

class CourseListView(generic.ListView):
    model = Course
    
