from django.db import models

# Create your models here.
class courseCreation(models.Model):
    Course_name = models.CharField(max_length=100)
    Course_Description = models.TextField()
    Course_thumbnail = models.ImageField(upload_to='course_thumbnails/')
    Course_video = models.FileField(upload_to='course_videos/')
    Course_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.Course_name

