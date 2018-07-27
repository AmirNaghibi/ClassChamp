from django.contrib import admin
from .models import Student ,Assessment, Course, Grades

# Register your models here.
#admin.site.register(Assessment)
admin.site.register(Course)
#admin.site.register(Grades)


# Register the Admin classe for Grades using the decorator
@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    list_display = ('course', 'assessment_type', 'assessment_name', 'date_added', 'grade')
    fields = ['course','assessment_type',('assessment_name','grade'),'date_added']
    ordering = ('assessment_type','date_added',)


# Register the Admin classe for Assessment using the decorator
@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    # list_display = ('course_name', 'homeworks', 'quizzes','midterms','final')
    list_display = ('homeworks', 'quizzes','midterms','final')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email_address','school_name')
    fields = [('first_name','last_name'),'email_address','school_name']