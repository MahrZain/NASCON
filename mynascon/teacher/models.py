from django.db import models

class Course(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail   = models.ImageField(upload_to='course_thumbnails/')
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CourseVideo(models.Model):
    course     = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)
    title      = models.CharField(max_length=150)
    video      = models.FileField(upload_to='course_videos/')
    transcript = models.TextField(blank=True, null=True)
    order      = models.PositiveIntegerField(default=0,
                    help_text="Lower numbers display first")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.name} — {self.title}"
