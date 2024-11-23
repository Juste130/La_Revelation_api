# Generated by Django 5.1.1 on 2024-11-22 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_alter_place_de_fete_designation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place_de_fete',
            name='designation',
            field=models.CharField(choices=[('vip', 'VIP'), ('salle_conference', 'Salle de conference'), ('hall0', "Hall à l'entré"), ('hall1', 'Hall au premier étage'), ('calme', 'Espace calme')], max_length=100, unique=True),
        ),
    ]
