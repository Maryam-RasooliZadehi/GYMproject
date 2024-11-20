from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model
# Create your models here.

class Action(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    def __str__ (self):
        return self.title
    



    
    
