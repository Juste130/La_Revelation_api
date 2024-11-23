# Generated by Django 5.1.1 on 2024-11-16 13:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chambres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_chambre', models.CharField(max_length=5, unique=True, verbose_name='Numéro de chambre')),
                ('type', models.CharField(choices=[('ventilee', 'Chambre ventilée'), ('climatisé', 'Chambre climatisée'), ('suite', 'Suite')], max_length=50, verbose_name='Type de chambre')),
                ('prix_heure', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prix par heure')),
                ('prix_nuitee', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prix par nuitée')),
                ('status_chambre', models.CharField(choices=[('indisponible', 'Indisponible'), ('disponible', 'Disponible')], max_length=15, verbose_name='Status de la chambre')),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Chambre',
                'verbose_name_plural': 'Chambres',
            },
        ),
        migrations.CreateModel(
            name='Place_de_fete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=100, unique=True)),
                ('capacite', models.IntegerField(verbose_name='Capacité de la place')),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status_place', models.CharField(choices=[('indisponible', 'Indisponible'), ('disponible', 'Disponible')], max_length=15, verbose_name='Status de la place')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nom', models.CharField(max_length=40, verbose_name="Nom de l'utilisateur")),
                ('prenom', models.CharField(max_length=40, verbose_name="Prénom de l'utilisateur")),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('contact', models.CharField(max_length=20)),
                ('type_user', models.CharField(choices=[('admin', 'Administrateur'), ('client', 'Client')], max_length=10, verbose_name="Type d'utilisateur")),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_heure_reservation', models.DateTimeField(auto_now_add=True, verbose_name='Date de réservation')),
                ('status_reservation', models.CharField(choices=[('en_cours', 'En cours...'), ('confirmee', 'Confirmée'), ('annulee', 'Annulée')], max_length=15, verbose_name='Status de la réservation')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation_Chambre',
            fields=[
                ('reservation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reservation.reservation')),
                ('date_heure_arrive', models.DateTimeField(verbose_name="Date et Heure d'arrivé")),
                ('date_heure_depart', models.DateTimeField(verbose_name='Date et Heure de départ')),
                ('cout', models.DecimalField(decimal_places=2, max_digits=10)),
                ('plus_details', models.TextField(verbose_name='Plud de détails')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.chambres', verbose_name='Chambre')),
            ],
            bases=('reservation.reservation',),
        ),
        migrations.CreateModel(
            name='Reservation_Evenement',
            fields=[
                ('reservation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reservation.reservation')),
                ('date', models.DateField(verbose_name="Date de l'évènement")),
                ('heure_debut', models.TimeField(verbose_name='Heure de début')),
                ('duree', models.IntegerField(verbose_name='Durée')),
                ('cout', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nombre_invites', models.IntegerField(verbose_name="Nombres d'invités approximatif")),
                ('plus_details', models.TextField(verbose_name='Plud de détails')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.place_de_fete')),
            ],
            bases=('reservation.reservation',),
        ),
    ]
