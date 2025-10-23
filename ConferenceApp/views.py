from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Conference
from .forms import ConferenceForm

# Create your views here.
def all_conferences(request):
    conferences = Conference.objects.all()
    return render(request, 'conference/liste.html', {'conferences_liste': conferences})

class ConfernceList(ListView):
    model =Conference
    context_object_name = 'liste'
    ordering = ['start_date']
    template_name = 'conference/liste.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 🔥 Ajouter la liste des thèmes dans le contexte
        context['themes'] = Conference.THEME
        return context


class ConfernceDetail(DetailView):
    model =Conference
    context_object_name = 'conference'
    template_name = 'conference/detail.html'


class ConferenceCreate(CreateView):
    model = Conference
    template_name = 'conference/conference_form.html'
    form_class = ConferenceForm
    success_url = reverse_lazy('Conferences_list')


class ConferenceUpdate(UpdateView):
    model = Conference
    template_name = 'conference/conference_form.html'
    form_class = ConferenceForm
    success_url = reverse_lazy('Conferences_list')


class ConferenceDelete(DeleteView):
    model = Conference
    success_url = reverse_lazy('Conferences_list')
    template_name = 'conference/conference_confirm_delete.html'

