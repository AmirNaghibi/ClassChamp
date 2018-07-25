from django.shortcuts import render
from .models import Student, Assessment, Course, Grades
from django.db.models import Avg

# Create your views here.

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    #!num_books=Book.objects.all().count()
    #student_name = Student.objects.get(last_name='naghibi').get_name()
    student_name = Student.objects.get(last_name='naghibi').first_name
    course_name = Course.objects.get(name='CPSC 317').name
    #assessment = Assessment.get_assessment()
    homework_avg = Grades.objects.all().filter(assessment_type='h').aggregate(Avg('grade'))['grade__avg'] #Grades.objects.filter(assessment_type__exact='h').avg()
    #!num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    #!num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    #!num_authors=Author.objects.count()  # The 'all()' is implied by default.
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'student_name':student_name,'course_name':course_name,'homework_avg':homework_avg},
    )
