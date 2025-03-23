from django.shortcuts import render
from django.http import Http404, JsonResponse
from . import services

import helpers

# Create your views here.
def course_list_view(request):
    queryset = services.get_published_courses()
    print(queryset)
    # return JsonResponse({"data":[x.path for x in queryset]})
    context = {
        "courses": queryset,
    }
    return render(request, "courses/course_list.html", context)

def course_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404("Course not found")
    lessons_queryset = services.get_course_lessons(course_obj)
    context = {
        "course": course_obj,
        "lessons": lessons_queryset,
    }
    # return JsonResponse({"data": course_obj.title, "lessons": [x.path for x in lessons_queryset]})
    return render(request, "courses/course_detail.html", context)

def lesson_detail_view(request, course_id=None, lesson_id=None, *args, **kwargs):
    lesson_obj = services.get_lesson_detail(
        course_id=course_id, 
        lesson_id=lesson_id)
    if lesson_obj is None:
        raise Http404("Course not found")
    email_id_exists = request.session.get("email_id")
    if lesson_obj.requires_email and not email_id_exists:
        request.session['next_url'] = request.build_absolute_uri()
        return render(request, "courses/email-required.html", {})

    template_name = "courses/lesson-coming-soon.html"
    context = {
        "lesson": lesson_obj
    }
    if not lesson_obj.is_coming_soon and lesson_obj.has_video:
        template_name = "courses/lesson.html"
        
        video_embed_html = helpers.get_cloudinary_video_object(
            lesson_obj,
            field_name="video",
            as_html=True,
            width=750,
        )
        context['video_embed'] = video_embed_html
    
    return render(request, template_name, context)