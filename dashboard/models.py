from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


# Grade --> Course --> Assessment : a grade has a course and each course han an assessment
# student AND **Assessment** are stand alone objects (no dependency, they don't depend on any other object)
class Student(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email_address = models.EmailField(max_length=50)
    school_name = models.CharField(max_length=70)

    def get_name(self):
        return self.first_name

class Assessment(models.Model):
    
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

    def get_assessment(self):
        return {'homeworks':self.homeworks, 'quizzes':self.quizzes, 'midterms':self.midterms, 'final':self.final}
    


class Course(models.Model):
    """
    Model representing a Course (e.g. CPSC 317, Math 200).
    """
    name = models.CharField(max_length=20, help_text="Enter a course name (e.g. CPSC 317, MATH 200)")
    avg = models.IntegerField(default=0)
    # each course MUST have one assessment
    assessment = models.OneToOneField(
        Assessment,
        on_delete=models.CASCADE,
        help_text="enter an assessment for this course"
        )

    # def get_absolute_url(self):
    #     """
    #     Returns the url to access a particular course instance.
    #     """
    #     return reverse('course-detail', args=[str(self.id)])
 
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        """
        return reverse('course-detail', args=[str(self.id)])

    def get_name(self):
        return self.name


# each grade row MUST have one assessment
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

    
    ASSESSMENT_TYPE = (
        ('h','Homework'),
        ('q','Quiz'),
        ('m','Midterm'),
        ('f','Final'),
    ) 

    assessment_type = models.CharField(max_length=1, choices=ASSESSMENT_TYPE, default='h' , help_text='Choose type of assessment (e.g Homework)')
    assessment_name = models.CharField(max_length=20, default='Homework 1', help_text='enter a name for this assessment')

    grade = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        help_text = "Enter grade for assessment"
    )

    date_added = models.DateField(("Date"), default=datetime.date.today)

    def __str__(self):
        return self.course.name


