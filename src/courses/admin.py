from cloudinary import CloudinaryImage
from django.contrib import admin
from courses.models import Course, Lesson
from django.utils.html import format_html

# Register your models here.
class LessonInline(admin.StackedInline):
    model = Lesson
    readonly_fields = ["public_id", "updated"]
    extra = 0

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ['title', 'status', 'access']
    list_filter = ['status', 'access']
    readonly_fields = ['display_image']
    fields = ['public_id', 'title', 'description', 'status', 'image', 'access', 'display_image']
    readonly_fields = ['public_id', 'display_image']

    def display_image(self, obj,*args, **kwargs):
        url = obj.image_admin_url
        return format_html(f"<img src={url} />")

    display_image.short_description = 'Current Image'

