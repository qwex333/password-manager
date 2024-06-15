from django.db import models

# Create your models here.
from datetime import datetime
from django.contrib.auth.models import User

# eache variable in class obj is a column in DB

# class UserAccount(models.Model):
#     username = models.CharField(max_length=30, unique=True)
#     password = models.CharField(max_length=30)
#     reg_time = models.TimeField("time registered", default=datetime.now())

#     def __str__(self) -> str:
#         return self.username

class PasswordData(models.Model):
    # user = models.ForeignKey(UserAccount, to_field="username", related_name="passworddata", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="passworddata", on_delete=models.CASCADE)

    subject = models.CharField(max_length=30)
    account = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    date_added = models.DateField("date added", default=datetime.today())

    def __str__(self) -> str:
        return self.subject + " -- " + self.account
