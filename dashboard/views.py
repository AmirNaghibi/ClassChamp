from django.shortcuts import render, redirect
from .models import *
from django.db.models import Avg
from django.views import generic
# class to create form based on models
from . import forms
from django.http import HttpResponseRedirect, HttpResponse

# calculate evaluation avrg
# evaluation_types: homework=h , quiz=q , midterm=m , final=f
def evaluation_avrg(evaluation_type, course_name):
    avrg = 0 if (Grades.objects.all().filter(course__name=course_name,evaluation_type=evaluation_type).count()==0) else Grades.objects.all().filter(course__name=course_name,evaluation_type=evaluation_type).aggregate(Avg('grade'))['grade__avg']
    return avrg


# calculate course weight
def evaluation_weight(evaluation_type, course_name):
    if evaluation_type=='h':
        return 0 if (Grades.objects.all().filter(course__name=course_name,evaluation_type=evaluation_type).count()==0) else Course.objects.get(name=course_name).homeworks
    elif evaluation_type=='q':
        return 0 if (Grades.objects.all().filter(course__name=course_name,evaluation_type=evaluation_type).count()==0) else Course.objects.get(name=course_name).quizzes
    elif evaluation_type=='m':
        return 0 if (Grades.objects.all().filter(course__name=course_name,evaluation_type=evaluation_type).count()==0) else Course.objects.get(name=course_name).midterms
    else:
        return 0 if (Grades.objects.all().filter(course__name=course_name,evaluation_type=evaluation_type).count()==0) else Course.objects.get(name=course_name).final

      
# calculate avrg given course name
def course_overall_avrg(course_name):
    # average grade calculations: homework, quiz, midterm
    if Grades.objects.filter(course__name=course_name):
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
    else:
        return 0


# calculate avrg for all courses
def term_overall_avrg():
    if Course.objects.all().count() != 0:
        course_averages = []
        for course in Course.objects.all():
            course_averages.append(course_overall_avrg(course.name))
        total = 0
        for grade in course_averages:
            total += grade
        return round(total/len(course_averages),2)
    else:
        return 0


def index(request):
    """
    View function for home page of site.
    """
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
    )


def coursesPage(request):
    if Course.objects.all().count() != 0:
        course_list = Course.objects.all()
        course_avrg = {}
        for course in course_list:
            course_avrg[course]=course_overall_avrg(course.name)
        context = {
            'term_avrg':term_overall_avrg(),
            'course_avrg':course_avrg,
        }
        return render(
            request,
            'courses.html',
            context = context,
        )
    else:
            return render(
            request,
            'courses.html',
        )
        


def course_detail_view(request, pk):
    try:
        course = Course.objects.get(id=pk)
        course_name = course.name
        course_avrg = course_overall_avrg(course.name)
        course_evaluation_grades = {
            'homeworks': evaluation_avrg('h',course.name),
            'quizzes': evaluation_avrg('q',course.name),
            'midterms': evaluation_avrg('m',course.name),
            'final': evaluation_avrg('f',course.name),
        }
        context = {
            'course':course,
            'course_avrg':course_avrg,
            'course_evaluation_grades':course_evaluation_grades,
        }
    except Course.DoesNotExist:
        raise Http404('Course does not exist')
    return render(
        request, 
        'course_detail.html', 
        context=context,
    )


def grades_detail_view(request,pk):
    try:
        course = Course.objects.get(id=pk)
        course_name = course.name
        course_avrg = course_overall_avrg(course.name)
        course_homework_grades = Grades.objects.filter(course__name=course_name,evaluation_type="h")
        course_quizz_grades = Grades.objects.filter(course__name=course_name,evaluation_type="q")
        course_midterm_grades = Grades.objects.filter(course__name=course_name,evaluation_type="m")
        course_final_grades = Grades.objects.filter(course__name=course_name,evaluation_type="f")
        context = {
            'course_name':course_name,
            'course_avrg':course_avrg,
            'course_homework_grades':course_homework_grades,
            'course_quizz_grades':course_quizz_grades,
            'course_midterm_grades':course_midterm_grades,
            'course_final_grades':course_final_grades,
        }
    except Course.DoesNotExist:
        raise Http404('Grades do not exist')
    return render(
        request, 
        'grades_detail.html', 
        context=context,
    )

def is_valid_grade(grade):
    if grade in range(0,101):
        return True
    else:
        return False

# Add course tab
def add_course(request):
    if request.method == 'POST':
        form = forms.AddCourse(request.POST)
        if form.is_valid():
            homeworks = int(form.cleaned_data['homeworks'])
            quizzes = int(form.cleaned_data['quizzes'])
            midterms = int(form.cleaned_data['midterms'])
            final = int(form.cleaned_data['final'])
            if int(form.cleaned_data['homeworks'])+int(form.cleaned_data['quizzes'])+int(form.cleaned_data['midterms'])+int(form.cleaned_data['final'])!=100:
                return render(
                request,
                'error_page.html',
                context={'msg':"sum of evaluations must be 100"},
                )
            elif (not is_valid_grade(homeworks) or not is_valid_grade(quizzes) or not is_valid_grade(midterms) or not is_valid_grade(final)):
                return render(
                    request,
                    'error_page.html',
                    context={'msg':"Graded must be integers in range 0 to 100"},
                )
            else:
            # Successful save on db
                form.save()
                msg = "successfully create course "+form.cleaned_data['name']
                return render(
                    request,
                    'error_page.html',
                    context={
                        'msg':msg,
                    },
                )
    else:
        form = forms.AddCourse()

    context = {
        'form':form,
    }

    return render(
        request,
        'create_course.html',
        context=context,
    )


def add_grade(request):
    if request.method == 'POST':
        form = forms.AddGrade(request.POST)
        if form.is_valid():
            grade = int(form.cleaned_data['grade'])
            if  not is_valid_grade(grade):
                return render(
                request,
                'error_page.html',
                context={'msg':"Graded must be integers in range 0 to 100"},
                )
            else:
                # save course to db
                form.save()
                msg = "successfully added grade "+form.cleaned_data['evaluation_name']+": "+str(form.cleaned_data['grade'])+"%"
                return render(
                    request,
                    'error_page.html',
                    context={
                        'msg':msg,
                    },
                )
    else:
        form = forms.AddGrade()

    context = {
        'form':form,
    }
    return render(
        request,
        'add_grade.html',
        context=context,
    )


def delete_grade(request,pk,gradeID):
    Grades.objects.get(id=gradeID).delete()
    # course_link = 'dashboard/courses/'+str(pk)+'/grades'
    return redirect('grades-detail',pk=pk)


def delete_course(request,courseID):
    Course.objects.get(id=courseID).delete()
    return redirect('courses')


def show_error(request):
    return render(
        request,
        'error_page.html',
    )







