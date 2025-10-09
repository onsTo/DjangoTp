from django.contrib import admin
from .models import Conference, Submission

# Enregistrer uniquement Submission manuellement
admin.site.register(Submission)
#admin.site.register(Conference)


class SubbmissionInline(admin.TabularInline):
    model = Submission
    extra = 1  # Nombre de formulaires supplémentaires à afficher
    readonly_fields = ('submission_id',)  # Rendre le champ submission_id en lecture seule

#stackedInline avec cette plus simple    

# Personnalisation de l'interface admin pour Conference
@admin.register(Conference)
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




# Personnalisation de l'interface générale
admin.site.site_header = "Gestion de la conférence"
admin.site.site_title = "Gestion de la conférence"
admin.site.index_title = "Bienvenue sur la gestion de la conférence"




