# Generated by Django 4.2.1 on 2023-07-05 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investisseurs', '0006_investisseur_status_retrait'),
    ]

    operations = [
        migrations.AddField(
            model_name='investisseur',
            name='date_augmentation_solde',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
