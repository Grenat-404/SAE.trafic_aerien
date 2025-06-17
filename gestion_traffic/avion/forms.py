from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
from . import models


class aeroportsForm(ModelForm):
    class Meta:
        model = models.Aeroports
        fields = ('nom', 'pays')
        labels = {
        'nom' : _('Nom'),
        'pays' : _("Pays de localisation"),
        }

class pistesForm(ModelForm):
    class Meta:
        model = models.Pistes
        fields = ('numero', 'aeroports', 'longueur')
        labels = {
        'numero' : _('Numéro de la piste'),
        'aeroports' : _("Aéroport d'appartennance") ,
        'longueur' : _('Longueur de la piste'),
        }

class compagniesForm(ModelForm):
    class Meta:
        model = models.Compagnies
        fields = ('nom', 'description', 'pays_rattachement')
        labels = {
        'nom': _('Nom de la compagnie'),
        'description': _("Description"),
        'pays_rattachement': _('Pays de rattachement'),
        }

class typesForm(ModelForm):
    class Meta:
        model = models.Types
        fields = ('marque', 'modele', 'description', 'images', 'longueur_piste_necessaire')
        labels = {
        'marque' : _('Marque'),
        'modele' : _('Modèle') ,
        'description' : _('Description'),
        'images' : _('URL de la photo'),
        'longueur_piste_necessaire': _(' longueur de piste nécessaire'),
        }

class avionsForm(ModelForm):
    class Meta:
        model = models.Avions
        fields = ('nom', 'compagnie', 'modele')
        labels = {
        'nom' : _("Nom de l'avion"),
        'compagnie' : _('Nom de la compagnie') ,
        'modele' : _("Modele de l'avion"),
        }


class volsForm(ModelForm):
    class Meta:
        model = models.Vols
        fields = ('avions', 'pilote', 'aeroports_dep', 'date_heure_depart', 'aeroports_arr', 'date_heure_arrivee')
        labels = {
        'avions' : _('Avion'),
        'pilote' : _('Pilote du vol') ,
        'aeroports_dep' : _('aéroport de départ'),
        'date_heure_depart' : _('date et heure de départ'),
        'aeroports_arr' : _("aéroport d'arrivée"),
        'date_heure_arrivee' : _("date et heure d'arrivée")
        }
        widgets = {
            'date_heure_depart': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={
                    'placeholder': 'JJ/MM/AAAA HH:MM',
                    'class': 'form-control',
                }
            ),
            'date_heure_arrivee': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={
                    'placeholder': 'JJ/MM/AAAA HH:MM',
                    'class': 'form-control',
                }
            ),
        }