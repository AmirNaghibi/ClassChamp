from django.contrib import admin
from .models import Student ,Assessment, Course, Grades


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','assessment')

# Register the Admin classe for Grades using the decorator
@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    list_display = ('course', 'assessment_type', 'assessment_name', 'date_added', 'grade')
    fields = ['course','assessment_type',('assessment_name','grade'),'date_added']
    ordering = ('assessment_type','date_added',)


# Register the Admin classe for Assessment using the decorator
@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('homeworks', 'quizzes','midterms','final')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email_address','school_name')
    fields = [('first_name','last_name'),'email_address','school_name']