# Generated by Django 4.2.1 on 2023-06-26 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0013_alter_utilisateur_solde'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=75)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('type_message', models.CharField(choices=[('inscription', 'Inscription'), ('message', 'Message'), ('autre', 'Autre')], max_length=50)),
                ('read', models.BooleanField(default=False)),
                ('date_ajouter', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-date_ajouter',),
            },
        ),
    ]
