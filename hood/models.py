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


class Profile(models.Model):
    """
    Profile class that defines objects of each profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    idNumber = models.CharField(max_length=8, null=True, unique=True)
    name = models.CharField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='profilepic/')
    generalLocation = models.TextField(max_length=500, blank=True)
    email = models.EmailField(max_length=254)
    hood = models.ForeignKey(Hood, null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    method that lets a user create a profile
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    method that saves a user's profile
    """
    instance.profile.save()

