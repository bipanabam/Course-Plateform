from django.urls import path
from . import views

urlpatterns = [
    path("courses/", views.course_list_view, name="course_list"),
    path("courses/<slug:course_id>/", views.course_detail_view, name="course_detail"),
    path("courses/<slug:course_id>/lessons/<slug:lesson_id>/", views.lesson_detail_view, name="lesson_detail"),
]
