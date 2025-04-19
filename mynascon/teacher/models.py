# your_app/models.py

import os
import logging
import requests
from django.conf import settings
from django.db import models

# get a logger for warning messages
logger = logging.getLogger(__name__)

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
    order      = models.PositiveIntegerField(default=0, help_text="Lower numbers display first")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.name} — {self.title}"

    def save(self, *args, **kwargs):
        # 1) First save so self.video.path exists
        super().save(*args, **kwargs)

        # 2) Only attempt transcription if we have a video and no transcript yet
        if self.video and not self.transcript:
            api_url = "https://api-inference.huggingface.co/models/openai/whisper-small"
            headers = {"Authorization": f"Bearer {settings.HF_TOKEN}"}

            try:
                with open(self.video.path, "rb") as f:
                    response = requests.post(api_url, headers=headers, data=f, timeout=60)
                    response.raise_for_status()
                    data = response.json()
                    text = data.get("text", "").strip()
            except requests.RequestException as e:
                # log the problem and skip, transcript stays blank
                logger.warning(f"HuggingFace transcription failed for {self.video.name}: {e}")
                text = ""

            # 3) If we got back anything, save it
            if text:
                self.transcript = text
                # update only the transcript field to avoid infinite recursion
                super().save(update_fields=["transcript"])
