from django.contrib import admin
from .models import Course, CourseVideo

# Inline for adding/editing videos right on the Course page
class CourseVideoInline(admin.TabularInline):
    model = CourseVideo
    extra = 1                # how many blank video slots to show
    fields = ('title', 'video', 'order')
    ordering = ('order',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display   = ('name', 'price', 'created_at')
    list_filter    = ('price',)
    search_fields  = ('name', 'description')
    inlines        = [CourseVideoInline]

@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):
    list_display   = ('title', 'course', 'order')
    list_filter    = ('course',)
    search_fields  = ('title',)
    ordering       = ('course', 'order')
