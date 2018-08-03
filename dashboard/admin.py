from django.contrib import admin
from .models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','homeworks','quizzes','midterms','final')


# Register the Admin classe for Grades using the decorator
@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    list_display = ('course', 'evaluation_type', 'evaluation_name', 'date_added', 'grade')
    fields = ['course','evaluation_type',('evaluation_name','grade'),'date_added']
    ordering = ('evaluation_type','date_added',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email_address','school_name')
    fields = [('first_name','last_name'),'email_address','school_name']