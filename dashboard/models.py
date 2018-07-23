from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Assessment(models.Model):
    assessment_name = models.CharField(max_length=20, help_text="enter course name for the assessment (e.g CPSC 317)")
    
    assignment = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        help_text="Percentage weight for assignments",
    )

    quiz = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        help_text="Percentage weight for quizzes",
    )

    midterm = models.IntegerField(
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
        return 'Assessment for ' + self.assessment_name
    


class Course(models.Model):
    """
    Model representing a Course (e.g. CPSC 317, Math 200).
    """
    name = models.CharField(max_length=20, help_text="Enter a course name (e.g. CPSC 317, MATH 200)")
    avg = models.IntegerField(default=0)
    assessment = models.OneToOneField(
        Assessment,
        on_delete=models.CASCADE,
        )

    def get_absolute_url(self):
        """
        Returns the url to access a particular course instance.
        """
        return reverse('course-detail', args=[str(self.id)])
 
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

