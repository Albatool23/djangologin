from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def login_validator(self, postData):
       errors = {}
       user = Users.objects.filter(email=postData['email'])
       if len(user) == 0:
           errors['email_e'] = "Email or Password is not correct"

       elif (user[0].email != postData['email']):
           errors['email_n'] = "Email or Password is not correct"

       elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
           errors['password'] = "Email or Password is not correct"
       return errors

    def registration_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        elif len(postData['password']) < 8:
            errors['password'] = "password should be at least 8 characters"
        elif (postData['password'] != postData['cPassword']):
            errors['cPassword'] = "password is not equal to the confirm password"
        elif len(postData['fname']) < 2:
            errors['fname'] = "name should be at least 2 characrters long"
        elif len(postData['lname']) < 2:
            errors['lname'] = "name should be at least 2 characrters long"
        return errors

class Users (models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    cpw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
