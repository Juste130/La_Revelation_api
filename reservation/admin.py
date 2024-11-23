from django.contrib import admin
from .models import Utilisateur, Reservation, Reservation_Evenement, Reservation_Chambre, Place_de_fete, Chambres 

# Register your models here.

class AdminUtilisateur(admin.ModelAdmin):
    list_display = ('id', 'nom','prenom', 'email', 'contact', 'password', 'type_user')
    list_filter = ('nom', 'prenom', 'type_user')
    search_fields = ['nom', 'prenom', 'type_user']

class AdminReservation(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'date_heure_reservation', 'status_reservation')
    list_filter = ('date_heure_reservation', 'status_reservation')
    search_fields = ['date_heure_reservation', 'status_reservation']
    readonly_fields = ('date_heure_reservation',)

class AdminReservation_Evenement(admin.ModelAdmin):
    list_display = ('id', 'place', 'date', 'heure_debut', 'duree', 'cout', 'nombre_invites')
    list_filter = ('date', 'heure_debut')
    readonly_fields = ('date', 'heure_debut', 'duree')

class AdminReservation_Chambre(admin.ModelAdmin):
    list_display = ('id', 'room', 'date_heure_arrive', 'date_heure_depart', 'cout')
    list_filter = ('date_heure_arrive', 'date_heure_depart')
    readonly_fields = ('date_heure_arrive', 'date_heure_depart')


class AdminPlace_de_fete(admin.ModelAdmin):
    list_display = ('id', 'designation', 'capacite', 'prix', 'status_place', 'description')
    list_filter = ('designation', 'status_place')
    search_fields = ['designation', 'capacite', 'prix', 'status_place', ]

class AdminChambres(admin.ModelAdmin):
    list_display = ('id', 'numero_chambre', 'type', 'prix_heure', 'prix_nuitee', 'status_chambre', 'description')
    list_filter = ('numero_chambre','type', 'status_chambre')
    search_fields = ['numero_chambre', 'type', 'prix_heure', 'prix_nuitee', 'status_chambre']
    

admin.site.register(Utilisateur, AdminUtilisateur)
admin.site.register(Reservation, AdminReservation)
admin.site.register(Reservation_Evenement, AdminReservation_Evenement)
admin.site.register(Reservation_Chambre, AdminReservation_Chambre)
admin.site.register(Place_de_fete, AdminPlace_de_fete)
admin.site.register(Chambres, AdminChambres)

