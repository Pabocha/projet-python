# Generated by Django 4.2.1 on 2023-06-07 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investisseurs', '0003_investisseur_solde'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investisseur',
            name='montant_investi',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='investisseur',
            name='retrait_en_attente',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='investisseur',
            name='revenue_mensuel',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='investisseur',
            name='solde',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='investisseur',
            name='total_de_gains',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='investisseur',
            name='total_de_retrait',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=12, null=True),
        ),
    ]
