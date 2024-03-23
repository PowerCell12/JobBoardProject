# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='images/profile_pics/', blank=True, default='/default_profile_picture.png')



class Moderators(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    ContactNumber = models.CharField(max_length=15, null=True, blank=True)



class Recruiters(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    companies = models.ManyToManyField(to="Company.Company")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        UserProfile.objects.get_or_create(user=instance)
        user_profile = UserProfile.objects.get(user=instance)
        Moderators.objects.get_or_create(user_profile=user_profile)


post_save.connect(create_user_profile, sender=User)
