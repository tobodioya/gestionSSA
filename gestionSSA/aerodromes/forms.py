from django.forms import ModelForm
from .models import Choixdepartement, Dossierinspection, Dossieraerodrome, Dossierevenementsecu, Dossierformation, Dossieragent, Evtsecurite
from django import forms



class ChoixdepartementForm(ModelForm):
    class Meta:
        model = Choixdepartement
        exclude = ['descript']
        
        
        

class DossierinspectionForm(ModelForm):
	class Meta:
		model = Dossierinspection
		exclude = ['description', 'dossierinsp', 'datedocument' ]
		

class DossieraerodromeForm(ModelForm):
	class Meta:
		model = Dossieraerodrome
		exclude = ['descriptiondossier', 'dossieraero', 'datedoc' ]
		
		

class DossierevenementsecuForm(ModelForm):
	class Meta:
		model = Dossierevenementsecu
		exclude = ['descriptiondocumentevt', 'dossierevt', 'datedocumentevt' ]
		
		
class DossierformationForm(ModelForm):
	class Meta:
		model = Dossierformation
		exclude = ['description', 'dossierformation', 'datedocument' ]
		
		
		
class DossieragentForm(ModelForm):
	class Meta:
		model = Dossieragent
		exclude = ['descriptiondocumentagent', 'dossieragent', 'datedocumentagent' ]
		
		

class EvtsecuriteForm(ModelForm):
	
	choixaero = forms.BooleanField(initial=False, required=False)
	choixdebut = forms.DateField(required=False)
	choixfin = forms.DateField(required=False)
	choixperiode = forms.BooleanField(initial=False, required=False)
	
	
	class Meta:
		model = Evtsecurite
		exclude = ['latitudeevt', 'longitudeevt', 'dateevt', 'heureevt', 'notifiantevt', 'immataeronefevt', 
		'descripinsp', 'notifevt', 'nomanimalevt', 'statutevt', 'lieuevt', 'classeevt', 'groupeanimalevt']
		
		

"""class ChoixrequeteForm(forms.Form):
	choixclassevt = forms.BooleanField(required=False)
	choixgrpanim = forms.BooleanField(required=False)
	choixaero = forms.BooleanField(required=False)
	choixdebut = forms.DateField(required=False)
	choixfin = forms.DateField(required=False)
	choixperiode = forms.BooleanField(required=False)"""
	   

   