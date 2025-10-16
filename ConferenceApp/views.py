from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView, DetailView 

# Create your views here.
def all_conferences(request):
    conferences = Conference.objects.all()
    return render(request, 'conference/liste.html', {'conferences_liste': conferences})

class ConfernceList(ListView):
    model =Conference
    context_object_name = 'liste'
    ordering = ['start_date']
    template_name = 'conference/liste.html'

class ConfernceDetail(DetailView):
    model =Conference
    context_object_name = 'conference'
    template_name = 'conference/detail.html'