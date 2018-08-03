from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


# Grade --> Course --> Evaluation : a grade has a course and each course han an evaluation
# Student AND **Evaluation** are stand alone objects (no dependency, they don't depend on any other object)
class Student(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email_address = models.EmailField(max_length=50)
    school_name = models.CharField(max_length=70)
    def get_name(self):
        return self.first_name
    

class Course(models.Model):
    """
    Model representing a Course (e.g. CPSC 317, Math 200).
    """
    name = models.CharField(max_length=20, help_text="Enter a course name (e.g. CPSC 317, MATH 200)")
    # each course MUST have one Evaluation
    homeworks = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        help_text="Percentage weight for homeworks",
    )
    quizzes = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        help_text="Percentage weight for quizzes",
    )
    midterms = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        help_text="Percentage weight for midterms",
    )
    final = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        help_text="Percentage weight for final exam",
    )

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
    
    def get_absolute_url(self):
        return "%i" % self.id


# each grade row MUST have one evaluation
class Grades(models.Model):
    """
    Model representing a grades. 
    NOTE: the relationship between grades and course is one to many (i.e foreignkey)
    one to one relationship allows you to create ONLY one grade per course. But a course 
    obviously can have multiple grades.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        help_text="choose the course for the grade"
    )   
    EVALUATION_TYPE = (
        ('h','Homework'),
        ('q','Quiz'),
        ('m','Midterm'),
        ('f','Final'),
    ) 
    evaluation_type = models.CharField(max_length=1, choices=EVALUATION_TYPE, default='h' , help_text='Choose type of evaluation (e.g Homework)')
    evaluation_name = models.CharField(max_length=20, default='Homework 1', help_text='enter a name for this evaluation')
    grade = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        help_text = "Enter grade (ex. 83)"
    )
    date_added = models.DateField(("Date"), default=datetime.date.today)
    def __str__(self):
        return self.course.name


