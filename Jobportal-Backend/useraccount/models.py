from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save





class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    resume = models.FileField(upload_to="files", null=True)

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    user = instance

    if created:
        profile = UserProfile(user=user)
        profile.save()

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, related_name='employerprofile', on_delete=models.CASCADE)

    company_name = models.CharField(max_length=20,null=True)

    services = models.CharField(max_length=120,null=True)
    employees=models.IntegerField(null=True)
    website = models.CharField(max_length=50,null=True)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    user = instance

    if created:
        profile = EmployerProfile(user=user)
        profile.save()
