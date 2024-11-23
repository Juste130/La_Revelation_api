from rest_framework import serializers;
from .models import Chambres, Reservation_Chambre, Reservation, Reservation_Evenement, Utilisateur, Place_de_fete;


class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'



class ReservationSerializer(serializers.ModelSerializer):
    type_reservation = serializers.SerializerMethodField()
    details_reservation = serializers.SerializerMethodField()
    class Meta:
        model = Reservation
        fields = '__all__'

    def get_type_reservation(self, obj):
        if isinstance(obj, Reservation_Chambre):
            return "room"
        elif isinstance(obj, Reservation_Evenement):
            return "event"
        return None
    
    def get_details_reservation(self, obj):
        if isinstance(obj, Reservation_Chambre):
            return {"room_room": obj.room, "room_date_heure_arrive": obj.date_heure_arrive, "room_date_heure_depart": obj.date_heure_depart, "room_cout":obj.cout}
        elif isinstance(obj, Reservation_Evenement):
            return {"event_place": obj.place, "event_date": obj.date, "event_heure_debut": obj.heure_debut, "event_duree":obj.duree, "event_cout": obj.cout, "event_nombre_invites": obj.nombre_invites}


class ReservationChambreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation_Chambre
        fields = '__all__'


class ReservationEvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation_Evenement
        fields = '__all__'


class ChambreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chambres
        fields = '__all__'


class PlaceDeFeteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place_de_fete
        fields = '__all__'