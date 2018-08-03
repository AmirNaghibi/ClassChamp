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