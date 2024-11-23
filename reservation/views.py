from django.shortcuts import render

# Create your views here.


from rest_framework import viewsets, status
# from rest_framework.decorators import api_view
from rest_framework.decorators import action
from datetime import datetime, timedelta
from rest_framework.response import Response
from .models import Utilisateur, Reservation, Reservation_Chambre, Reservation_Evenement, Chambres, Place_de_fete
from .serializers import UtilisateurSerializer, ReservationSerializer, ReservationEvenementSerializer, ReservationChambreSerializer, ChambreSerializer, PlaceDeFeteSerializer










class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

    def perform_create(self, serializer):
        # Ajoute automatiquement l'utilisateur authentifié lors de la création
        serializer.save(utilisateur=self.request.user)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        # Ajoute automatiquement l'utilisateur authentifié lors de la création
        serializer.save(utilisateur=self.request.user)


class ReservationChambreViewSet(viewsets.ModelViewSet):
    queryset = Reservation_Chambre.objects.all()
    serializer_class = ReservationChambreSerializer

    @action(detail=False, methods=['post'])
    def reserver_chambre(self, request):
        room_type = request.data.get('room_type')
        date_debut = request.data.get('date_debut')
        date_fin = request.data.get('date_fin')
        utilisateur = request.user

        if not(room_type and date_debut and date_fin):
            return Response({'detail': 'Toutes les informations sont requises'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            date_debut = datetime.fromisoformat(date_debut)
            date_fin = datetime.fromisoformat(date_fin)
            if date_debut >= date_fin:
                return Response({'detail': 'la date de début doit précéder la date de fin'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'detail': 'Les dates doivent etre au format valide (YYYY-MM-DD HH:MM).'}, status=status.HTTP_400_BAD_REQUEST)    
        
        chambres_disponibles = Chambres.objects.filter(type=room_type, status_chambre='disponible')

        if not chambres_disponibles.exists():
            return Response({'detail': 'Aucune chambre de ce type n\'est disponible.'}, status=status.HTTP_404_NOT_FOUND)
        


        conflits = Reservation_Chambre.objects.filter(
            room__in=chambres_disponibles,
            date_debut__lt=date_fin,
            date_fin__gt=date_debut
        )
        if conflits.exists():
            return Response({'detail': 'Toutes les chambres de ce type sont réservées pour cette période.'}, status=status.HTTP_400_BAD_REQUEST)
        

        chambre = chambres_disponibles.first()
        reservation = Reservation_Chambre.objects.create(
            room=chambre,
            utilisateur=utilisateur,
            date_heure_arrive=date_debut,
            date_heure_depart=date_fin,
            plus_details=request.data.get('plus_details', '')

        )
        serializer = self.get_serializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReservationEvenementViewSet(viewsets.ModelViewSet):
    queryset = Reservation_Evenement.objects.all()
    serializer_class = ReservationEvenementSerializer

    @action(detail=False, methods=['post'])
    def reserver_event(self, request):
        place_designation = request.data.get('place_designation')
        date = request.data.get('date')
        heure_debut = request.data.get('heure_debut')
        duree = request.data.get('duree')
        
        utilisateur = request.user

        if not (place_designation and date and heure_debut and duree):
            return Response({'detail': 'Toutes les informations sont requises'}, status=status.HTTP_400_BAD_REQUEST)
        
        place_disponible = Place_de_fete.objects.filter(designation=place_designation, status_place='disponible')

        try:
            heure_debut = datetime.strptime(heure_debut, '%H:%M').time()
        except ValueError:
            return Response({'detail': 'Heure invalide. Utilisez HH:MM.'}, status=status.HTTP_400_BAD_REQUEST)


        if not place_disponible.exists():
            return Response({'detail': 'Aucune place disponible pour cette désignation.'}, status=status.HTTP_404_NOT_FOUND)

        heure_fin = datetime.strptime(heure_debut, '%H:%M') + timedelta(hours=int(duree))
        
        conflits = Reservation_Evenement.objects.filter(
            place__in=place_disponible,
            date=date,
            heure_debut__lt=heure_fin,
            heure_fin__gt=heure_debut,
        )

        if conflits.exists():
            return Response({'detail': 'L\'espace voulue est dejà réservée pour cette période'}, status=status.HTTP_400_BAD_REQUEST)
        

        place=place_disponible.first()
        reservation = Reservation_Evenement.objects.create(
            place=place,
            utilisateur=utilisateur,
            date=date,
            heure_debut=heure_debut,
            nombre_invites=request.data.get('nombre_invites'),
            plus_details=request.data.get('plus_details')
        )

        serializer = self.get_serializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


        




class ChambreViewSet(viewsets.ModelViewSet):
    queryset = Chambres.objects.all()
    serializer_class = ChambreSerializer

    def perform_create(self, serializer):
        # Ajoute automatiquement l'utilisateur authentifié lors de la création
        serializer.save(utilisateur=self.request.user)


class PlaceDeFeteViewSet(viewsets.ModelViewSet):
    queryset = Place_de_fete.objects.all()
    serializer_class = PlaceDeFeteSerializer

    def perform_create(self, serializer):
        # Ajoute automatiquement l'utilisateur authentifié lors de la création
        serializer.save(utilisateur=self.request.user)

