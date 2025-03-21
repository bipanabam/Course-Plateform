from django.urls import path
from . import views

urlpatterns = [
    path("courses/", views.course_list_view, name="course_list"),
    path("courses/<int:course_id>/", views.course_detail_view, name="course_detail"),
    path("courses/<int:course_id>/lessons/<int:lesson_id>/", views.lesson_detail_view, name="lesson_detail"),
]
