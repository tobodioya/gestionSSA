from django.db import models
from django.utils import timezone
from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError


class Directionac(models.Model):
   nomdir = models.CharField(max_length=30)
   descripdir = models.TextField(null=True)
	
   def __str__(self):
      return self.nomdir


class Departementac(models.Model):
   nomdep = models.CharField(max_length=30)
   descripdep = models.TextField(null=True)
   directionac = models.ForeignKey('Directionac', on_delete=models.CASCADE)
	
   def __str__(self):
      return self.nomdep
   	
   	
class Serviceac(models.Model):
   nomser = models.CharField(max_length=30, verbose_name="Nom Service")
   descripser = models.TextField(null=True, verbose_name="Description Service")
   departementac = models.ForeignKey('Departementac', on_delete=models.CASCADE, verbose_name="Département Service")
	
   def __str__(self):
      return self.nomser
   	

class Bureauac(models.Model):
   nombur = models.CharField(max_length=30)
   descripbur = models.TextField(null=True)
   serviceac = models.ForeignKey('Serviceac', on_delete=models.CASCADE)
	
   def __str__(self):
      return self.nombur

	

class Formationac(models.Model):
   codeform = models.CharField(max_length=20, verbose_name="Codification")
   nomform = models.CharField(max_length=30, verbose_name="Intitulé de la formation")
   specialiteform = models.BooleanField(default=True)
   realiseform = models.BooleanField(default=False)
   TYPEFORMATION = (
    ('PLG', 'Planifiée'),
    ('HPL', 'Hors Planning')
   )
   typeformation = models.CharField(max_length=3, choices=TYPEFORMATION,default='PLG', verbose_name="Type")
   PERIODICITE = (
      ('0', '0'),
      ('1', '1'),
      ('2', '2'),
      ('3', '3'),
      ('4', '4'),
      ('5', '5')
    )
   periodicform = models.CharField(max_length=2, choices=PERIODICITE,default='0', verbose_name="Périodicité")
   descripform = models.TextField(null=True, verbose_name="Description")
   debutforma = models.DateField(null=True, verbose_name="Date de début")
   finforma = models.DateField(null=True, verbose_name="Date de fin")
   lieuforma = models.CharField(max_length=30, verbose_name="Lieu de formation")
   agentaformer = models.ForeignKey('Agentac', on_delete=models.CASCADE, verbose_name="Matricule Agent")
   coutform = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Coût Formation en CFA", default=1)
   docdescriptif = models.FileField(upload_to = 'dossiers/formations/%Y/%m/%d/', verbose_name="Document Formation", default='fichierdefaut.pdf')
   
   
   def clean(self):
   	if self.finforma < self.debutforma:
   		raise ValidationError("Les dates de début et de fin de la formation ne sont pas correctes!")	
  
  
   def __str__(self):
      return self.codeform + '-' + self.agentaformer.matriculeag
   
   class Meta:
      ordering = ['debutforma']

				

class Agentac(models.Model):
   matriculeag = models.CharField(max_length=20,verbose_name="Matricule Agent")
   prenomsag = models.CharField(max_length=50, verbose_name="Prénom(s) Agent")
   nomag = models.CharField(max_length=30, verbose_name="Nom Agent")
   fonctionag =  models.CharField(max_length=50, verbose_name="Fonction Agent",default="Inspecteur")
   naissanceag = models.DateField(verbose_name="Date de naissance ")
   lieunaisag = models.CharField(max_length=50, verbose_name="Lieu de naissance", default='Dakar')
   descripag = models.TextField(null=True, verbose_name="Apropos Agent")
   serviceac = models.ForeignKey('Serviceac', on_delete=models.CASCADE, verbose_name="Service Agent")
   photoagent = models.ImageField(upload_to = 'agents/photos/%Y/%m/%d/', verbose_name="Photo", default='fichierdefaut.pdf')
   
   def __str__(self):
   	return self.matriculeag
   	
   class Meta:
   	ordering = ['nomag']




class Dossieragent(models.Model):
	codeagent = models.ForeignKey('Agentac',  on_delete=models.CASCADE, verbose_name="Matricule Agent")
	descriptiondocumentagent = models.TextField(null=True, blank = True, verbose_name="Description Dossier Agent")
	datedocumentagent = models.DateField(verbose_name="Date de production du document ", default='2020-02-13')
	dossieragent = models.FileField(upload_to = 'dossiers/agent/%Y/%m/%d/', verbose_name="Document Agent", default='fichierdefaut.pdf')
	
	def __str__(self):
		return self.descriptiondocumentagent + self.codeagent.matriculeag
		



class Aerodrome(models.Model):
   nomaero = models.CharField(max_length=50,verbose_name="Nom Aérodrome")
   codeoaciaero = models.CharField(max_length=50, verbose_name="Code OACI")
   localiteaero = models.CharField(max_length=50,verbose_name="Localité", default="")
   coordLataero = models.CharField(max_length=30, verbose_name="Latitude ")
   coordLongaero = models.CharField(max_length=30, verbose_name="Longitude ")
   gestionaero = models.CharField(max_length=50,verbose_name="Gestionnaire", default="")
   contactgestionaero = models.CharField(max_length=50,verbose_name="Contact Gestionnaire", default="")
   aerointernational = models.BooleanField(default=False, verbose_name="Aéroport international")
   STATUTAEROS = (
      ('CERTIF', 'Certifié'),
      ('ACERTI', 'A certifier'),
      ('HOMOLO', 'Homologué'),
      ('AHOMOL', 'A homologuer'),
    )
   statutaero = models.CharField(max_length=6, choices=STATUTAEROS)
   conformiteaero =  models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Conformité aérodrome en %", default=0)
   descripaero = models.TextField(null=True, verbose_name="Description Aérodrome")
   illustrationaero = models.FileField(upload_to = 'illustrations/%Y/%m/%d/', verbose_name="Illustrations Aérodrome", default='fichierdefaut.pdf')
		
   def __str__(self):
      return self.nomaero
      
      


class Dossieraerodrome(models.Model):
	codeaerodrome = models.ForeignKey('Aerodrome',  on_delete=models.CASCADE, verbose_name="Nom Aérodrome")
	descriptiondossier = models.TextField(null=True, blank = True, verbose_name="Description Dossier Aérodrome")
	datedoc = models.DateField(verbose_name="Date de production du document ")
	dossieraero = models.FileField(upload_to = 'dossiers/aerodromes/%Y/%m/%d/', verbose_name="Document Aérodrome", default='fichierdefaut.pdf')
	
	def __str__(self):
		return self.codeaerodrome.nomaero + self.descriptiondossier

      
      

class Evtsecurite(models.Model):
	codeevt = models.CharField(max_length=150, editable=False)
	TYPEEVTS = (
		('ANS','Approche non conforme'),
		('PIN', 'Position inusuelle'),
		('ECA', 'Evt lié aux conditions aerodrome'),
		('SAI', 'Mise en oeuvre inadaptée des systèmes aéronef'),
		('TRM', 'Travaux et maintenance'),
		('MCO', 'Mauvaise coordination et opérations sol'),
		('INC', 'Incursion sur piste'),
		('PSV', 'Perte séparation en vol'),
		('PES', 'Pénétration espace'),
		('EXP', 'Exploitation'),
		('PAN', 'Péril animalier dont aviaire'),
		('FDG', 'Feux Dangereux, lasers'),
		('MET', 'Météo'),
		('DIB', 'Défaillance interfaces sol-bord'),
		('EEA', 'Evt relatif entretien aeronef'),
		('FFV', 'Feu-fumée en vol ou au sol'),
		('DSB', 'Défaillance système à bord'),
		('DPR', 'Dépressurisation'),
		('FOD', 'Dommage suite FOD'),
		('AUT', 'Autre'),
	)
	typeevt = models.CharField(max_length=3, choices=TYPEEVTS,verbose_name="Type Evt Sécu")
	lieuevt = models.CharField(max_length=30,verbose_name="Lieu Evt Sécu")
	latitudeevt = models.CharField(max_length=30, verbose_name="Latitude Evt Sécu")
	longitudeevt = models.CharField(max_length=30, verbose_name="Longitude Evt Sécu")
	dateevt = models.DateField(verbose_name="Date Evt Sécu ")
	heureevt = models.TimeField(verbose_name="Heure Evt Sécu ")
	notifiantevt = models.CharField(max_length=30,verbose_name="Notifiant Evt Sécu")
	immataeronefevt = models.CharField(max_length=30, verbose_name="Immatriculation aéronef", default="NA")
	CLASSEEVTS = (
		('INC', 'Incident'),
		('IGR', 'Incident Grave'),
		('ACC', 'Accident'),
		
	)
	classeevt = models.CharField(max_length=3, choices=CLASSEEVTS, verbose_name="Classe Evt", default='INC')
	STATUTEVTS = (
		('ENC', 'Ouvert, analyse en cours'),
		('CAD', 'Clos avec analyse détaillée'),
		('CAS', 'Clos avec analyse sommaire'),
		
	)
	statutevt = models.CharField(max_length=3, choices=STATUTEVTS, verbose_name="Statut Evt", default='ENC')
	GROUPEANIMALEVT = (
		('OIS', 'Oiseaux'),
		('ATA', 'Autre animal'),
		('NEA', 'NA'),
		
	)
	groupeanimalevt = models.CharField(max_length=3, choices=GROUPEANIMALEVT, verbose_name="Groupe animal Evt", default='NEA')
	nomanimalevt = models.CharField(max_length=30,verbose_name="Nom animal Evt Sécu",default='NA')
	nomaero = models.ForeignKey('Aerodrome', on_delete=models.CASCADE, verbose_name="Aérodrome", default='')
	descripinsp = models.TextField(null=True, verbose_name="Description Evt Sécu")
	notifevt = models.FileField(upload_to = 'evt_securite/%Y/%m/%d/', verbose_name="Notification evt")
	
	
	def save(self):
		if not self.id:
			self.codeevt =   str(datetime.today()) + "--" + self.typeevt
		super(Evtsecurite, self).save()
	
		
	
	def __str__(self):
		return  self.codeevt	
		
		

class Dossierevenementsecu(models.Model):
	codeevenementsecu = models.ForeignKey('Evtsecurite',  on_delete=models.CASCADE, verbose_name="Code Evénement Sécurité")
	descriptiondocumentevt = models.TextField(null=True, blank = True, verbose_name="Description Dossier Evénement")
	datedocumentevt = models.DateField(verbose_name="Date de production du document ", default='2020-02-13')
	dossierevt = models.FileField(upload_to = 'dossiers/evt/%Y/%m/%d/', verbose_name="Document Evénement", default='fichierdefaut.pdf')
	
	def __str__(self):
		return self.descriptiondocumentevt + self.codeevenementsecu.codeevt
		
      
      
class DomaineInspection(models.Model):
	nomdomaineinsp = models.CharField(max_length=30, verbose_name="Domaine d'inspecion ")
	checklistdomaineinsp = models.FileField(upload_to = 'checklist/%Y/%m/%d/', verbose_name="Checklist", default='fichierdefaut.pdf')
	servicedomaineinsp = models.ForeignKey('Serviceac', on_delete=models.CASCADE, verbose_name="Service Responsable")
	descripdomaineinsp = models.TextField(null=True, verbose_name="Description Domaine Inspection")
	
	def __str__(self):
		return self.nomdomaineinsp         

class Inspection(models.Model):
	codeinsp = models.CharField (max_length=150, editable=False)
	domaineinsp = models.ManyToManyField('DomaineInspection', verbose_name="Domaine(s) Inspection")
	datedebutinsp = models.DateField(verbose_name="Début inspection ")
	datefininsp = models.DateField(verbose_name="Fin inspection ")
	TYPEINSPS = (
	   ('PER', 'Périodique'),
	   ('INO', 'Inopiné'),
	   ('AUT', 'Autre')
	)	
	typeinsp = models.CharField(max_length=3, choices=TYPEINSPS,verbose_name="Type Inspection")
	ZONEINSP = (
	   ('aibd', 'AIBD'),
	   ('louis', 'St Louis'),
	   ('tamba', 'Tamba'),
	   ('zig', 'Ziguinchor'),
	   ('cap', 'Cap Skirring'),
	   ('centre', 'Zone Centre'),
	   ('est', 'Zone Est'),
	   ('nord', 'Zone Nord'),
	   ('sud', 'Zone Sud-Est')
	)	
	zoneinsp = models.CharField(max_length=6, choices=ZONEINSP, verbose_name="Zone Aérodrome",default="")
	insprealisee = models.BooleanField(default=False, verbose_name="Réalisée")
	inspentamee = models.BooleanField(default=False, verbose_name="Entamée")
	agentac = models.ManyToManyField('Agentac', verbose_name="Equipe Inspection")
	nomaero = models.ForeignKey('Aerodrome', on_delete=models.CASCADE, verbose_name="Aérodrome")
	nomdepartement = models.ForeignKey('Departementac', on_delete=models.CASCADE, verbose_name="Département en charge")
	descripinsp = models.TextField(null=True, verbose_name="Description Inspection")
	coutinsp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Coût Inspection en CFA", default=0)
	rapportinsp = models.FileField(upload_to = 'aerodromes/%Y/%m/%d/', verbose_name="Rapport Inspection", default='fichierdefaut.pdf')
	
	def clean(self):
		if self.datefininsp < self.datedebutinsp:
			raise ValidationError("Les dates de début et de fin de l'inspection ne sont pas correctes!")	
	
	def save(self):
		self.codeinsp = str(self.datedebutinsp) + '/'+ str(self.zoneinsp) + '_' + str(self.nomaero.nomaero)
		super(Inspection, self).save()
		
	
	def __str__(self):
		return self.codeinsp	 
      
class Positionequipe(models.Model):
	latitudeposi = models.CharField(max_length=30, verbose_name="Latitude ")
	longitudeposi = models.CharField(max_length=30, verbose_name="Longitude ")
	descripposi = models.TextField(null=True, verbose_name="Description Position")
	
	def __str__(self):
		return 'Point_'+ self.latitudeposi +';' + self.longitudeposi   
		

class Trajetmission(models.Model):
	inspection = models.ForeignKey('Inspection', on_delete=models.CASCADE, verbose_name="Inspection")
	MOYENTRANS = (
	   ('VOIT', 'Voiture'),
	   ('AVIO', 'Avion'),
	)
	moyentrans = models.CharField(max_length=4, choices=MOYENTRANS)
	positionequipes = models.ManyToManyField('Positionequipe', verbose_name="Points du trajet")
	descriptrajet = models.TextField(null=True, verbose_name="Description Trajet")
	
	def __str__(self):
		return self.descriptrajet
		

class Choixdepartement(models.Model):
	departement = models.ForeignKey('Departementac', on_delete=models.CASCADE, verbose_name="Département")
	descript = models.TextField(null=True, verbose_name="Description Choix")
	
	def __str__(self):
		return self.descript
		
		
class Dossierinspection(models.Model):
	codeinspection = models.ForeignKey('Inspection',  on_delete=models.CASCADE, verbose_name="Code Inspection")
	description = models.TextField(null=True, blank = True, verbose_name="Description Dossier Inspection")
	datedocument = models.DateField(verbose_name="Date de production du document ", default='2020-02-13')
	dossierinsp = models.FileField(upload_to = 'dossiers/%Y/%m/%d/', verbose_name="Document Inspection", default='fichierdefaut.pdf')
	
	def __str__(self):
		return self.description + self.codeinspection.codeinsp
		
		
		
class Dossierformation(models.Model):
	codeformation = models.ForeignKey('Formationac',  on_delete=models.CASCADE, verbose_name="Code Formation")
	description = models.TextField(null=True, blank = True, verbose_name="Description Dossier Formation")
	datedocument = models.DateField(verbose_name="Date de production du document ", default='2020-02-13')
	dossierformation = models.FileField(upload_to = 'dossiers/formations/%Y/%m/%d/', verbose_name="Document Formation", default='fichierdefaut.pdf')
	
	def __str__(self):
		return self.description + self.codeformation.codeform
		

class Document(models.Model):
	codedocument = models.CharField(max_length=100, verbose_name="Référence document")
	titre = models.CharField(max_length=300, verbose_name="Titre document")
	departementdocument = models.ForeignKey('Departementac',  on_delete=models.CASCADE, verbose_name="Département  en charge")
	datedocument = models.DateField(verbose_name="Date de production du document ")
	fichierdocument = models.FileField(upload_to = 'documents/%Y/%m/%d/', verbose_name="Document Inspection", default='fichierdefaut.pdf')
	
	def __str__(self):
		return self.codedocument
		
		      
		      