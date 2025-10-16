from django.contrib import admin
from .models import Conference
from .models import Submission


# Enregistrer uniquement Submission manuellement
#admin.site.register(Submission)
#admin.site.register(Conference)


class SubmissionStackedInline(admin.StackedInline):
    model = Submission
    extra = 1  # nombre de formulaires vides affichés par défaut
    fields = (
        'title',
        'abstract',
        'status',
        'payed',
        'submission_id',
        'submission_date',
    )
    readonly_fields = ('submission_id', 'submission_date')  # champs lecture seule
    show_change_link = True  # optionnel : lien pour ouvrir la soumission complète


# Variante 2 : Inline tabulaire (Tableau horizontal)
class SubmissionTabularInline(admin.TabularInline):
    model = Submission
    extra = 1
    fields = ('title', 'status', 'payed')  # supprimer 'user'
    #readonly_fields = ('status',)  # si tu veux
    show_change_link = True




class SubbmissionInline(admin.TabularInline):
    model = Submission
    extra = 1  # Nombre de formulaires supplémentaires à afficher
    readonly_fields = ('submission_id',)  # Rendre le champ submission_id en lecture seule
    

# Personnalisation de l'interface admin pour Conference
"""@admin.register(Conference)
class AdminPerso(admin.ModelAdmin):
    list_display = ('name', 'theme', 'start_date', 'end_date','duration')
    ordering = ('start_date',)
    search_fields = ('name',)
    list_filter = ('theme', 'location', 'start_date', 'end_date')
    #fieldsets mte3 kel html yekhdhou liste de tuple
    fieldsets = (
    ("Informations générales", {
        'fields': ('name', 'description', 'location', 'theme')
    }),
    ("Logistics", {
        'fields': ('start_date', 'end_date')
    }),
    )
    read_only_fields = ('conference_id',)
    def duration(self, objet):
        if objet.start_date and objet.end_date:
            return objet.end_date - objet.start_date
        else:
            return "RAS"
    #bech nsameha fel html
    duration.short_description = "Duration (Days)"
    #taffichilek les dates fel haut mta3 page
    date_hierarchy = 'start_date'
    
    inlines = [SubbmissionInline]

"""


@admin.register(Conference)
class AdminPerso(admin.ModelAdmin):
    list_display = ('name', 'theme', 'start_date', 'end_date', 'duration')
    ordering = ('start_date',)
    search_fields = ('name',)
    list_filter = ('theme', 'location', 'start_date', 'end_date')

    fieldsets = (
        ("Informations générales", {
            'fields': ('name', 'description', 'location', 'theme')
        }),
        ("Logistics", {
            'fields': ('start_date', 'end_date')
        }),
    )

    readonly_fields = ('conference_id',)

    # Méthode pour calculer la durée d’une conférence
    def duration(self, obj):
        if obj.start_date and obj.end_date:
            return obj.end_date - obj.start_date
        else:
            return "RAS"
    duration.short_description = "Duration (Days)"

    # Affiche la hiérarchie par date
    date_hierarchy = 'start_date'

        # Ajout de l’inline pour afficher les soumissions liées à la conférence
    #inlines = [SubmissionStackedInline]
    inlines = [SubmissionTabularInline] #  Version tabulaire

@admin.action(description="Marquer comme payée")
def mark_as_payed(modeladmin, request, queryset):
    queryset.update(payed=True)

@admin.action(description="Marquer comme acceptée")
def mark_as_accepted(modeladmin, request, queryset):
    queryset.update(status="Accepted")

class SubmissionAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste
    list_display = ('title', 'status', 'get_user', 'conference', 'submission_date', 'payed', 'short_abstract')
    
    # Champs modifiables directement depuis la liste
    list_editable = ('status', 'payed')
    
    # Filtres dans la liste
    list_filter = ('status', 'payed', 'conference', 'submission_date')
    
    # Recherche
    search_fields = ('title', 'keywords', 'userid__username')
    
    # Lecture seule dans le formulaire d'édition
    readonly_fields = ('submission_id', 'submission_date')
    
    # Organisation du formulaire par sections
    fieldsets = (
        ('Infos générales', {
            'fields': ('submission_id', 'title', 'abstract', 'keywords')
        }),
        ('Fichier et conférence', {
            'fields': ('paper', 'conference')
        }),
        ('Suivi', {
            'fields': ('status', 'payed', 'submission_date', 'userid')
        }),
    )
    # Actions personnalisées pour make payed et make accepted
    actions = [mark_as_payed,mark_as_accepted]
    
    # Méthodes personnalisées
    def get_user(self, obj):
        return obj.userid
    get_user.short_description = 'User'
    
    def short_abstract(self, obj):
        return (obj.abstract[:50] + "...") if len(obj.abstract) > 50 else obj.abstract
    short_abstract.short_description = 'Résumé'

admin.site.register(Submission, SubmissionAdmin)




# Personnalisation de l'interface générale
admin.site.site_header = "Gestion de la conférence"
admin.site.site_title = "Gestion de la conférence"
admin.site.index_title = "Bienvenue sur la gestion de la conférence"




