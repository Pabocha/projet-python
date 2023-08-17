# Generated by Django 4.2.1 on 2023-06-13 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membres', '0004_alter_membres_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membres',
            name='price',
        ),
        migrations.AddField(
            model_name='membres',
            name='contribution',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='membres',
            name='date_inscris',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='membres',
            name='email',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membres',
            name='matricule',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membres',
            name='nom',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membres',
            name='phone',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membres',
            name='prenom',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membres',
            name='revenue_de_membre',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12),
        ),
    ]
