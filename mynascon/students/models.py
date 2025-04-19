from django.db import models

class Student(models.Model):
    username = models.CharField(max_length=30, unique=True,null=True)
    email = models.EmailField(unique=True,null=True)
    password = models.CharField(max_length=128)  # store hashed or plain text (for simplicity, keep plain for now)

    def __str__(self):
        return self.username
