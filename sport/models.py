from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()
# Create your models here.

class Action(models.Model):
    
    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    def __str__ (self):
        return self.title
    
class Course(models.Model):

    teacher = models.ForeignKey(User , on_delete=models.CASCADE , related_name="course_teacher")
    student = models.ForeignKey(User , on_delete=models.CASCADE , related_name="course_student")

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    def save(self , *args , **kwargs):
         #args is a short form of arguments , this will let you to save multiple arguments in  your class model.
         #kwargs means key value arguments, just like args but with values in each
         # Ensures that teacher has the user_type "teacher"
         if self.teacher.user_type != 'teacher':
            raise ValidationError({'teacher':'Selected user must have user_type "teacher"'})
         
         # Ensures that student has the user_type "student"
         if self.teacher.user_type != 'student':
            raise ValidationError({'student':'Selected user must have user_type "student"'})
         
         super().save(*args , **kwargs)

class Diet(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
class Plan(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    set_number = models.PositiveIntegerField()
    number_per_set = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    day_of_week = models.CharField(max_length=10 , choices=(("saturday", "saturday")
                                                            ("sunday", "sunday")
                                                            ("monday", "monday")
                                                            ("tuesday", "tuesday")
                                                            ("wednesday", "wednesday")
                                                            ("thursday", "thursday")
                                                            ("friday", "friday")))
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    


         
         



    
    
