from django.contrib import admin
#from evenementsSecurite.models import Evtsecurite
#from inspections.models import Inspection
#from planformations.models import Directionac, Departementac, Serviceac, Bureauac, Formationac, Agentac, 
from .models import Aerodrome, Evtsecurite, Inspection, Trajetmission, Positionequipe, Dossierevenementsecu, Dossieragent, Dossierformation, Document
from .models import Directionac, Departementac, Serviceac, Bureauac, Formationac, Agentac,DomaineInspection, Dossierinspection, Dossieraerodrome
from django import forms




class AgentacAdmin(admin.ModelAdmin):
	list_display = ('prenomsag', 'nomag', 'matriculeag', 'serviceac')
	list_filter = ('serviceac',)
	search_fields = ('nomag', 'matriculeag')
	
	
class DocumentAdmin(admin.ModelAdmin):
	list_display = ('codedocument', 'titre', 'datedocument', 'departementdocument')
	list_filter = ('datedocument',)
	search_fields = ('codedocument', 'titre')
	


class FormationacAdmin(admin.ModelAdmin):
	list_display = ('codeform', 'nomform', 'debutforma', 'finforma', 'lieuforma')
	ordering = ('debutforma',)
	search_fields = ('nomform', 'codeform')
	
	
class EvtsecuriteAdmin(admin.ModelAdmin):
	list_display = ('codeevt', 'dateevt', 'heureevt', 'notifiantevt', 'lieuevt')
	ordering = ('dateevt',)
	search_fields = ('codeevt', 'dateevt')
	

class InspectionAdmin(admin.ModelAdmin):
	autocompleted_fields = {'codeinsp' :'nomaero'}
	
	list_display = ('codeinsp', 'datedebutinsp', 'zoneinsp', 'nomdepartement')
	list_filter = ('datedebutinsp',)
	search_fields = ('zoneinsp', 'codeinsp')
	
"""
class DossierinspectionAdmin(admin.ModelAdmin):
	list_display = ('codeevt', 'dateevt', 'heureevt', 'notifiantevt', 'lieuevt')
	ordering = ('dateevt',)
	search_fields = ('codeevt', 'dateevt')
	
	"""
	
	
	
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Document,DocumentAdmin)
		
admin.site.register(Directionac)
admin.site.register(Departementac)
admin.site.register(Serviceac)
admin.site.register(Bureauac)
admin.site.register(DomaineInspection)
admin.site.register(Dossieraerodrome)
admin.site.register(Dossierformation)

admin.site.register(Agentac, AgentacAdmin)
admin.site.register(Formationac, FormationacAdmin)
admin.site.register(Aerodrome)
admin.site.register(Evtsecurite,EvtsecuriteAdmin)

admin.site.register(Trajetmission)
admin.site.register(Positionequipe)
admin.site.register(Dossierinspection)
"""admin.site.register(Dossierinspection, DossierinspectionAdmin)"""
admin.site.register(Dossierevenementsecu)
admin.site.register(Dossieragent)


