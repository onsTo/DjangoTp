from django.urls import path
#from .views import *
from .views import ConfernceList, ConfernceDetail, ConferenceCreate, ConferenceUpdate, ConferenceDelete

urlpatterns = [
    #path("liste/", views.all_conferences, name="Conferences_list"), #importation de fonction
    #pour utilser dans le code name="Conferences_list" et "liste/" pour navigation
    path("liste/", ConfernceList.as_view(), name="Conferences_list"),
    path("detail/<int:pk>/", ConfernceDetail.as_view(), name="Conference_detail"),
    path("form/", ConferenceCreate.as_view(), name="Conference_add"),
    path("<int:pk>/edit/", ConferenceUpdate.as_view(), name="Conference_edit"),
    path("<int:pk>/delete/", ConferenceDelete.as_view(), name="Conference_delete"),
    
]
