from django.shortcuts import render

# Create your views here.


from rest_framework import viewsets, status, permissions
# from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import make_aware
from rest_framework.views import APIView
from datetime import datetime, timedelta
from rest_framework.response import Response
from .models import Utilisateur, Reservation, Reservation_Chambre, Reservation_Evenement, Chambres, Place_de_fete
from .serializers import UtilisateurSerializer, ReservationSerializer, ReservationEvenementSerializer, ReservationChambreSerializer, ChambreSerializer, PlaceDeFeteSerializer
import logging






logger = logging.getLogger(__name__)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Extraire le token refresh depuis la requête
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Aucun token fourni."}, status=status.HTTP_400_BAD_REQUEST)

            # Ajouter le token à la liste noire
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Déconnexion réussie."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
        # Récupération des données de la requête
        room_type = request.data.get('room_type')
        date_debut_str = request.data.get('date_debut')
        date_fin_str = request.data.get('date_fin')
        utilisateur = request.user

        # Vérification des champs requis
        if not (room_type and date_debut_str and date_fin_str):
            return Response({'detail': 'Toutes les informations sont requises'}, status=status.HTTP_400_BAD_REQUEST)

        # Conversion et validation des dates
        try:
            date_debut = datetime.fromisoformat(date_debut_str)
            date_fin = datetime.fromisoformat(date_fin_str)

            # Rendre les datetimes "aware" (compatibles avec les fuseaux horaires)
            date_debut = make_aware(date_debut)
            date_fin = make_aware(date_fin)

            if date_debut >= date_fin:
                return Response({'detail': 'La date de début doit précéder la date de fin.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'detail': 'Les dates doivent être au format valide (YYYY-MM-DD HH:MM:SS).'}, status=status.HTTP_400_BAD_REQUEST)

        # Recherche des chambres disponibles
        chambres_disponibles = Chambres.objects.filter(type=room_type, status_chambre='disponible')

        if not chambres_disponibles.exists():
            return Response({'detail': 'Aucune chambre de ce type n\'est disponible.'}, status=status.HTTP_404_NOT_FOUND)

        # Vérification des conflits avec d'autres réservations
        conflits = Reservation_Chambre.objects.filter(
            room__in=chambres_disponibles,
            date_heure_arrive__lt=date_fin,
            date_heure_depart__gt=date_debut
        )

        if conflits.exists():
            return Response({'detail': 'Toutes les chambres de ce type sont réservées pour cette période.'}, status=status.HTTP_400_BAD_REQUEST)

        # Création de la réservation
        chambre = chambres_disponibles.first()
        reservation = Reservation_Chambre.objects.create(
            room=chambre,
            utilisateur=utilisateur,
            date_heure_arrive=date_debut,
            date_heure_depart=date_fin,
            cout=request.data.get('cout', 0),  # Coût par défaut à 0 si non fourni
            plus_details=request.data.get('plus_details', '')
        )

        # Mise à jour du statut de la chambre
        chambre.status_chambre = 'occupée'
        chambre.save()

        # Sérialisation et réponse
        serializer = self.get_serializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReservationEvenementViewSet(viewsets.ModelViewSet):
    queryset = Reservation_Evenement.objects.all()
    serializer_class = ReservationEvenementSerializer

    def validate_input(self, request):
        """
        Valide les champs d'entrée pour la réservation.
        """
        # Récupération des données
        place_designation = request.data.get('place_designation')
        date = request.data.get('date')
        heure_debut = request.data.get('heure_debut')
        duree = request.data.get('duree')

        if not (place_designation and date and heure_debut and duree):
            raise ValueError("Toutes les informations sont requises : place_designation, date, heure_debut, duree.")

        # Validation de la date
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Date invalide. Utilisez le format YYYY-MM-DD.")

        # Validation de l'heure de début
        try:
            heure_debut = datetime.strptime(heure_debut, '%H:%M').time()
        except ValueError:
            raise ValueError("Heure invalide. Utilisez le format HH:MM.")

        # Validation de la durée
        try:
            duree = int(duree)
            if duree <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("La durée doit être un nombre positif.")

        return place_designation, date, heure_debut, duree

    @action(detail=False, methods=['post'])
    def reserver_event(self, request):
        try:
            # Validation des données d'entrée
            place_designation, date, heure_debut, duree = self.validate_input(request)

            utilisateur = request.user

            # Vérification de la disponibilité de la place
            place_disponible = Place_de_fete.objects.filter(designation=place_designation, status_place='disponible')
            if not place_disponible.exists():
                return Response({'detail': 'Aucune place disponible pour cette désignation.'}, status=status.HTTP_404_NOT_FOUND)

            # Calcul de l'heure de fin
            heure_fin = (datetime.combine(datetime.today(), heure_debut) + timedelta(hours=duree)).time()

            # Vérification des conflits
            conflits = Reservation_Evenement.objects.filter(
                place__in=place_disponible,
                date=date,
                heure_debut__lt=heure_fin,
                heure_debut__gt=heure_debut,
            )

            place = Place_de_fete.objects.filter(designation=place_designation).get()

            cout = place.prix * duree

            if conflits.exists():
                return Response({'detail': 'L\'espace voulu est déjà réservé pour cette période.'}, status=status.HTTP_400_BAD_REQUEST)

            # Création de la réservation
            place = place_disponible.first()
            reservation = Reservation_Evenement.objects.create(
                place=place,
                utilisateur=utilisateur,
                date=date,
                heure_debut=heure_debut,
                duree=duree,
                cout=cout,  # Calcul automatique ou valeur par défaut
                nombre_invites=request.data.get('nombre_invites', 0),
                plus_details=request.data.get('plus_details', '')
            )

            # Sérialisation et retour
            serializer = self.get_serializer(reservation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            # Gestion des erreurs de validation
            logger.error(f"Erreur lors de la réservation : {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Gestion des erreurs inattendues
            logger.error(f"Erreur inattendue : {str(e)}")
            return Response({'detail': 'Une erreur inattendue s\'est produite.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        




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

