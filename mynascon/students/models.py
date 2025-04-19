from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Student(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name='student_groups',  # changed
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='student_permissions',  # changed
        blank=True
    )

    def __str__(self):
        return self.username
