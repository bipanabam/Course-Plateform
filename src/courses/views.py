from django.shortcuts import render
from django.http import Http404, JsonResponse
from . import services

# Create your views here.
def course_list_view(request):
    queryset = services.get_published_courses()
    print(queryset)
    return JsonResponse({"data":[x.id for x in queryset]})
    return render(request, "courses/course_list.html", {})

def course_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404("Course not found")
    lessons_queryset = course_obj.lessons.all()
    return JsonResponse({"data": course_obj.title, "lessons": [x.title for x in lessons_queryset]})
    return render(request, "courses/course_detail.html", {})

def lesson_detail_view(request, course_id=None, lesson_id=None, *args, **kwargs):
    lesson_obj = services.get_lesson_detail(
        course_id=course_id, 
        lesson_id=lesson_id)
    if lesson_obj is None:
        raise Http404("Course not found")
    return JsonResponse({"data": lesson_obj.title})
    return render(request, "courses/lesson_detail.html", {})