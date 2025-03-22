from django.shortcuts import render

def homepage(request, *args, **kwargs):
    template_name = "home.html"
    return render(request, template_name)