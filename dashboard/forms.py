from django import forms
from . import models

class AddCourse(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = '__all__'
        help_texts = {
            'name': '',
            'homeworks':'',
            'quizzes':'',
            'midterms':'',
            'final':'',
        }


class AddGrade(forms.ModelForm):
    class Meta:
        model = models.Grades
        fields = '__all__'
        help_texts = {
            'course':'',
            'evaluation_type':'',
            'evaluation_name':'',
            'grade':'',
            'date_added':'',
        }