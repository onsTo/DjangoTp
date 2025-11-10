from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Conference
from .forms import ConferenceForm
from django.contrib.auth.mixins import LoginRequiredMixin  # ili connecter khw youdkhel il update delete add
from .models import Submission
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


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


class ConferenceCreate(LoginRequiredMixin,CreateView):
    model = Conference
    template_name = 'conference/conference_form.html'
    form_class = ConferenceForm
    success_url = reverse_lazy('Conferences_list')


class ConferenceUpdate(LoginRequiredMixin,UpdateView):
    model = Conference
    template_name = 'conference/conference_form.html'
    form_class = ConferenceForm
    success_url = reverse_lazy('Conferences_list')


class ConferenceDelete(LoginRequiredMixin,DeleteView):
    model = Conference
    success_url = reverse_lazy('Conferences_list')
    template_name = 'conference/conference_confirm_delete.html'

class ListSubmissions(ListView):
    model = Submission
    template_name = 'submissions/list_submissions.html'  # à créer
    context_object_name = 'submissions'

    def get_queryset(self):
        # Récupérer l'ID de la conférence depuis l'URL
        conference_id = self.kwargs.get('conference_id')
        conference = get_object_or_404(Conference, pk=conference_id)
        return Submission.objects.filter(conference=conference).order_by('-submission_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conference'] = get_object_or_404(Conference, pk=self.kwargs.get('conference_id'))
        return context

class SubmissionDetailView(DetailView):
    model = Submission
    template_name = 'submissions/submission_detail.html'  # à créer
    context_object_name = 'submission'
    pk_url_kwarg = 'pk'  # correspond à <str:pk> dans l'URL


class AddSubmissionView(CreateView):
    model = Submission
    template_name = 'submissions/add_submission.html'
    fields = ['title', 'abstract', 'keywords', 'paper']  # retirer 'conference'

    def form_valid(self, form):
        # l'utilisateur connecté devient l'auteur
        form.instance.userid = self.request.user

        # récupérer la conférence depuis la query string
        conference_id = self.request.GET.get('conference_id')
        conference = get_object_or_404(Conference, pk=conference_id)
        form.instance.conference = conference

        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse_lazy('list_submissions', kwargs={'conference_id': self.object.conference.pk})
class UpdateSubmissionView(UpdateView):
    model = Submission
    fields = ['title', 'abstract', 'keywords', 'paper', 'status', 'payed']
    template_name = 'submissions/update_submission.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.userid != request.user:
            raise PermissionDenied("Vous n'avez pas la permission de modifier cette soumission.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('list_submissions', kwargs={'conference_id': self.object.conference.pk})
