# coding=UTF8
from django.db import models

class Renjianer(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=255)
    user_id = models.IntegerField()
    left_name = models.CharField(max_length=255)
    left_id = models.IntegerField()
    right_name = models.CharField(max_length=255)
    right_id = models.IntegerField()
    
    def __str__(self):
        return self.user_name
    
    class Meta:
        ordering = ["user_name"]