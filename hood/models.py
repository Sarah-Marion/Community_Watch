from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
class Hood(models.Model):
    """
    Hood class that defines objects of each neighbourhood
    """
    hoodName = models.CharField(max_length=100)
    hoodLocation = models.CharField(max_length=50, null=True)
    occupantsCount = models.PositiveSmallIntegerField(null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.hoodName

    def save_hood(self):
        """
        Method that creates a new hood object
        """
        self.save()

    def delete_hood(self):
        """
        Method that deletes a hood object
        """
        self.delete()