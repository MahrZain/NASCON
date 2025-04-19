# your_app/admin.py

from django.contrib import admin
from .models import Course, CourseVideo

class CourseVideoInline(admin.TabularInline):
    model    = CourseVideo
    extra    = 1
    fields   = ('order', 'title', 'video')
    ordering = ('order',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display  = ('name', 'price', 'created_at')
    list_filter   = ('price',)
    search_fields = ('name', 'description')
    inlines       = [CourseVideoInline]

@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):
    list_display  = ('title', 'course', 'order')
    list_filter   = ('course',)
    search_fields = ('title',)
    ordering      = ('course', 'order')
