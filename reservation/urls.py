from django.urls import path
from .views import UtilisateurViewSet, ReservationViewSet, ReservationChambreViewSet, ReservationEvenementViewSet, ChambreViewSet, PlaceDeFeteViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('user', UtilisateurViewSet, basename='user')
router.register('reservation', ReservationViewSet, basename='reservation')
router.register('reservationEvent', ReservationEvenementViewSet, basename='reservationEvent')
router.register('reservationRoom', ReservationChambreViewSet, basename='reservationRoom')
router.register('room', ChambreViewSet, basename='room')
router.register('placedefetes', PlaceDeFeteViewSet, basename='placedefetes')

urlpatterns = router.urls


# urlpatterns = [
#     path('createUser/', UserApiViews.as_view()),
#     path('updateUser/<int:pk>/', UserApiViews.as_view()),
#     path('infoUser/<int:pk>/', UserApiViews.as_view()),
#     path('deleteUser/<int:pk>/', UserApiViews.as_view()),

#     path('createReservationChambre/', ReservationChambreApiViews.as_view()),
#     path('updateReservationChambre/<int:pk>/', ReservationChambreApiViews.as_view()),
#     path('detailsReservationChambre/<int:pk>/', ReservationChambreApiViews.as_view()),
#     path('deleteReservationChambre/<int:pk>/', ReservationChambreApiViews.as_view()),
#     path('listReservationChambre/', ReservationChambreApiViews.as_view()),

#     path('createReservationEvent/', ReservationEvenementApiViews.as_view()),
#     path('updateReservationEvent/<int:pk>/', ReservationEvenementApiViews.as_view()),
#     path('detailsReservationEvent/<int:pk>/', ReservationEvenementApiViews.as_view()),
#     path('deleteReservationEvent/<int:pk>/', ReservationEvenementApiViews.as_view()),
#     path('listReservationEvent/', ReservationEvenementApiViews.as_view()),

#     path('detailsReservation/<int:pk>/', ReservationApiViews.as_view()),
#     path('listReservation/', ReservationApiViews.as_view()),
    
# ]