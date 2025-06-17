from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'avion'

urlpatterns = [
    # page d'accueil
    path('', views.index, name='index'),

    # Aéroports
    path('airports/', views.afficheAeroports, name='afficheAeroports'),
    path('airports/add/', views.ajoutAeroports, name='ajoutAeroports'),
    path('airports/<int:id>/edit/', views.updateAeroports, name='updateAeroports'),
    path('airports/<int:id>/delete/', views.deleteAeroports, name='deleteAeroports'),

    # Avions
    path('planes/', views.afficheAvions, name='afficheAvions'),
    path('planes/add/', views.ajoutAvions, name='ajoutAvions'),
    path('planes/<int:id>/edit/', views.updateAvions, name='updateAvions'),
    path('planes/<int:id>/delete/', views.deleteAvions, name='deleteAvions'),

    # Compagnies
    path('companies/', views.afficheCompagnies, name='afficheCompagnies'),
    path('companies/add/', views.ajoutCompagnies, name='ajoutCompagnies'),
    path('companies/<int:id>/edit/',  views.updateCompagnies, name='updateCompagnies'),
    path('companies/<int:id>/delete/', views.deleteCompagnies, name='deleteCompagnies'),

    # Pistes
    path('runways/', views.affichePistes, name='affichePistes'),
    path('runways/add/', views.ajoutPistes, name='ajoutPistes'),
    path('runways/<int:id>/edit/', views.updatePistes, name='updatePistes'),
    path('runways/<int:id>/delete/', views.deletePistes, name='deletePistes'),

    # Types d'avion
    path('types/', views.afficheTypes, name='afficheTypes'),
    path('types/add/', views.ajoutTypes, name='ajoutTypes'),
    path('types/<int:id>/edit/', views.updateTypes, name='updateTypes'),
    path('types/<int:id>/delete/', views.deleteTypes, name='deleteTypes'),

    # Vols
    path('flights/', views.afficheVols, name='afficheVols'),
    path('flights/add/', views.ajoutVols, name='ajoutVols'),
    path('flights/<int:id>/edit/', views.updateVols, name='updateVols'),
    path('flights/<int:id>/delete/', views.deleteVols, name='deleteVols'),
    path('vols/<int:vol_id>/fiche/', views.fiche_vol_pdf, name='fiche_vol'),
    path('vols/importer/', views.fichier_vols, name='fichier_vols'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)