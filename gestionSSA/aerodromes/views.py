from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Inspection, Aerodrome
import collections

from django.http import HttpResponse, Http404
from datetime import datetime, timedelta

from .models import Agentac, Formationac, DomaineInspection, Dossierinspection, Dossieraerodrome, Evtsecurite, Dossierevenementsecu, Dossierformation, Dossieragent, Document
from django.views import generic
from django.contrib.auth.decorators import login_required

from .forms import ChoixdepartementForm, DossierinspectionForm, DossieraerodromeForm, DossierevenementsecuForm, DossierformationForm, DossieragentForm, EvtsecuriteForm
from django.db.models import Q



@login_required
def home(request):
	
	aeroportinternationaux = Aerodrome.objects.filter(Q(aerointernational=True))
	aeroportnationaux = Aerodrome.objects.filter(Q(aerointernational=False))
	
	return render(request, 'aerodromes/accueil.html', {
	'aeroportinternationaux': aeroportinternationaux,
	'aeroportnationaux': aeroportnationaux,
	
	 })


@login_required
def pageevts(request):
	evenementssecurite = Evtsecurite.objects.all()
	tauxevtsPAN = 0
	tauxevtsFDG = 0
	tauxevtsMET = 0
	tauxevtsAUT = 0
	
	nbreevtsecu = Evtsecurite.objects.all().count()
	nbreevtsPAN = Evtsecurite.objects.filter(Q(typeevt='PAN')).count()
	nbreevtsFDG = Evtsecurite.objects.filter(Q(typeevt='FDG')).count()
	nbreevtsMET = Evtsecurite.objects.filter(Q(typeevt='MET')).count()
	
	if(nbreevtsecu != 0):
		tauxevtsPAN = round(100*(nbreevtsPAN/nbreevtsecu),2)
		tauxevtsFDG = round(100*(nbreevtsFDG/nbreevtsecu),2)
		tauxevtsMET = round(100*(nbreevtsMET/nbreevtsecu),2)
		tauxevtsAUT = round((100*(nbreevtsecu - nbreevtsPAN - nbreevtsFDG - nbreevtsMET)/nbreevtsecu),2)
	
	form = DossierevenementsecuForm()
	return render(request, 'aerodromes/evenementsSecurite/accueil.html', {
	'evenementssecurite': evenementssecurite,
	'form': form,
	'tauxevtsPAN': tauxevtsPAN,
	'tauxevtsFDG': tauxevtsFDG,
	'tauxevtsMET': tauxevtsMET,
	'tauxevtsAUT': tauxevtsAUT,
	
	})
    



@login_required
def afficherperilanimal(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    
   
    anneecourante = datetime.today().year
         
    evtsecuanneecourante = Evtsecurite.objects.filter(Q(dateevt__year = anneecourante), Q(typeevt = 'PAN'))
    evtsecuanneepreceden = Evtsecurite.objects.filter(Q(dateevt__year = anneecourante-1), Q(typeevt = 'PAN'))
    
    nbreevtsecuanneecourante = evtsecuanneecourante.count()
    nbreevtsecuanneepreceden = evtsecuanneepreceden.count()
        
    formattedtypeevts = [format(evt.dateevt.month) for evt in evtsecuanneecourante]
    formattedtypeevtsp = [format(evt.dateevt.month) for evt in evtsecuanneepreceden]
    
    evtpanancourparmois = {x:formattedtypeevts.count(x) for x in formattedtypeevts}
    lesevtpan = list(evtpanancourparmois.keys())
    nbredevpanparmois = list(evtpanancourparmois.values())
    evtspanmoisnbre = []
    cteur = 0
    for i in lesevtpan:
    	bonformat = {}
    	bonformat['mois'] = lesevtpan[cteur]
    	bonformat['nbreevt'] = nbredevpanparmois[cteur]
    	evtspanmoisnbre.append(bonformat)
    	cteur = cteur + 1
    
    evtspanmoisnbre = sorted(evtspanmoisnbre, key = lambda i: i['mois'])
    
    evtpanancourparmoisp = {x:formattedtypeevtsp.count(x) for x in formattedtypeevtsp}
    lesevtpanp = list(evtpanancourparmoisp.keys())
    nbredevpanparmoisp = list(evtpanancourparmoisp.values())
    evtspanmoisnbrep = []
    cteur = 0
    for i in lesevtpanp:
    	bonformatp = {}
    	bonformatp['mois'] = lesevtpanp[cteur]
    	bonformatp['nbreevt'] = nbredevpanparmoisp[cteur]
    	evtspanmoisnbrep.append(bonformatp)
    	cteur = cteur + 1
    
    evtspanmoisnbrep = sorted(evtspanmoisnbrep, key = lambda i: i['mois'])
    bonnelisteevt = []
    for i in range(12):
    	bonformatbon = {}
    	bonformatbon['mois'] = i+1
    	bonformatbon['nbreevt'] = 0
    	bonnelisteevt.append(bonformatbon)
    	
    bonnelisteevtan = []
    for i in range(12):
    	bonformatbonan = {}
    	bonformatbonan['mois'] = i+1
    	bonformatbonan['nbreevt'] = 0
    	bonnelisteevtan.append(bonformatbonan)
    	
    for ev in evtspanmoisnbre:
    	for i in bonnelisteevtan:
    		if str(ev['mois']) == str(i['mois']):
    			i['nbreevt'] = ev['nbreevt']
    	
    for ev in evtspanmoisnbrep:
    	for i in bonnelisteevt:
    		if str(ev['mois']) == str(i['mois']):
    			i['nbreevt'] = ev['nbreevt']
  	              
    
    return render(request, 'aerodromes/evenementsSecurite/Perilanimalier.html',{
    
    'bonnelisteevt': bonnelisteevt,
    'bonnelisteevtan': bonnelisteevtan,
    'anneecourante': anneecourante,
    'anneeprecedente': anneecourante-1,
    'evtsecuanneecourante': evtsecuanneecourante, 
    'evtsecuanneepreceden': evtsecuanneepreceden,
    'nbreevtsecuanneepreceden': nbreevtsecuanneepreceden,
    'nbreevtsecuanneecourante': nbreevtsecuanneecourante,
    })
    



@login_required
def afficherrequetesepecif(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    
    anneecourante = datetime.today().year
    evenementssecurites = Evtsecurite.objects.all()
         
    evtsecuanneecourante = Evtsecurite.objects.filter(Q(dateevt__year = anneecourante))
    evtsecuanneepreceden = Evtsecurite.objects.filter(Q(dateevt__year = anneecourante-1))
    
    nbreevtsecuanneecourante = evtsecuanneecourante.count()
    nbreevtsecuanneepreceden = evtsecuanneepreceden.count()
        
    formattedtypeevts = [format(evt.dateevt.month) for evt in evtsecuanneecourante]
    formattedtypeevtsp = [format(evt.dateevt.month) for evt in evtsecuanneepreceden]
    
    evtpanancourparmois = {x:formattedtypeevts.count(x) for x in formattedtypeevts}
    lesevtpan = list(evtpanancourparmois.keys())
    nbredevpanparmois = list(evtpanancourparmois.values())
    evtspanmoisnbre = []
    cteur = 0
    for i in lesevtpan:
    	bonformat = {}
    	bonformat['mois'] = lesevtpan[cteur]
    	bonformat['nbreevt'] = nbredevpanparmois[cteur]
    	evtspanmoisnbre.append(bonformat)
    	cteur = cteur + 1
    
    evtspanmoisnbre = sorted(evtspanmoisnbre, key = lambda i: i['mois'])
    
    evtpanancourparmoisp = {x:formattedtypeevtsp.count(x) for x in formattedtypeevtsp}
    lesevtpanp = list(evtpanancourparmoisp.keys())
    nbredevpanparmoisp = list(evtpanancourparmoisp.values())
    evtspanmoisnbrep = []
    cteur = 0
    for i in lesevtpanp:
    	bonformatp = {}
    	bonformatp['mois'] = lesevtpanp[cteur]
    	bonformatp['nbreevt'] = nbredevpanparmoisp[cteur]
    	evtspanmoisnbrep.append(bonformatp)
    	cteur = cteur + 1
    
    evtspanmoisnbrep = sorted(evtspanmoisnbrep, key = lambda i: i['mois'])
    bonnelisteevt = []
    for i in range(12):
    	bonformatbon = {}
    	bonformatbon['mois'] = i+1
    	bonformatbon['nbreevt'] = 0
    	bonnelisteevt.append(bonformatbon)
    	
    bonnelisteevtan = []
    for i in range(12):
    	bonformatbonan = {}
    	bonformatbonan['mois'] = i+1
    	bonformatbonan['nbreevt'] = 0
    	bonnelisteevtan.append(bonformatbonan)
    	
    for ev in evtspanmoisnbre:
    	for i in bonnelisteevtan:
    		if str(ev['mois']) == str(i['mois']):
    			i['nbreevt'] = ev['nbreevt']
    	
    for ev in evtspanmoisnbrep:
    	for i in bonnelisteevt:
    		if str(ev['mois']) == str(i['mois']):
    			i['nbreevt'] = ev['nbreevt']
    
   
    
    form = EvtsecuriteForm()	
    
    return render(request, 'aerodromes/evenementsSecurite/requetesepecif.html', {
    'form': form,
    
    'bonnelisteevt': bonnelisteevt,
    'bonnelisteevtan': bonnelisteevtan,
    'anneecourante': anneecourante,
    'anneeprecedente': anneecourante-1,
    'evtsecuanneecourante': evtsecuanneecourante, 
    'evtsecuanneepreceden': evtsecuanneepreceden,
    'nbreevtsecuanneepreceden': nbreevtsecuanneepreceden,
    'nbreevtsecuanneecourante': nbreevtsecuanneecourante,
    'evenementssecurites': evenementssecurites,
    
    })


@login_required
def afficherresultatrequetespeci(request):
	
	if request.method == 'POST':
		aerodevt = '--(TOUS)'
		
		choixdebut = '--'
		choixfin = '-- (à tout moment)'
		form = EvtsecuriteForm(request.POST)
		
		if form.is_valid():
			typedevt = form.cleaned_data['typeevt']
			
			choixaero = form.cleaned_data['choixaero']
			choixperiode = form.cleaned_data['choixperiode']
									
			anneecourante = datetime.today().year
			evenementssecurites = Evtsecurite.objects.filter(Q(typeevt = typedevt))
			
			evtsecuanneecourante = Evtsecurite.objects.filter(Q(dateevt__year = anneecourante), Q(typeevt = typedevt))
			evtsecuanneepreceden = Evtsecurite.objects.filter(Q(dateevt__year = anneecourante-1), Q(typeevt = typedevt))
			
			if choixaero == True:
				aerodevt = form.cleaned_data['nomaero'].nomaero
				evtsecuanneecourante = evtsecuanneecourante.filter(Q(nomaero__nomaero = aerodevt))
				evtsecuanneepreceden = evtsecuanneepreceden.filter(Q(nomaero__nomaero = aerodevt))
			if choixperiode == True:
				choixdebut = form.cleaned_data['choixdebut']
				choixfin = form.cleaned_data['choixfin']
				evenementssecurites = evenementssecurites.filter(Q(dateevt__lte = choixfin), Q(dateevt__gte = choixdebut))
			
			formattedtypeevts = [format(evt.dateevt.month) for evt in evtsecuanneecourante]
			formattedtypeevtsp = [format(evt.dateevt.month) for evt in evtsecuanneepreceden]
			evtpanancourparmois = {x:formattedtypeevts.count(x) for x in formattedtypeevts}
			lesevtpan = list(evtpanancourparmois.keys())
			nbredevpanparmois = list(evtpanancourparmois.values())
			evtspanmoisnbre = []
			cteur = 0
			for i in lesevtpan:
				bonformat = {}
				bonformat['mois'] = lesevtpan[cteur]
				bonformat['nbreevt'] = nbredevpanparmois[cteur]
				evtspanmoisnbre.append(bonformat)
				cteur = cteur + 1
				
			evtspanmoisnbre = sorted(evtspanmoisnbre, key = lambda i: i['mois'])
			evtpanancourparmoisp = {x:formattedtypeevtsp.count(x) for x in formattedtypeevtsp}
			lesevtpanp = list(evtpanancourparmoisp.keys())
			nbredevpanparmoisp = list(evtpanancourparmoisp.values())
			evtspanmoisnbrep = []
			cteur = 0
			for i in lesevtpanp:
				bonformatp = {}
				bonformatp['mois'] = lesevtpanp[cteur]
				bonformatp['nbreevt'] = nbredevpanparmoisp[cteur]
				evtspanmoisnbrep.append(bonformatp)
				cteur = cteur + 1
				
			evtspanmoisnbrep = sorted(evtspanmoisnbrep, key = lambda i: i['mois'])
			bonnelisteevt = []
			for i in range(12):
				bonformatbon = {}
				bonformatbon['mois'] = i+1
				bonformatbon['nbreevt'] = 0
				bonnelisteevt.append(bonformatbon)
				
			bonnelisteevtan = []
			for i in range(12):
				bonformatbonan = {}
				bonformatbonan['mois'] = i+1
				bonformatbonan['nbreevt'] = 0
				bonnelisteevtan.append(bonformatbonan)
			
			for ev in evtspanmoisnbre:
				for i in bonnelisteevtan:
					if str(ev['mois']) == str(i['mois']):
						i['nbreevt'] = ev['nbreevt']
						
			for ev in evtspanmoisnbrep:
				for i in bonnelisteevt:
					if str(ev['mois']) == str(i['mois']):
						i['nbreevt'] = ev['nbreevt']
			
			nbreevtsecuanneecourante = evtsecuanneecourante.count()
			nbreevtsecuanneepreceden = evtsecuanneepreceden.count()
			nombreevenementssecurite = evenementssecurites.count()
			
				
						
			
			return render(request, 'aerodromes/evenementsSecurite/resultatrequetespeci.html', {
			
			'bonnelisteevt': bonnelisteevt,
			'bonnelisteevtan': bonnelisteevtan,
			'anneecourante': anneecourante,
			'anneeprecedente': anneecourante-1,
			'evtsecuanneecourante': evtsecuanneecourante,
			'evtsecuanneepreceden': evtsecuanneepreceden,
			'nbreevtsecuanneepreceden': nbreevtsecuanneepreceden,
			'nbreevtsecuanneecourante': nbreevtsecuanneecourante,
			'evenementssecurites': evenementssecurites,
			'typedevt': typedevt,
			'aerodevt': aerodevt,
			'choixfin': choixfin,
			'choixdebut': choixdebut,
			'nombreevenementssecurite': nombreevenementssecurite,
			
			})




@login_required
def afficherfeunalaser(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    
    anneecourante = datetime.today().year
    
    evtsecuanneecourante = Evtsecurite.objects.filter(Q(dateevt__year = anneecourante), Q(typeevt = 'FDG'))
    evtsecuanneepreceden = Evtsecurite.objects.filter(Q(dateevt__year = anneecourante-1), Q(typeevt = 'FDG'))
    
    nbreevtsecuanneecourante = evtsecuanneecourante.count()
    nbreevtsecuanneepreceden = evtsecuanneepreceden.count()
        
    
    return render(request, 'aerodromes/evenementsSecurite/feuxnalaser.html', {
    'anneecourante': anneecourante,
    'anneepreceden': anneecourante - 1,
    'evtsecuanneecourante': evtsecuanneecourante,
    'evtsecuanneepreceden': evtsecuanneepreceden,
    'nbreevtsecuanneecourante': nbreevtsecuanneecourante,
    'nbreevtsecuanneepreceden': nbreevtsecuanneepreceden,
    })

 
@login_required
def afficherpsc(request):
	inspections = Inspection.objects.filter(Q(codeinsp__icontains='aibd') | Q(codeinsp__icontains='louis') | Q(codeinsp__icontains='tamba') |
	Q(codeinsp__icontains='cap') | Q(codeinsp__icontains='zig'))
	
	
	
	compt2 = 0
	formatteddomaine_inspections = []
	for i in inspections:
		chdomaine = ''
		
		for domaine in i.domaineinsp.all():
			chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
		
		formatteddomaine_inspections.insert(compt2,chdomaine)
		compt2 = compt2 + 1
		
	formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
	formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
	formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
	aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
	
	listeinspection = []
	compteurinsp = 0
	for inspection in inspections:
		inspectionsbonformat = {}
		inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
		inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
		inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
		inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
		inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
		listeinspection.append(inspectionsbonformat)
		compteurinsp = compteurinsp + 1
	
	
	listdominsp = []
	listdomaineaffiches = []
	strdominsp = ''
	
	listdominsp = formatteddomaine_inspections
	strdominsp = ''.join(listdominsp)
	listdominsp = strdominsp.split("-")
	listdominsp = list(dict.fromkeys(listdominsp))
	
	domaineinspections = DomaineInspection.objects.all()
	for domins in domaineinspections:
		if any(domins.nomdomaineinsp in s for s in listdominsp):
			dominsp = {}
			dominsp['domaineinspection'] = domins.nomdomaineinsp
			dominsp['chklstdomaineinspection'] = domins.checklistdomaineinsp
			listdomaineaffiches.append(dominsp)
	
	
	form = ChoixdepartementForm()	
		
	
	
	return render(request, 'aerodromes/inspections/psc.html', {
	
	'listeinspection' : listeinspection,
	'listdomaineaffiches' : listdomaineaffiches,
	'inspections' : inspections,
	'form': form,
	
	})
	

def contient(machaine, grandechaine):
	if machaine.lower() in grandechaine.lower():
		return True
	else:
		return False
	
	
		
@login_required
def afficherpscaibd(request):
	
	inspections = Inspection.objects.filter(codeinsp__icontains='aibd')
	
	compt2 = 0
	formatteddomaine_inspections = []
	for i in inspections:
		chdomaine = ''
		
		for domaine in i.domaineinsp.all():
			chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
		
		formatteddomaine_inspections.insert(compt2,chdomaine)
		compt2 = compt2 + 1
		
	formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
	formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
	formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
	aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
	
	listeinspection = []
	compteurinsp = 0
	for inspection in inspections:
		inspectionsbonformat = {}
		inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
		inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
		inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
		inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
		inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
		listeinspection.append(inspectionsbonformat)
		compteurinsp = compteurinsp + 1
	
	
	return render(request, 'aerodromes/inspections/pscaibd.html', {
	
	'listeinspection' : listeinspection,
		
	})
	
	
	
@login_required
def afficherpscrcentre(request):
	
	inspections = Inspection.objects.filter(codeinsp__icontains='centre')
	
	compt2 = 0
	formatteddomaine_inspections = []
	for i in inspections:
		chdomaine = ''
		
		for domaine in i.domaineinsp.all():
			chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
		
		formatteddomaine_inspections.insert(compt2,chdomaine)
		compt2 = compt2 + 1
		
	formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
	formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
	formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
	aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
	
	listeinspection = []
	compteurinsp = 0
	for inspection in inspections:
		inspectionsbonformat = {}
		inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
		inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
		inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
		inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
		inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
		listeinspection.append(inspectionsbonformat)
		compteurinsp = compteurinsp + 1
	
	
	return render(request, 'aerodromes/inspections/pscrparaero.html', {
	
	'listeinspection' : listeinspection,
		
	})
	
	
 
@login_required
def afficherpscslouis(request):
	
	inspections = Inspection.objects.filter(codeinsp__icontains='loui')
	
	compt2 = 0
	formatteddomaine_inspections = []
	for i in inspections:
		chdomaine = ''
		
		for domaine in i.domaineinsp.all():
			chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
		
		formatteddomaine_inspections.insert(compt2,chdomaine)
		compt2 = compt2 + 1
		
	formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
	formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
	formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
	aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
	
	listeinspection = []
	compteurinsp = 0
	for inspection in inspections:
		inspectionsbonformat = {}
		inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
		inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
		inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
		inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
		inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
		listeinspection.append(inspectionsbonformat)
		compteurinsp = compteurinsp + 1
	
	
	return render(request, 'aerodromes/inspections/pscaibd.html', {
	
	'listeinspection' : listeinspection,
		
	})
	
	
	
	
@login_required
def afficherpscrnord(request):
	
	inspections = Inspection.objects.filter(codeinsp__icontains='nord')
	
	compt2 = 0
	formatteddomaine_inspections = []
	for i in inspections:
		chdomaine = ''
		
		for domaine in i.domaineinsp.all():
			chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
		
		formatteddomaine_inspections.insert(compt2,chdomaine)
		compt2 = compt2 + 1
		
	formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
	formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
	formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
	aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
	
	listeinspection = []
	compteurinsp = 0
	for inspection in inspections:
		inspectionsbonformat = {}
		inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
		inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
		inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
		inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
		inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
		listeinspection.append(inspectionsbonformat)
		compteurinsp = compteurinsp + 1
	
	
	return render(request, 'aerodromes/inspections/pscrparaero.html', {
	
	'listeinspection' : listeinspection,
		
	})


	
@login_required	
def afficherpsctamb(request):
	
	inspections = Inspection.objects.filter(codeinsp__icontains='tamb')
	
	compt2 = 0
	formatteddomaine_inspections = []
	for i in inspections:
		chdomaine = ''
		
		for domaine in i.domaineinsp.all():
			chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
		
		formatteddomaine_inspections.insert(compt2,chdomaine)
		compt2 = compt2 + 1
		
	formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
	formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
	formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
	aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
	
	listeinspection = []
	compteurinsp = 0
	for inspection in inspections:
		inspectionsbonformat = {}
		inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
		inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
		inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
		inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
		inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
		listeinspection.append(inspectionsbonformat)
		compteurinsp = compteurinsp + 1
	
	
	return render(request, 'aerodromes/inspections/pscaibd.html', {
	
	'listeinspection' : listeinspection,
		
	})
	
	
	
@login_required	
def afficherpscrest(request):
	
	inspections = Inspection.objects.filter(codeinsp__icontains='est')
	
	compt2 = 0
	formatteddomaine_inspections = []
	for i in inspections:
		chdomaine = ''
		
		for domaine in i.domaineinsp.all():
			chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
		
		formatteddomaine_inspections.insert(compt2,chdomaine)
		compt2 = compt2 + 1
		
	formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
	formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
	formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
	aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
	
	listeinspection = []
	compteurinsp = 0
	for inspection in inspections:
		inspectionsbonformat = {}
		inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
		inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
		inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
		inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
		inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
		listeinspection.append(inspectionsbonformat)
		compteurinsp = compteurinsp + 1
	
	
	return render(request, 'aerodromes/inspections/pscrparaero.html', {
	
	'listeinspection' : listeinspection,
		
	})	

	

@login_required
def afficherpsccap(request):
	
	inspections = Inspection.objects.filter(codeinsp__icontains='cap')
	
	compt2 = 0
	formatteddomaine_inspections = []
	for i in inspections:
		chdomaine = ''
		
		for domaine in i.domaineinsp.all():
			chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
		
		formatteddomaine_inspections.insert(compt2,chdomaine)
		compt2 = compt2 + 1
		
	formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
	formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
	formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
	aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
	
	listeinspection = []
	compteurinsp = 0
	for inspection in inspections:
		inspectionsbonformat = {}
		inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
		inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
		inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
		inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
		inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
		listeinspection.append(inspectionsbonformat)
		compteurinsp = compteurinsp + 1
	
	
	return render(request, 'aerodromes/inspections/pscaibd.html', {
	
	'listeinspection' : listeinspection,
		
	})
	
	
	
@login_required
def afficherpscrsud(request):
	
	inspections = Inspection.objects.filter(codeinsp__icontains='sud')
	
	compt2 = 0
	formatteddomaine_inspections = []
	for i in inspections:
		chdomaine = ''
		
		for domaine in i.domaineinsp.all():
			chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
		
		formatteddomaine_inspections.insert(compt2,chdomaine)
		compt2 = compt2 + 1
		
	formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
	formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
	formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
	aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
	
	listeinspection = []
	compteurinsp = 0
	for inspection in inspections:
		inspectionsbonformat = {}
		inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
		inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
		inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
		inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
		inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
		listeinspection.append(inspectionsbonformat)
		compteurinsp = compteurinsp + 1
	
	
	return render(request, 'aerodromes/inspections/pscrparaero.html', {
	
	'listeinspection' : listeinspection,
		
	})
	
	

def afficherpsczig(request):
	
	inspections = Inspection.objects.filter(codeinsp__icontains='zig')
	
	compt2 = 0
	formatteddomaine_inspections = []
	for i in inspections:
		chdomaine = ''
		
		for domaine in i.domaineinsp.all():
			chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
		
		formatteddomaine_inspections.insert(compt2,chdomaine)
		compt2 = compt2 + 1
		
	formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
	formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
	formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
	aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
	
	listeinspection = []
	compteurinsp = 0
	for inspection in inspections:
		inspectionsbonformat = {}
		inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
		inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
		inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
		inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
		inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
		listeinspection.append(inspectionsbonformat)
		compteurinsp = compteurinsp + 1
	
	
	return render(request, 'aerodromes/inspections/pscaibd.html', {
	
	'listeinspection' : listeinspection,
		
	})
	
	 
@login_required
def afficherpscr(request):
	inspections = Inspection.objects.all()
	inspections = inspections.exclude(codeinsp__icontains='aibd')
	inspections = inspections.exclude(codeinsp__icontains='louis')
	inspections = inspections.exclude(codeinsp__icontains='tamba')
	inspections = inspections.exclude(codeinsp__icontains='cap')
	inspections = inspections.exclude(codeinsp__icontains='zig')
	
		
	
	compt2 = 0
	formatteddomaine_inspections = []
	for i in inspections:
		chdomaine = ''
		
		for domaine in i.domaineinsp.all():
			chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
		
		formatteddomaine_inspections.insert(compt2,chdomaine)
		compt2 = compt2 + 1
		
	formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
	formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
	formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
	aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
	
	listeinspection = []
	compteurinsp = 0
	for inspection in inspections:
		inspectionsbonformat = {}
		inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
		inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
		inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
		inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
		inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
		listeinspection.append(inspectionsbonformat)
		compteurinsp = compteurinsp + 1
	
	
	listdominsp = []
	listdomaineaffiches = []
	strdominsp = ''
	
	listdominsp = formatteddomaine_inspections
	strdominsp = ''.join(listdominsp)
	listdominsp = strdominsp.split("-")
	listdominsp = list(dict.fromkeys(listdominsp))
	
	domaineinspections = DomaineInspection.objects.all()
	for domins in domaineinspections:
		if any(domins.nomdomaineinsp in s for s in listdominsp):
			dominsp = {}
			dominsp['domaineinspection'] = domins.nomdomaineinsp
			dominsp['chklstdomaineinspection'] = domins.checklistdomaineinsp
			listdomaineaffiches.append(dominsp)
	
	
	form = ChoixdepartementForm()	
		
	
	return render(request, 'aerodromes/inspections/regionaux.html', {
	
	'listeinspection' : listeinspection,
	'listdomaineaffiches' : listdomaineaffiches,
	'inspections' : inspections,
	'form': form,
	
	})
	

@login_required
def afficherrealise(request):
	
	inspectionsrealises = Inspection.objects.filter(insprealisee=True)
	insprealiseaerointern = Inspection.objects.filter(Q(insprealisee=True),
	Q(codeinsp__icontains='aibd') | Q(codeinsp__icontains='louis') | Q(codeinsp__icontains='tamba') |
	Q(codeinsp__icontains='cap') | Q(codeinsp__icontains='zig'))
	
	nombreinspaerointern = insprealiseaerointern.count()
	nombreinspaeroregion = inspectionsrealises.count() - nombreinspaerointern
	nombreinspperiodique = Inspection.objects.filter(Q(insprealisee=True), Q(typeinsp='PER')).count()
	nombreinspecinopinee = Inspection.objects.filter(Q(insprealisee=True), Q(typeinsp='INO')).count()
	nombreinspectioautre = Inspection.objects.filter(Q(insprealisee=True), Q(typeinsp='AUT')).count()
	
	form = DossierinspectionForm()
		
		
	return render(request, 'aerodromes/inspections/realise.html', {
	'inspectionsrealises' : inspectionsrealises,
	'form' : form,
	'nombreinspaerointern' : nombreinspaerointern,
	'nombreinspaeroregion' : nombreinspaeroregion,
	'nombreinspperiodique' : nombreinspperiodique,
	'nombreinspecinopinee' : nombreinspecinopinee,
	'nombreinspectioautre' : nombreinspectioautre,
		
	})
	
	


@login_required
def afficherformationsrealisees(request):
	
	formationsrealisees = Formationac.objects.filter(realiseform=True)
	
	
	form = DossierformationForm()
			
	return render(request, 'aerodromes/planformations/formationsrealisees.html', {
	'formationsrealisees' : formationsrealisees,
	'form' : form,
	
		
	})
	
	
	

@login_required
def afficherprioriteformations(request):
	
	formations = Formationac.objects.all()
	
	
	formattedcode_formations = [format(formation.codeform) for formation in formations]
	formatteddebut_formations = [format(formation.debutforma) for formation in formations]
	formattedfin_formations = [format(formation.finforma) for formation in formations]
	formattednom_formations = [format(formation.nomform) for formation in formations]
	formattedlieu_formations = [format(formation.lieuforma) for formation in formations]
	formatteddep_formations = [format(formation.agentaformer.serviceac.departementac.nomdep) for formation in formations]
	formattedmatriag_formations = [format(formation.agentaformer.matriculeag ) for formation in formations]
	formattednomag_formations = [format(formation.agentaformer.nomag ) for formation in formations]
	formattednaissag_formations = [format(formation.agentaformer.naissanceag ) for formation in formations]
	formattedperiod_formations = [format(formation.periodicform) for formation in formations]
	formattedcout_formations = [format(formation.coutform) for formation in formations]
	formattedspecif_formations = [format(formation.specialiteform) for formation in formations]
	
	dateaujourdhui = datetime.today().year   
	"""difference = datetime.strptime(formatteddebut_formations[0], '%Y-%m-%d').year"""
	
	
	formationsprios = []
	
	compteurinsp = 0
	for forma in formations:
		priosbonformat = {}
		special = 0
		prioage = 0
		prioperiod = 0
		priosbonformat['codeform'] = formattedcode_formations[compteurinsp]
		priosbonformat['debutforma'] = formatteddebut_formations[compteurinsp]
		priosbonformat['finforma'] = formattedfin_formations[compteurinsp]
		priosbonformat['nomform'] = formattednom_formations[compteurinsp]
		priosbonformat['lieuforma'] = formattedlieu_formations[compteurinsp]
		priosbonformat['depform'] = formatteddep_formations[compteurinsp]
		priosbonformat['matriform'] = formattedmatriag_formations[compteurinsp]
		priosbonformat['nomag'] = formattednomag_formations[compteurinsp]
		priosbonformat['naissag'] = formattednaissag_formations[compteurinsp]
		priosbonformat['periodicform'] = formattedperiod_formations[compteurinsp]
		priosbonformat['coutform'] = formattedcout_formations[compteurinsp]
		priosbonformat['specialiteform'] = formattedspecif_formations[compteurinsp]
		if priosbonformat['specialiteform'] == 'True':
			special = 5
		if int(dateaujourdhui) - int(datetime.strptime(priosbonformat['naissag'], '%Y-%m-%d').year) <= 55:
			prioage = int(dateaujourdhui) - int(datetime.strptime(priosbonformat['naissag'], '%Y-%m-%d').year) 
		if prioperiod != 0:
			prioperiod = int(priosbonformat['periodicform']) - int(datetime.strptime(priosbonformat['debutforma'], '%Y-%m-%d').year) + int(dateaujourdhui)
		priocout = 20/float(priosbonformat['coutform'])
		
		priosbonformat['priorite'] = round((special + prioperiod + prioage + priocout),2)
		
		formationsprios.append(priosbonformat)
		compteurinsp = compteurinsp + 1
			
				
	return render(request, 'aerodromes/planformations/prioriteformations.html', {
	'formationsprios' : formationsprios,
	
		
	})
	
	
	
@login_required
def afficherlisteinspecteurs(request):
	
	listeinspecteurs = Agentac.objects.all()
	
		
	form = DossieragentForm()
		
		
	return render(request, 'aerodromes/planformations/listeinspecteurs.html', {
	'listeinspecteurs' : listeinspecteurs,
	'form' : form,
	
		
	})




@login_required
def afficherdossierinspection(request):
	if request.method == 'POST':
		
		form = DossierinspectionForm(request.POST)
		if form.is_valid():
			codeinspectionaffichee = form.cleaned_data['codeinspection'].codeinsp
			documentsinspection = Dossierinspection.objects.filter(codeinspection__codeinsp=codeinspectionaffichee)
			
			return render(request, 'aerodromes/inspections/dossierinspection.html', {
			'documentsinspection' : documentsinspection,
			'codeinspectionaffichee' : codeinspectionaffichee,
			
			})



@login_required
def afficherdossierformation(request):
	if request.method == 'POST':
		
		form = DossierformationForm(request.POST)
		if form.is_valid():
			codeformationaffichee = form.cleaned_data['codeformation'].codeform
			documentsformation = Dossierformation.objects.filter(codeformation__codeform=codeformationaffichee)
			
			return render(request, 'aerodromes/planformations/dossierformation.html', {
			'documentsformation' : documentsformation,
			'codeformationaffichee' : codeformationaffichee,
			
			})




@login_required
def afficherdossierinspecteur(request):
	if request.method == 'POST':
		
		form = DossieragentForm(request.POST)
		if form.is_valid():
			matriculeagentaffiche = form.cleaned_data['codeagent'].matriculeag
			documentsagent = Dossieragent.objects.filter(codeagent__matriculeag=matriculeagentaffiche)
			
			return render(request, 'aerodromes/planformations/dossierinspecteur.html', {
			'documentsagent' : documentsagent,
			'matriculeagentaffiche' : matriculeagentaffiche,
			
			})






@login_required
def afficherdossierevenementsecu(request):
	if request.method == 'POST':
		
		form = DossierevenementsecuForm(request.POST)
		if form.is_valid():
			codeevtaffiche = form.cleaned_data['codeevenementsecu'].codeevt
			documentsevt = Dossierevenementsecu.objects.filter(codeevenementsecu__codeevt=codeevtaffiche)
			
			return render(request, 'aerodromes/evenementsSecurite/dossierevt.html', {
			'documentsevt' : documentsevt,
			'codeevtaffiche' : codeevtaffiche,
			
			})




@login_required
def afficherdossieraerodrome(request):
	if request.method == 'POST':
		
		form = DossieraerodromeForm(request.POST)
		if form.is_valid():
			nomaeroaffiche = form.cleaned_data['codeaerodrome'].nomaero
			statutaero = form.cleaned_data['codeaerodrome'].statutaero
			documentsaerodrome = Dossieraerodrome.objects.filter(codeaerodrome__nomaero=nomaeroaffiche)
			
			return render(request, 'aerodromes/dossieraerodrome.html', {
			'documentsaerodrome' : documentsaerodrome,
			'nomaeroaffiche' : nomaeroaffiche,
			'statutaero' : statutaero,
			
			})




	
@login_required
def afficheraerodromesSenegal(request):
	
	
	aerodromesSenegal = Aerodrome.objects.all()
	
	formatted_aerodromesSenegal = [format(aerodsene.codeoaciaero) for aerodsene in aerodromesSenegal]
	formattednomaero_aerodromesSenegal = [format(aerodsene.nomaero) for aerodsene in aerodromesSenegal]
	formattedlocaliteaero_aerodromesSenegal = [format(aerodsene.localiteaero) for aerodsene in aerodromesSenegal]
	formattedgestaero_aerodromesSenegal = [format(aerodsene.gestionaero) for aerodsene in aerodromesSenegal]
	formattedcontactgestaero_aerodromesSenegal = [format(aerodsene.contactgestionaero) for aerodsene in aerodromesSenegal]
	formattedstatutaero_aerodromesSenegal = [format(aerodsene.statutaero) for aerodsene in aerodromesSenegal]
	formattedconformiteaero_aerodromesSenegal = [format(aerodsene.conformiteaero) for aerodsene in aerodromesSenegal] 
	aerodromedescrip = [format(aerodsene.descripaero) for aerodsene in aerodromesSenegal]
	aerodromeillustr = [format(aerodsene.illustrationaero.url) for aerodsene in aerodromesSenegal]
	
	listeaerodromes = []
	compteurinsp = 0
	for aerodsene in aerodromesSenegal:
		aerodromesbonformat = {}
		aerodromesbonformat['codeaero'] = formatted_aerodromesSenegal[compteurinsp]
		aerodromesbonformat['nomaero'] = formattednomaero_aerodromesSenegal[compteurinsp]
		aerodromesbonformat['localiteaero'] = formattedlocaliteaero_aerodromesSenegal[compteurinsp]
		aerodromesbonformat['gestionaero'] = formattedgestaero_aerodromesSenegal[compteurinsp]
		aerodromesbonformat['contactgestaero'] = formattedcontactgestaero_aerodromesSenegal[compteurinsp]
		aerodromesbonformat['statutaero'] = formattedstatutaero_aerodromesSenegal[compteurinsp]
		aerodromesbonformat['conformiteaero'] = formattedconformiteaero_aerodromesSenegal[compteurinsp]
		aerodromesbonformat['illustrationaero'] = aerodromeillustr[compteurinsp]
		aerodromesbonformat['descripaero'] = aerodromedescrip[compteurinsp]
		listeaerodromes.append(aerodromesbonformat)
		compteurinsp = compteurinsp + 1
		
	
	form = DossieraerodromeForm()
	
	
	return render(request, 'aerodromes/aerodromesSenegal.html', {
	'listeaerodromes' : listeaerodromes,
	'form' : form,
	})
	
	
	

@login_required
def homeplanform(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    
    dateaujourdhui = datetime.now()
    anneecourante = datetime.today().year
    datedebutinspe = dateaujourdhui + timedelta(days=21)
    inspectionsaentamer = Inspection.objects.filter(Q(datedebutinsp__lte=datedebutinspe),Q(inspentamee=False))
    nombrenotifications = inspectionsaentamer.count()
    formations = Formationac.objects.filter(Q(typeformation='PLG'))
    realisationformation = 0
    formationsrealisees = Formationac.objects.filter(Q(realiseform=True))
    if (formations.count() != 0):
    	realisationformation = 100 * (formationsrealisees.count()/formations.count())
    
    inspections = Inspection.objects.filter(Q(typeinsp='PER'), Q(datedebutinsp__year = anneecourante))
    realisationinspection = 0
    inspectionsrealisees = Inspection.objects.filter(Q(insprealisee=True), Q(datedebutinsp__year = anneecourante))
    if (inspections.count() != 0):
    	realisationinspection = 100 * (inspectionsrealisees.count()/inspections.count())
    
    evtsecuanneecourante = Evtsecurite.objects.filter(Q(dateevt__year = anneecourante))
    evtsecuanneepreceden = Evtsecurite.objects.filter(Q(dateevt__year = anneecourante-1))
    
    nbreaerohomologues = Aerodrome.objects.filter(Q(statutaero='HOMOLO')).count()
    nbreaeroahomologue = Aerodrome.objects.filter(Q(statutaero='AHOMOL')).count()
    nbreaerodcertifies = Aerodrome.objects.filter(Q(statutaero='CERTIF')).count()
    nbreaeroacertifier = Aerodrome.objects.filter(Q(statutaero='ACERTI')).count()
    
    nbreevtsecuanneecourante = evtsecuanneecourante.count()
    nbreevtsecuanneepreceden = evtsecuanneepreceden.count()
    
    evetsecu = Evtsecurite.objects.all()
    formattedtypeevts = [format(evt.typeevt) for evt in evtsecuanneecourante]
    
    evtancourpartype = {x:formattedtypeevts.count(x) for x in formattedtypeevts}
    lestypedevt = list(evtancourpartype.keys())
    nbredevpartyp = list(evtancourpartype.values())
    evtstypnbre = []
    cteur = 0
    for i in lestypedevt:
    	bonformat = {}
    	bonformat['typeevt'] = lestypedevt[cteur]
    	bonformat['nbreevt'] = nbredevpartyp[cteur]
    	evtstypnbre.append(bonformat)
    	cteur = cteur + 1
    
    formattedtypeevtsp = [format(evt.typeevt) for evt in evtsecuanneepreceden]
    formattedmoisevent = [format(evt.dateevt.month) for evt in evtsecuanneecourante]
    formattedmoiseventp = [format(evt.dateevt.month) for evt in evtsecuanneepreceden]
    
    evtanpparmois = {x:formattedmoiseventp.count(x) for x in formattedmoiseventp}
    lesmoisdevtp = list(evtanpparmois.keys())
    nbredevanpparmois = list(evtanpparmois.values())
    evtsnbreparmoisp = []
    cteur = 0
    for i in lesmoisdevtp:
    	bonformatmoisp = {}
    	bonformatmoisp['moisevtp'] = lesmoisdevtp[cteur]
    	bonformatmoisp['nbreevtmoisp'] = nbredevanpparmois[cteur]
    	evtsnbreparmoisp.append(bonformatmoisp)
    	cteur = cteur + 1
    
    evtancparmois = {x:formattedmoisevent.count(x) for x in formattedmoisevent}
    lesmoisdevt = list(evtancparmois.keys())
    nbredevancparmois = list(evtancparmois.values())
    evtsnbreparmois = []
    cteur = 0
    for i in lesmoisdevt:
    	bonformatmois = {}
    	bonformatmois['moisevt'] = lesmoisdevt[cteur]
    	bonformatmois['nbreevtmois'] = nbredevancparmois[cteur]
    	evtsnbreparmois.append(bonformatmois)
    	cteur = cteur + 1
    	
    evtsnbreparmois = sorted(evtsnbreparmois, key = lambda i: i['moisevt'])
    
    evtanppartype = {x:formattedtypeevtsp.count(x) for x in formattedtypeevtsp}
    lestypedevtp = list(evtanppartype.keys())
    nbredevpartypp = list(evtanppartype.values())
    evtsptypnbre = []
    cteur = 0
    for i in lestypedevtp:
    	bonformatp = {}
    	bonformatp['typeevt'] = lestypedevtp[cteur]
    	bonformatp['nbreevt'] = nbredevpartypp[cteur]
    	evtsptypnbre.append(bonformatp)
    	cteur = cteur + 1
    
    
    return render(request, 'aerodromes/planformations/accueil.html', {
    'dateaujourdhui' : dateaujourdhui,
    'datedebutinspe' : datedebutinspe,
    'nombrenotifications' : nombrenotifications,
    'inspectionsaentamer' : inspectionsaentamer,
    'realisationformation': round(realisationformation, 2),
    'realisationinspection': round(realisationinspection, 2),
    'nbreevtsecuanneecourante': nbreevtsecuanneecourante,
    'nbreevtsecuanneepreceden': nbreevtsecuanneepreceden,
    'anneecourante': anneecourante,
    'anneepassee': anneecourante-1,
    'evetsecu': evetsecu,
    'evtstypnbre': evtstypnbre,
    'evtsptypnbre': evtsptypnbre,
    'evtsnbreparmois': evtsnbreparmois,
    'evtsnbreparmoisp': evtsnbreparmoisp,
    'formattedmoisevent': formattedmoisevent,
    'nbreaerohomologues': nbreaerohomologues,
    'nbreaeroahomologue': nbreaeroahomologue,
    'nbreaerodcertifies': nbreaerodcertifies,
    'nbreaeroacertifier': nbreaeroacertifier,
    'nbreinitialacertif': nbreaerodcertifies + nbreaeroacertifier,
    'nbreinitialahomolo': nbreaeroahomologue + nbreaerohomologues,
      
       
    
    })

@login_required
def afficherplanning(request):
	
	formations = Formationac.objects.all()
	formattedcode_formations = [format(formation.codeform) for formation in formations]
	formattednom_formations = [format(formation.nomform) for formation in formations]
	formatteddebut_formations = [format(formation.debutforma) for formation in formations]
	formattedfin_formations = [format(formation.finforma) for formation in formations]
	formattedmatricule_formations = [format(formation.agentaformer.matriculeag) for formation in formations]
	formattedlieufor_formations = [format(formation.lieuforma) for formation in formations]
	
	
	listmatriculeinspecteurs = []
	for matricule in formattedmatricule_formations:
		if matricule not in listmatriculeinspecteurs:
			listmatriculeinspecteurs.append(matricule)
	
	listeinspecteurs = []
	
	for matri in listmatriculeinspecteurs:
		for agent in Agentac.objects.all():
			if agent.matriculeag == matri:
				formationsbonformatag = {}
				formationsbonformatag['matriculebf'] = agent.matriculeag
				formationsbonformatag['nomagbf'] = agent.nomag
				formationsbonformatag['prenomsagbf'] = agent.prenomsag
				listeinspecteurs.append(formationsbonformatag)
				
			
	form = ChoixdepartementForm()
	
	formationimpactees = []
	
	nbrechevauchements = 0
	nbreformations = len(formations)
	for i in range(nbreformations-1):
		for j in range(i,nbreformations-1):
			if (datetime.strptime(formattedfin_formations[i], '%Y-%m-%d') >= datetime.strptime(formatteddebut_formations[j+1],'%Y-%m-%d')) and (datetime.strptime(formattedfin_formations[j+1],'%Y-%m-%d') >= datetime.strptime(formatteddebut_formations[i],'%Y-%m-%d')):
				nbrechevauchements = nbrechevauchements + 1
				formaimpactees = {}
				formaimpactees['debut1'] = formatteddebut_formations[i]
				formaimpactees['fin1'] = formattedfin_formations[i]
				formaimpactees['code1'] = formattedcode_formations[i]
				formaimpactees['matricule1'] = formattedmatricule_formations[i]
				formaimpactees['debut2'] = formatteddebut_formations[j+1]
				formaimpactees['fin2'] = formattedfin_formations[j+1]
				formaimpactees['code2'] = formattedcode_formations[j+1]
				formaimpactees['matricule2'] = formattedmatricule_formations[j+1]
				formationimpactees.append(formaimpactees)			
				
		
	listeformations = []
	compteurinsp = 0
	for formation in formations:
		formationsbonformat = {}
		formationsbonformat['codeform'] = formattedcode_formations[compteurinsp]
		formationsbonformat['nomform'] = formattednom_formations[compteurinsp]
		formationsbonformat['debutform'] = formatteddebut_formations[compteurinsp]
		formationsbonformat['finform'] = formattedfin_formations[compteurinsp]
		formationsbonformat['matriculeform'] = formattedmatricule_formations[compteurinsp]
		formationsbonformat['lieuformbf'] = formattedlieufor_formations[compteurinsp]
		listeformations.append(formationsbonformat)
		compteurinsp = compteurinsp + 1
		
	return render(request, 'aerodromes/planformations/planningforma.html', {
	'listeformations' : listeformations,
	'form': form,
	'listeinspecteurs': listeinspecteurs,
	'nbrechevauchements': nbrechevauchements,
	'formationimpactees': formationimpactees,
	
	
	})
	


@login_required
def afficherformationsdepartement(request):
	if request.method == 'POST':
		
		form = ChoixdepartementForm(request.POST)
		
		if form.is_valid():
			departementencharge = form.cleaned_data['departement'].nomdep
			formations = Formationac.objects.filter(Q(agentaformer__serviceac__departementac__nomdep = departementencharge))
			
			
			formattedcode_formations = [format(formation.codeform) for formation in formations]
			formatteddebut_formations = [format(formation.debutforma) for formation in formations]
			formattedfin_formations = [format(formation.finforma) for formation in formations]
			formattedmatricule_formations = [format(formation.agentaformer.matriculeag) for formation in formations]
			formattednomfor_formations = [format(formation.nomform) for formation in formations]
			formattedlieufor_formations = [format(formation.lieuforma) for formation in formations]
			
			
			formationimpactees = []
			nbrechevauchements = 0
			nbreformations = len(formations)
			for i in range(nbreformations-1):
				for j in range(i,nbreformations-1):
					if (datetime.strptime(formattedfin_formations[i], '%Y-%m-%d') >= datetime.strptime(formatteddebut_formations[j+1],'%Y-%m-%d')) and (datetime.strptime(formattedfin_formations[j+1],'%Y-%m-%d') >= datetime.strptime(formatteddebut_formations[i],'%Y-%m-%d')):
						nbrechevauchements = nbrechevauchements + 1
						formaimpactees = {}
						formaimpactees['debut1'] = formatteddebut_formations[i]
						formaimpactees['fin1'] = formattedfin_formations[i]
						formaimpactees['code1'] = formattedcode_formations[i]
						formaimpactees['matricule1'] = formattedmatricule_formations[i]
						formaimpactees['debut2'] = formatteddebut_formations[j+1]
						formaimpactees['fin2'] = formattedfin_formations[j+1]
						formaimpactees['code2'] = formattedcode_formations[j+1]
						formaimpactees['matricule2'] = formattedmatricule_formations[j+1]
						formationimpactees.append(formaimpactees)
									
			
			listmatriculeinspecteurs = []
			for matricule in formattedmatricule_formations:
				if matricule not in listmatriculeinspecteurs:
					listmatriculeinspecteurs.append(matricule)
					
			listeinspecteurs = []
			for matri in listmatriculeinspecteurs:
				for agent in Agentac.objects.all():
					if agent.matriculeag == matri:
						formationsbonformatag = {}
						formationsbonformatag['matriculebf'] = agent.matriculeag
						formationsbonformatag['nomagbf'] = agent.nomag
						formationsbonformatag['prenomsagbf'] = agent.prenomsag
						listeinspecteurs.append(formationsbonformatag)
			
			
			listeformations = []
			compteurinsp = 0
			for formation in formations:
				formationsbonformat = {}
				formationsbonformat['codeformbf'] = formattedcode_formations[compteurinsp]
				formationsbonformat['matriculebf'] = formattedmatricule_formations[compteurinsp]
				formationsbonformat['debutformbf'] = formatteddebut_formations[compteurinsp]
				formationsbonformat['finformbf'] = formattedfin_formations[compteurinsp]
				formationsbonformat['nomformbf'] = formattednomfor_formations[compteurinsp]
				formationsbonformat['lieuformbf'] = formattedlieufor_formations[compteurinsp]
				listeformations.append(formationsbonformat)
				compteurinsp = compteurinsp + 1
			
			return render(request, 'aerodromes/planformations/formationsdepartement.html', {
			'listeformations' : listeformations,
			'form': form,
			'listeinspecteurs': listeinspecteurs,
			'nbrechevauchements': nbrechevauchements,
			'formationimpactees': formationimpactees,
			
			})





@login_required
def afficherinspectionsdepartement(request):
	if request.method == 'POST':
		
		form = ChoixdepartementForm(request.POST)
		
		if form.is_valid():
			departementencharge = form.cleaned_data['departement'].nomdep
			inspections = Inspection.objects.filter(Q(nomdepartement__nomdep = departementencharge),
			Q(codeinsp__icontains='aibd') | Q(codeinsp__icontains='louis') | Q(codeinsp__icontains='tamba') |
			Q(codeinsp__icontains='cap') | Q(codeinsp__icontains='zig'))
			
			compt2 = 0
			formatteddomaine_inspections = []
			for i in inspections:
				chdomaine = ''
				for domaine in i.domaineinsp.all():
					chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
				formatteddomaine_inspections.insert(compt2,chdomaine)
				compt2 = compt2 + 1
			formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
			formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
			formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
			aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
			listeinspection = []
			compteurinsp = 0
			for inspection in inspections:
				inspectionsbonformat = {}
				inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
				inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
				inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
				inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
				inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
				listeinspection.append(inspectionsbonformat)
				compteurinsp = compteurinsp + 1
			listdominsp = []
			listdomaineaffiches = []
			strdominsp = ''
			listdominsp = formatteddomaine_inspections
			strdominsp = ''.join(listdominsp)
			listdominsp = strdominsp.split("-")
			listdominsp = list(dict.fromkeys(listdominsp))
			domaineinspections = DomaineInspection.objects.all()
			for domins in domaineinspections:
				if any(domins.nomdomaineinsp in s for s in listdominsp):
					dominsp = {}
					dominsp['domaineinspection'] = domins.nomdomaineinsp
					dominsp['chklstdomaineinspection'] = domins.checklistdomaineinsp
					listdomaineaffiches.append(dominsp)
			return render(request, 'aerodromes/inspections/pscdepartement.html', {
			'listeinspection' : listeinspection,
			'listdomaineaffiches' : listdomaineaffiches,
			'inspections' : inspections,
			'form': form,
			
			})
			


@login_required
def afficherinspectionsrdepartement(request):
	if request.method == 'POST':
		
		form = ChoixdepartementForm(request.POST)
		
		if form.is_valid():
			departementencharge = form.cleaned_data['departement'].nomdep
			
			
			inspections = Inspection.objects.filter(Q(nomdepartement__nomdep = departementencharge),
			~Q(codeinsp__icontains='aibd'), ~Q(codeinsp__icontains='louis'), ~Q(codeinsp__icontains='tamba'),
			~Q(codeinsp__icontains='cap'), ~Q(codeinsp__icontains='zig')
			
			)
			
						
			
			compt2 = 0
			formatteddomaine_inspections = []
			for i in inspections:
				chdomaine = ''
				for domaine in i.domaineinsp.all():
					chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
				formatteddomaine_inspections.insert(compt2,chdomaine)
				compt2 = compt2 + 1
			formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
			formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
			formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
			aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
			listeinspection = []
			compteurinsp = 0
			for inspection in inspections:
				inspectionsbonformat = {}
				inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
				inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
				inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
				inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
				inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
				listeinspection.append(inspectionsbonformat)
				compteurinsp = compteurinsp + 1
			listdominsp = []
			listdomaineaffiches = []
			strdominsp = ''
			listdominsp = formatteddomaine_inspections
			strdominsp = ''.join(listdominsp)
			listdominsp = strdominsp.split("-")
			listdominsp = list(dict.fromkeys(listdominsp))
			domaineinspections = DomaineInspection.objects.all()
			for domins in domaineinspections:
				if any(domins.nomdomaineinsp in s for s in listdominsp):
					dominsp = {}
					dominsp['domaineinspection'] = domins.nomdomaineinsp
					dominsp['chklstdomaineinspection'] = domins.checklistdomaineinsp
					listdomaineaffiches.append(dominsp)
			return render(request, 'aerodromes/inspections/pscrdepartement.html', {
			'listeinspection' : listeinspection,
			'listdomaineaffiches' : listdomaineaffiches,
			'inspections' : inspections,
			'form': form,
			
			})
			


			

def afficherpscaibddepart(request):
	if request.method == 'POST':
		
		form = ChoixdepartementForm(request.POST)
		
		if form.is_valid():
			departementencharge = form.cleaned_data['departement'].nomdep
			
			inspections = Inspection.objects.filter(codeinsp__icontains='aibd', nomdepartement__nomdep = departementencharge)
			
					
			
			
			compt2 = 0
			formatteddomaine_inspections = []
			for i in inspections:
				chdomaine = ''
				for domaine in i.domaineinsp.all():
					chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
				formatteddomaine_inspections.insert(compt2,chdomaine)
				compt2 = compt2 + 1
			formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
			formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
			formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
			aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
			listeinspection = []
			compteurinsp = 0
			for inspection in inspections:
				inspectionsbonformat = {}
				inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
				inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
				inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
				inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
				inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
				listeinspection.append(inspectionsbonformat)
				compteurinsp = compteurinsp + 1
			listdominsp = []
			listdomaineaffiches = []
			strdominsp = ''
			listdominsp = formatteddomaine_inspections
			strdominsp = ''.join(listdominsp)
			listdominsp = strdominsp.split("-")
			listdominsp = list(dict.fromkeys(listdominsp))
			domaineinspections = DomaineInspection.objects.all()
			for domins in domaineinspections:
				if any(domins.nomdomaineinsp in s for s in listdominsp):
					dominsp = {}
					dominsp['domaineinspection'] = domins.nomdomaineinsp
					dominsp['chklstdomaineinspection'] = domins.checklistdomaineinsp
					listdomaineaffiches.append(dominsp)
			return render(request, 'aerodromes/inspections/pscdepartementaero.html', {
			'listeinspection' : listeinspection,
			'listdomaineaffiches' : listdomaineaffiches,
			'inspections' : inspections,
			'form': form,
			
			})
	

	

@login_required
def afficherpscslouisdepart(request):
	if request.method == 'POST':
		
		form = ChoixdepartementForm(request.POST)
		
		if form.is_valid():
			departementencharge = form.cleaned_data['departement'].nomdep
			
			inspections = Inspection.objects.filter(codeinsp__icontains='louis', nomdepartement__nomdep = departementencharge)
			
						
			compt2 = 0
			formatteddomaine_inspections = []
			for i in inspections:
				chdomaine = ''
				for domaine in i.domaineinsp.all():
					chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
				formatteddomaine_inspections.insert(compt2,chdomaine)
				compt2 = compt2 + 1
			formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
			formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
			formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
			aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
			listeinspection = []
			compteurinsp = 0
			for inspection in inspections:
				inspectionsbonformat = {}
				inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
				inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
				inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
				inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
				inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
				listeinspection.append(inspectionsbonformat)
				compteurinsp = compteurinsp + 1
			listdominsp = []
			listdomaineaffiches = []
			strdominsp = ''
			listdominsp = formatteddomaine_inspections
			strdominsp = ''.join(listdominsp)
			listdominsp = strdominsp.split("-")
			listdominsp = list(dict.fromkeys(listdominsp))
			domaineinspections = DomaineInspection.objects.all()
			for domins in domaineinspections:
				if any(domins.nomdomaineinsp in s for s in listdominsp):
					dominsp = {}
					dominsp['domaineinspection'] = domins.nomdomaineinsp
					dominsp['chklstdomaineinspection'] = domins.checklistdomaineinsp
					listdomaineaffiches.append(dominsp)
			return render(request, 'aerodromes/inspections/pscdepartementaero.html', {
			'listeinspection' : listeinspection,
			'listdomaineaffiches' : listdomaineaffiches,
			'inspections' : inspections,
			'form': form,
			
			})


	
@login_required
def afficherpsctambdepart(request):
	if request.method == 'POST':
		
		form = ChoixdepartementForm(request.POST)
		
		if form.is_valid():
			departementencharge = form.cleaned_data['departement'].nomdep
			
			inspections = Inspection.objects.filter(codeinsp__icontains='tamba', nomdepartement__nomdep = departementencharge)
			
			
					
			
			compt2 = 0
			formatteddomaine_inspections = []
			for i in inspections:
				chdomaine = ''
				for domaine in i.domaineinsp.all():
					chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
				formatteddomaine_inspections.insert(compt2,chdomaine)
				compt2 = compt2 + 1
			formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
			formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
			formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
			aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
			listeinspection = []
			compteurinsp = 0
			for inspection in inspections:
				inspectionsbonformat = {}
				inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
				inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
				inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
				inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
				inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
				listeinspection.append(inspectionsbonformat)
				compteurinsp = compteurinsp + 1
			listdominsp = []
			listdomaineaffiches = []
			strdominsp = ''
			listdominsp = formatteddomaine_inspections
			strdominsp = ''.join(listdominsp)
			listdominsp = strdominsp.split("-")
			listdominsp = list(dict.fromkeys(listdominsp))
			domaineinspections = DomaineInspection.objects.all()
			for domins in domaineinspections:
				if any(domins.nomdomaineinsp in s for s in listdominsp):
					dominsp = {}
					dominsp['domaineinspection'] = domins.nomdomaineinsp
					dominsp['chklstdomaineinspection'] = domins.checklistdomaineinsp
					listdomaineaffiches.append(dominsp)
			return render(request, 'aerodromes/inspections/pscdepartementaero.html', {
			'listeinspection' : listeinspection,
			'listdomaineaffiches' : listdomaineaffiches,
			'inspections' : inspections,
			'form': form,
			
			})

	
	
@login_required
def afficherpsccapdepart(request):
	if request.method == 'POST':
		
		form = ChoixdepartementForm(request.POST)
		
		if form.is_valid():
			departementencharge = form.cleaned_data['departement'].nomdep
			
			inspections = Inspection.objects.filter(codeinsp__icontains='cap', nomdepartement__nomdep = departementencharge)
			
							
			compt2 = 0
			formatteddomaine_inspections = []
			for i in inspections:
				chdomaine = ''
				for domaine in i.domaineinsp.all():
					chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
				formatteddomaine_inspections.insert(compt2,chdomaine)
				compt2 = compt2 + 1
			formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
			formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
			formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
			aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
			listeinspection = []
			compteurinsp = 0
			for inspection in inspections:
				inspectionsbonformat = {}
				inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
				inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
				inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
				inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
				inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
				listeinspection.append(inspectionsbonformat)
				compteurinsp = compteurinsp + 1
			listdominsp = []
			listdomaineaffiches = []
			strdominsp = ''
			listdominsp = formatteddomaine_inspections
			strdominsp = ''.join(listdominsp)
			listdominsp = strdominsp.split("-")
			listdominsp = list(dict.fromkeys(listdominsp))
			domaineinspections = DomaineInspection.objects.all()
			for domins in domaineinspections:
				if any(domins.nomdomaineinsp in s for s in listdominsp):
					dominsp = {}
					dominsp['domaineinspection'] = domins.nomdomaineinsp
					dominsp['chklstdomaineinspection'] = domins.checklistdomaineinsp
					listdomaineaffiches.append(dominsp)
			return render(request, 'aerodromes/inspections/pscdepartementaero.html', {
			'listeinspection' : listeinspection,
			'listdomaineaffiches' : listdomaineaffiches,
			'inspections' : inspections,
			'form': form,
			
			})

	
	
@login_required
def afficherpsczigdepart(request):
	if request.method == 'POST':
		
		form = ChoixdepartementForm(request.POST)
		
		if form.is_valid():
			departementencharge = form.cleaned_data['departement'].nomdep
			
			inspections = Inspection.objects.filter(codeinsp__icontains='zig', nomdepartement__nomdep = departementencharge)
					
			
			compt2 = 0
			formatteddomaine_inspections = []
			for i in inspections:
				chdomaine = ''
				for domaine in i.domaineinsp.all():
					chdomaine = chdomaine + '-' + domaine.nomdomaineinsp
				formatteddomaine_inspections.insert(compt2,chdomaine)
				compt2 = compt2 + 1
			formattedcode_inspections = [format(inspection.codeinsp) for inspection in inspections]
			formatteddebut_inspections = [format(inspection.datedebutinsp) for inspection in inspections]
			formattedfin_inspections = [format(inspection.datefininsp) for inspection in inspections]
			aerodromeinsp = [format(inspection.nomaero) for inspection in inspections]
			listeinspection = []
			compteurinsp = 0
			for inspection in inspections:
				inspectionsbonformat = {}
				inspectionsbonformat['codeinspbf'] = formattedcode_inspections[compteurinsp]
				inspectionsbonformat['domaineinspbf'] = formatteddomaine_inspections[compteurinsp]
				inspectionsbonformat['debutinspbf'] = formatteddebut_inspections[compteurinsp]
				inspectionsbonformat['fininspbf'] = formattedfin_inspections[compteurinsp]
				inspectionsbonformat['aerodromeinspbf'] = aerodromeinsp[compteurinsp]
				listeinspection.append(inspectionsbonformat)
				compteurinsp = compteurinsp + 1
			listdominsp = []
			listdomaineaffiches = []
			strdominsp = ''
			listdominsp = formatteddomaine_inspections
			strdominsp = ''.join(listdominsp)
			listdominsp = strdominsp.split("-")
			listdominsp = list(dict.fromkeys(listdominsp))
			domaineinspections = DomaineInspection.objects.all()
			for domins in domaineinspections:
				if any(domins.nomdomaineinsp in s for s in listdominsp):
					dominsp = {}
					dominsp['domaineinspection'] = domins.nomdomaineinsp
					dominsp['chklstdomaineinspection'] = domins.checklistdomaineinsp
					listdomaineaffiches.append(dominsp)
			return render(request, 'aerodromes/inspections/pscdepartementaero.html', {
			'listeinspection' : listeinspection,
			'listdomaineaffiches' : listdomaineaffiches,
			'inspections' : inspections,
			'form': form,
			
			})


@login_required
def afficherdocumentation(request):
	
	listedocuments = Document.objects.all()
	
		
		
	return render(request, 'aerodromes/listedocuments.html', {
	'listedocuments' : listedocuments,
	
		
	})
