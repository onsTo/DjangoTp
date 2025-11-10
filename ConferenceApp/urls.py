from django.urls import path
#from .views import *
from .views import ConfernceList, ConfernceDetail, ConferenceCreate, ConferenceUpdate, ConferenceDelete
from .views import ListSubmissions, SubmissionDetailView, AddSubmissionView, UpdateSubmissionView


urlpatterns = [
    #path("liste/", views.all_conferences, name="Conferences_list"), #importation de fonction
    #pour utilser dans le code name="Conferences_list" et "liste/" pour navigation
    path("liste/", ConfernceList.as_view(), name="Conferences_list"),
    path("detail/<int:pk>/", ConfernceDetail.as_view(), name="Conference_detail"),
    path("form/", ConferenceCreate.as_view(), name="Conference_add"),
    path("<int:pk>/edit/", ConferenceUpdate.as_view(), name="Conference_edit"),
    path("<int:pk>/delete/", ConferenceDelete.as_view(), name="Conference_delete"),
    #submissions
    path('conference/<int:conference_id>/submissions/', ListSubmissions.as_view(), name='list_submissions'),
    path('submission/add/', AddSubmissionView.as_view(), name='add_submission'),
    path('submission/<str:pk>/', SubmissionDetailView.as_view(), name='submission_detail'),
    path('submission/<str:pk>/edit/', UpdateSubmissionView.as_view(), name='update_submission'),



    
]
