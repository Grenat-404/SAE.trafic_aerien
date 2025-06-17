import csv
from io import TextIOWrapper

from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_naive, make_aware

from .forms import aeroportsForm, avionsForm, compagniesForm, pistesForm, typesForm, volsForm
from . import models
from django.urls import reverse
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Vols, Pistes, Aeroports, Avions


def index(request):
    apts = models.Aeroports.objects.all()
    return render(request, "index.html", {"Aeroports": apts})

# –– UTILS ––
def _handle_crud(request, Model, FormClass, template_list, template_add,
                 template_update, template_delete, context_name, redirect_name, pk_name='id'):
    """
    Générique pour LIST / ADD / EDIT / DELETE selon request.path
    Mais ici on l'appelle manuellement dans chaque view pour plus de clarté.
    """
    pass  # on n'utilise pas dans cette version, on garde views séparées

def fiche_vol_pdf(request, vol_id):
    vol = Vols.objects.get(pk=vol_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="fiche_vol_{vol_id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 100

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, y, f"Fiche de Vol #{vol.id}")

    p.setFont("Helvetica", 12)
    y -= 40
    p.drawString(100, y, f"Avion : {vol.avions.nom} ({vol.avions.modele.marque} {vol.avions.modele.modele})")

    y -= 25
    p.drawString(100, y, f"Compagnie : {vol.avions.compagnie.nom}")

    y -= 25
    p.drawString(100, y, f"Pilote : {vol.pilote}")

    y -= 25
    p.drawString(100, y, f"Aéroport de départ : {vol.aeroports_dep.nom} ({vol.date_heure_depart.strftime('%d/%m/%Y %H:%M')})")
    longueurs_dep = Pistes.objects.filter(aeroports=vol.aeroports_dep).values_list('longueur', flat=True)
    y -= 20
    p.drawString(120, y, f"Pistes : {', '.join(str(l) + ' m' for l in longueurs_dep) if longueurs_dep else 'Aucune'}")

    y -= 25
    p.drawString(100, y, f"Aéroport d'arrivée : {vol.aeroports_arr.nom} ({vol.date_heure_arrivee.strftime('%d/%m/%Y %H:%M')})")
    longueurs_arr = Pistes.objects.filter(aeroports=vol.aeroports_arr).values_list('longueur', flat=True)
    y -= 20
    p.drawString(120, y, f"Pistes : {', '.join(str(l) + ' m' for l in longueurs_arr) if longueurs_arr else 'Aucune'}")

    p.showPage()
    p.save()
    return response

def fichier_vols(request):
    import_message = None

    if request.method == "POST" and 'submit_csv' in request.POST:
        fichier_uploaded = request.FILES.get('fichier')
        if fichier_uploaded:
            try:
                # Décodage du fichier CSV
                fichier_decoded = TextIOWrapper(fichier_uploaded.file, encoding='utf-8')
                reader = csv.DictReader(fichier_decoded)
                cree, erreurs = 0, []

                for i, ligne in enumerate(reader, start=2):
                    try:
                        # Recherche de l'avion
                        nom_avion = ligne['avion'].strip()
                        try:
                            avion = Avions.objects.get(nom__iexact=nom_avion)
                        except Avions.DoesNotExist:
                            erreurs.append(f"Ligne {i}: Avion '{nom_avion}' inexistant")
                            continue

                        # Pilote
                        pilote = ligne['pilote'].strip()

                        # Aéroport de départ
                        nom_dep = ligne['aeroport_depart'].strip()
                        try:
                            aero_dep = Aeroports.objects.get(nom__iexact=nom_dep)
                        except Aeroports.DoesNotExist:
                            erreurs.append(f"Ligne {i}: Aéroport de départ '{nom_dep}' inexistant")
                            continue

                        # Date et heure de départ
                        dt_depart = parse_datetime(ligne['date_heure_depart'].strip())
                        if not dt_depart:
                            raise ValueError("Format date_heure_depart invalide")
                        if is_naive(dt_depart):
                            dt_depart = make_aware(dt_depart)

                        # Aéroport d'arrivée
                        nom_arr = ligne['aeroport_arrivee'].strip()
                        try:
                            aero_arr = Aeroports.objects.get(nom__iexact=nom_arr)
                        except Aeroports.DoesNotExist:
                            erreurs.append(f"Ligne {i}: Aéroport d'arrivée '{nom_arr}' inexistant")
                            continue

                        # Date et heure d'arrivée
                        dt_arrivee = parse_datetime(ligne['date_heure_arrivee'].strip())
                        if not dt_arrivee:
                            raise ValueError("Format date_heure_arrivee invalide")
                        if is_naive(dt_arrivee):
                            dt_arrivee = make_aware(dt_arrivee)

                        # Création et validation du vol
                        vol = Vols(
                            avions=avion,
                            pilote=pilote,
                            aeroports_dep=aero_dep,
                            date_heure_depart=dt_depart,
                            aeroports_arr=aero_arr,
                            date_heure_arrivee=dt_arrivee,
                        )
                        vol.full_clean()
                        vol.save()

                        cree += 1
                    except (ValidationError, ValueError) as e:
                        # Gestion des erreurs de validation
                        msg = e.message_dict if isinstance(e, ValidationError) else str(e)
                        erreurs.append(f"Ligne {i}: {msg}")
                    except Exception as e:
                        erreurs.append(f"Ligne {i}: Erreur inattendue: {e}")

                # Préparation du message de retour
                messages = []
                if cree:
                    messages.append(f"{cree} vol(s) créé(s) avec succès.")
                if erreurs:
                    messages.extend(erreurs)
                import_message = "<br>".join(messages)
            except Exception as err:
                import_message = f"Erreur de lecture du fichier: {err}"
        else:
            import_message = "Aucun fichier reçu."

    return render(request, 'avion/fichier_vols.html', {
        'import_message': import_message
    })

# –– Aéroports ––
def afficheAeroports(request):
    qs = Aeroports.objects.all()
    if qs:
        print("Il y a des aéroports")
    else:
        print("Il n'y a pas d'aéroports")
    return render(request, "avion/afficheAeroports.html", {"object_list": qs})

def ajoutAeroports(request):
    if request.method == "POST":
        form = aeroportsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('avion:afficheAeroports')
    else:
        form = aeroportsForm()
    return render(request, "avion/ajoutAeroports.html", {"form": form})

def updateAeroports(request, id):
    inst = get_object_or_404(models.Aeroports, pk=id)
    if request.method == "POST":
        form = aeroportsForm(request.POST, request.FILES, instance=inst)
        if form.is_valid():
            form.save()
            return redirect('avion:afficheAeroports')
    else:
        form = aeroportsForm(instance=inst)
    return render(request, "avion/updateAeroports.html", {"form": form, "id": id})

def deleteAeroports(request, id):
    inst = get_object_or_404(models.Aeroports, pk=id)
    if request.method == "POST":
        inst.delete()
        return redirect('avion:afficheAeroports')
    return render(request, "avion/deleteAeroports.html", {"object": inst})

# –– Avions ––
def afficheAvions(request):
    qs = models.Avions.objects.all()
    return render(request, "avion/afficheAvions.html", {"object_list": qs})

def ajoutAvions(request):
    if request.method == "POST":
        form = avionsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('avion:afficheAvions')
    else:
        form = avionsForm()
    return render(request, "avion/ajoutAvions.html", {"form": form})

def updateAvions(request, id):
    inst = get_object_or_404(models.Avions, pk=id)
    if request.method == "POST":
        form = avionsForm(request.POST, request.FILES, instance=inst)
        if form.is_valid():
            form.save()
            return redirect('avion:afficheAvions')
    else:
        form = avionsForm(instance=inst)
    return render(request, "avion/updateAvions.html", {"form": form, "id": id})

def deleteAvions(request, id):
    inst = get_object_or_404(models.Avions, pk=id)
    if request.method == "POST":
        inst.delete()
        return redirect('avion:afficheAvions')
    return render(request, "avion/deleteAvions.html", {"object": inst})

# –– Compagnies ––
def afficheCompagnies(request):
    qs = models.Compagnies.objects.all()
    return render(request, "avion/afficheCompagnies.html", {"object_list": qs})

def ajoutCompagnies(request):
    if request.method == "POST":
        form = compagniesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('avion:afficheCompagnies')
    else:
        form = compagniesForm()
    return render(request, "avion/ajoutCompagnies.html", {"form": form})

def updateCompagnies(request, id):
    inst = get_object_or_404(models.Compagnies, pk=id)
    if request.method == "POST":
        form = compagniesForm(request.POST, request.FILES, instance=inst)
        if form.is_valid():
            form.save()
            return redirect('avion:afficheCompagnies')
    else:
        form = compagniesForm(instance=inst)
    return render(request, "avion/updateCompagnies.html", {"form": form, "id": id})

def deleteCompagnies(request, id):
    inst = get_object_or_404(models.Compagnies, pk=id)
    if request.method == "POST":
        inst.delete()
        return redirect('avion:afficheCompagnies')
    return render(request, "avion/deleteCompagnies.html", {"object": inst})

# –– Pistes ––
def affichePistes(request):
    qs = models.Pistes.objects.all()
    return render(request, "avion/affichePistes.html", {"object_list": qs})

def ajoutPistes(request):
    if request.method == "POST":
        form = pistesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('avion:affichePistes')
    else:
        form = pistesForm()
    return render(request, "avion/ajoutPistes.html", {"form": form})

def updatePistes(request, id):
    inst = get_object_or_404(models.Pistes, pk=id)
    if request.method == "POST":
        form = pistesForm(request.POST, request.FILES, instance=inst)
        if form.is_valid():
            form.save()
            return redirect('avion:affichePistes')
    else:
        form = pistesForm(instance=inst)
    return render(request, "avion/updatePistes.html", {"form": form, "id": id})

def deletePistes(request, id):
    inst = get_object_or_404(models.Pistes, pk=id)
    if request.method == "POST":
        inst.delete()
        return redirect('avion:affichePistes')
    return render(request, "avion/deletePistes.html", {"object": inst})

# –– Types ––
def afficheTypes(request):
    qs = models.Types.objects.all()
    return render(request, "avion/afficheTypes.html", {"object_list": qs})

def ajoutTypes(request):
    if request.method == "POST":
        form = typesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('avion:afficheTypes')
    else:
        form = typesForm()
    return render(request, "avion/ajoutTypes.html", {"form": form})

def updateTypes(request, id):
    inst = get_object_or_404(models.Types, pk=id)
    if request.method == "POST":
        form = typesForm(request.POST, request.FILES, instance=inst)
        if form.is_valid():
            form.save()
            return redirect('avion:afficheTypes')
    else:
        form = typesForm(instance=inst)
    return render(request, "avion/updateTypes.html", {"form": form, "id": id})

def deleteTypes(request, id):
    inst = get_object_or_404(models.Types, pk=id)
    if request.method == "POST":
        inst.delete()
        return redirect('avion:afficheTypes')
    return render(request, "avion/deleteTypes.html", {"object": inst})

# –– Vols ––
def afficheVols(request):
    qs = models.Vols.objects.all()
    return render(request, "avion/afficheVols.html", {"object_list": qs})

def ajoutVols(request):
    if request.method == "POST":
        form = volsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('avion:afficheVols')
    else:
        form = volsForm()
    return render(request, "avion/ajoutVols.html", {"form": form})

def updateVols(request, id):
    inst = get_object_or_404(models.Vols, pk=id)
    if request.method == "POST":
        form = volsForm(request.POST, request.FILES, instance=inst)
        if form.is_valid():
            form.save()
            return redirect('avion:afficheVols')
    else:
        form = volsForm(instance=inst)
    return render(request, "avion/updateVols.html", {"form": form, "id": id})

def deleteVols(request, id):
    inst = get_object_or_404(models.Vols, pk=id)
    if request.method == "POST":
        inst.delete()
        return redirect('avion:afficheVols')
    return render(request, "avion/deleteVols.html", {"object": inst})
