from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import make_aware, is_naive

class Aeroports(models.Model):
    nom = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

    class Meta:
        managed = False
        db_table = 'aeroports'


class Pistes(models.Model):
    numero = models.IntegerField()
    aeroports = models.ForeignKey(
        Aeroports,
        on_delete=models.CASCADE,
        db_column='aeroport'
    )
    longueur = models.IntegerField()

    def __str__(self):
        return str(self.numero)

    class Meta:
        managed = False
        db_table = 'pistes_atterrissage'


class Compagnies(models.Model):
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)
    pays_rattachement = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

    class Meta:
        managed = False
        db_table = 'compagnies'


class Types(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    images = models.ImageField(upload_to='avions/', blank=True, null=True)
    longueur_piste_necessaire = models.IntegerField()

    def __str__(self):
        return f"{self.marque} {self.modele}"

    class Meta:
        managed = False
        db_table = 'types_avions'


class Avions(models.Model):
    nom = models.CharField(max_length=100)
    compagnie = models.ForeignKey(
        Compagnies,
        on_delete=models.CASCADE,
        db_column='compagnie'
    )
    modele = models.ForeignKey(
        Types,
        on_delete=models.CASCADE,
        db_column='modele'
    )

    def __str__(self):
        return self.nom

    class Meta:
        managed = False
        db_table = 'avions'


class Vols(models.Model):
    avions = models.ForeignKey(
        Avions,
        on_delete=models.CASCADE,
        db_column='avion'
    )
    pilote = models.CharField(max_length=100)
    aeroports_dep = models.ForeignKey(
        Aeroports,
        on_delete=models.CASCADE,
        related_name='vols_depart',
        db_column='aeroport_depart'
    )
    date_heure_depart = models.DateTimeField()
    aeroports_arr = models.ForeignKey(
        Aeroports,
        on_delete=models.CASCADE,
        related_name='vols_arrivee',
        db_column='aeroport_arrivee'
    )
    date_heure_arrivee = models.DateTimeField()

    def __str__(self):
        # Affiche l'heure de départ correctement
        dt = self.date_heure_depart.strftime('%Y-%m-%d %H:%M')
        return f"{self.avions.nom} – {dt}"

    class Meta:
        managed = False
        db_table = 'vols'

    def clean(self):
        super().clean()
        erreurs = {}

        # Rendre aware si nécessaire
        if is_naive(self.date_heure_depart):
            self.date_heure_depart = make_aware(self.date_heure_depart)
        if is_naive(self.date_heure_arrivee):
            self.date_heure_arrivee = make_aware(self.date_heure_arrivee)

        # Durée minimale de 10 min
        if self.date_heure_arrivee < self.date_heure_depart + timedelta(minutes=10):
            erreurs['date_heure_arrivee'] = "Le vol doit durer au moins 10 minutes."

        # Fenêtre de ±10 min pour éviter chevauchement au décollage
        dep_min = self.date_heure_depart - timedelta(minutes=10)
        dep_max = self.date_heure_depart + timedelta(minutes=10)
        conflits_dep = Vols.objects.filter(
            aeroports_dep=self.aeroports_dep,
            date_heure_depart__range=(dep_min, dep_max)
        ).exclude(pk=self.pk)
        if conflits_dep.exists():
            erreurs['date_heure_depart'] = (
                "Conflit : un vol décolle déjà de cet aéroport dans les 10 minutes."
            )

        # Fenêtre de ±10 min pour l'atterrissage
        arr_min = self.date_heure_arrivee - timedelta(minutes=10)
        arr_max = self.date_heure_arrivee + timedelta(minutes=10)
        conflits_arr = Vols.objects.filter(
            aeroports_arr=self.aeroports_arr,
            date_heure_arrivee__range=(arr_min, arr_max)
        ).exclude(pk=self.pk)
        if conflits_arr.exists():
            erreurs['date_heure_arrivee'] = (
                "Conflit : un vol atterrit déjà à cet aéroport dans les 10 minutes."
            )

        # Vérification longueur de piste minimale
        longueur_requise = self.avions.modele.longueur_piste_necessaire
        if not Pistes.objects.filter(
            aeroports=self.aeroports_dep,
            longueur__gte=longueur_requise
        ).exists():
            erreurs['aeroports_dep'] = (
                "Pas de piste assez longue à l'aéroport de départ."
            )
        if not Pistes.objects.filter(
            aeroports=self.aeroports_arr,
            longueur__gte=longueur_requise
        ).exists():
            erreurs['aeroports_arr'] = (
                "Pas de piste assez longue à l'aéroport d'arrivée."
            )

        if erreurs:
            raise ValidationError(erreurs)

    def save(self, *args, **kwargs):
        # On valide avant tout
        self.full_clean()
        super().save(*args, **kwargs)
