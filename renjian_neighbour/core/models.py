# coding=UTF8
from django.db import models

class Renjianer(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=255)
    user_id = models.IntegerField()
    left_name = models.CharField(max_length=255, null=True)
    left_id = models.IntegerField(null=True)
    right_name = models.CharField(max_length=255, null=True)
    right_id = models.IntegerField(null=True)
    
    def __unicode__(self):
        return self.user_name
    
    class Meta:
        ordering = ["date"]