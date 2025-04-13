from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=40, verbose_name="Nom de l'utilisateur")
    prenom = models.CharField(max_length=40, verbose_name="Prénom de l'utilisateur")
    email = models.EmailField(unique=True )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    contact = models.CharField(max_length=20)
    type_user = models.CharField(max_length=10, choices=(
        ('admin', 'Administrateur'),
        ('client', 'Client')
    ), verbose_name="Type d'utilisateur")

    objects = UtilisateurManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def has_perm(self, perm, obj=None):
        # Par défaut, autorise tous les superutilisateurs
        return self.is_superuser

    def has_module_perms(self, app_label):
        # Par défaut, autorise tous les superutilisateurs
        return self.is_superuser


class Reservation(models.Model):
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE)   
    date_heure_reservation = models.DateTimeField(auto_now_add=True, verbose_name="Date de réservation")
    status_reservation = models.CharField(max_length=15, choices=(
        ('en_cours', 'En cours...'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée')
    ), verbose_name="Status de la réservation", default='en_cours')


    def __str__(self):
        return f"Reservation {self.id} par {self.utilisateur.nom} {self.utilisateur.prenom} le {self.date_heure_reservation}"

class Reservation_Evenement(Reservation):
    place = models.ForeignKey('Place_de_fete', on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Date de l'évènement", editable=True)
    heure_debut = models.TimeField(verbose_name="Heure de début", editable=True)
    duree = models.IntegerField(verbose_name='Durée', editable=True)
    cout = models.IntegerField()
    nombre_invites = models.CharField(max_length=25, verbose_name="Nombres d'invités approximatif", choices=(
        ('petit', '01 à 10'),
        ('cinquantaine', '11 à 50'),
        ('centaine', '51 à 100'),
        ('cent_cinquantaine', '101 à 150'),
        ('deux_centaine', '151 à 200'),
        ('trois_centaine', '200 à 300'),
        ('maximum', 'Plus de 300')
    ))
    plus_details = models.TextField(verbose_name="Plud de détails")

    def __str__(self):
        return f"Reservation d'évènement {self.id}"

class Reservation_Chambre(Reservation):
    room = models.ForeignKey('Chambres', verbose_name="Chambre", on_delete=models.CASCADE)
    date_heure_arrive = models.DateTimeField(verbose_name="Date et Heure d'arrivé", editable=True,)
    date_heure_depart = models.DateTimeField(verbose_name="Date et Heure de départ", editable=True)
    cout = models.IntegerField()
    plus_details = models.TextField(verbose_name="Plud de détails")

    def __str__(self):
        return f"Reservation de chambre {self.id}"

class Place_de_fete(models.Model):
    designation = models.CharField(max_length=100, unique=True, choices=(
        ('vip', 'VIP'),
        ('salle_conference', 'Salle de conference'),
        ('hall0', 'Hall à l\'entré'),
        ('hall1', 'Hall au premier étage'),
        ('calme', 'Espace calme')
    ))
    capacite = models.IntegerField(verbose_name="Capacité de la place")
    prix = models.IntegerField()
    status_place = models.CharField(max_length=15, choices=(
        ('indisponible', "Indisponible"),
        ('disponible', 'Disponible')
    ), verbose_name="Status de la place")
    description = models.TextField()

    def __str__(self):
        return self.designation

class Chambres(models.Model):
    numero_chambre = models.CharField(max_length=5, verbose_name="Numéro de chambre", unique=True)
    type = models.CharField(max_length=50, verbose_name="Type de chambre", choices=(
        ('ventile', "Chambre ventilée"),
        ('climatise', "Chambre climatisée"),
        ('suite', 'Suite')
    ))
    prix_heure = models.IntegerField(verbose_name="Prix par heure")
    prix_nuitee = models.IntegerField(verbose_name="Prix par nuitée")
    status_chambre = models.CharField(max_length=15, choices=(
        ('indisponible', "Indisponible"),
        ('disponible', 'Disponible')
    ), verbose_name="Status de la chambre")
    description = models.TextField()

    def __str__(self):
        return f"Chambre {self.numero_chambre} - {self.type}"
    

    class Meta:
        verbose_name = "Chambre"
        verbose_name_plural = "Chambres"