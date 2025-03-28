from django.db import models
from django.utils.text import slugify
import uuid
import helpers
from cloudinary.models import CloudinaryField

helpers.cloudinary_init()

# Create your models here.
class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email_required", "Email Required"

class PublishStatus(models.TextChoices):
    PUBLISHED = "published", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "Draft"

def handle_upload(instance, filename):
    return f"{filename}"

def generate_public_id(instance, *args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-", "")[:5]
    if not title:
        return unique_id
    slug = slugify(title)
    unique_id_short = unique_id[:5]
    return f"{slug}-{unique_id_short}"

def get_public_id_prefix(instance, *args, **kwargs):
    if hasattr(instance, 'path'):
        path = instance.path
        if path.endswith("/"):
            path = path[:-1]
        if path.startswith("/"):
            path = path[1:]
        return path
    public_id = instance.public_id
    model_class = instance.__class__
    model_name = model_class.__name__
    model_name_slug = slugify(model_name)
    if not public_id:
        return f"{model_name_slug}"
    return f"{model_name_slug}/{public_id}"

def get_display_name(instance, *args, **kwargs):
    if hasattr(instance, 'get_display_name'):
        return instance.get_display_name()
    elif hasattr(instance, 'title'):
        return instance.title
    model_class = instance.__class__
    model_name = model_class.__name__
    return f"{model_name} Upload"

class Course(models.Model):
    title = models.CharField(max_length=125)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=140, blank=True, null=True, db_index=True)
    # image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    image = CloudinaryField("image", null=True, 
                            public_id_prefix=get_public_id_prefix,
                            display_name = get_display_name,
                            tags=['course', 'thumbnail'])
    access = models.CharField(
        max_length=20, 
        choices=AccessRequirement.choices,
        default=AccessRequirement.EMAIL_REQUIRED)
    status = models.CharField(
        max_length=10, 
        choices=PublishStatus.choices, 
        default=PublishStatus.DRAFT)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    @property
    def path(self):
        return f"/courses/{self.public_id}"
    
    def get_absolute_url(self):
        return self.path
    
    def get_display_name(self):
        return f"{self.title} - Course"
    
    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
    
    def __str__(self):
        return self.title
    

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=125)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=140, blank=True, null=True, db_index=True)
    thumbnail = CloudinaryField("image", 
                            public_id_prefix=get_public_id_prefix,
                            display_name = get_display_name,
                            tags=['lesson', 'thumbnail'],
                            blank=True, null=True)
    video = CloudinaryField("video", 
                            public_id_prefix=get_public_id_prefix,
                            display_name = get_display_name,
                            type="private",
                            tags=['video', 'lesson'],
                            blank=True, null=True, resource_type="video")
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(default=False, help_text="If user does not have access to course, "
    "can they see this?")
    status = models.CharField(
        max_length=10, 
        choices=PublishStatus.choices, 
        default=PublishStatus.PUBLISHED)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    @property
    def is_coming_soon(self):
        return self.status == PublishStatus.COMING_SOON
    
    @property
    def has_video(self):
        return self.video is not None
    
    @property
    def requires_email(self):
        return self.course.access == AccessRequirement.EMAIL_REQUIRED

    @property
    def path(self):
        course_path = self.course.path
        if course_path.endswith("/"):
            course_path = course_path[:-1]
        return f"{course_path}/lessons/{self.public_id}"
    
    def get_absolute_url(self):
        return self.path
    
    def get_display_name(self):
        return f"{self.title} - {self.course.get_display_name()}"
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', '-updated']

