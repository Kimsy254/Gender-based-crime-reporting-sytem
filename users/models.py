from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings


class User(AbstractUser):
    is_member = models.BooleanField(default=False)




class Member(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='Member')
    #username = None
    email = models.EmailField(max_length=20, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    member_profile_pic = models.ImageField(upload_to="profile_pic/member_profile_pic",blank=True)
   

    def get_absolute_url(self):
        return reverse('accounts:member_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['email']
        unique_together = ['email']


