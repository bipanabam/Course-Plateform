# Generated by Django 5.1.7 on 2025-03-19 15:46

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_course_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=125)),
                ('description', models.TextField(blank=True, null=True)),
                ('thumbnail', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('video', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='video')),
                ('order', models.IntegerField(default=0)),
                ('can_preview', models.BooleanField(default=False, help_text='If user does not have access to course, can they see this?')),
                ('status', models.CharField(choices=[('published', 'Published'), ('soon', 'Coming Soon'), ('draft', 'Draft')], default='published', max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.course')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
