from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional
    portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username   # username is the default attribute of User. It means where we can store the data.


# blank=True means even if user don't provide anything it will still run.

# upload_to='profile_pics' means it will go to media -> profile_pics folder path whenever user will enter image.

'''
Note:- In User class by default it has username, email, password, firstname, lastname. 
But if you want to add something extra field than you have to to do this 'OneToOneField'.
In this you can extra like URLField, ImageField and all.
'''