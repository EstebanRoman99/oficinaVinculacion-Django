# Generated by Django 4.1.1 on 2023-01-16 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0027_alter_materia_clave'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependencia',
            name='rfc',
            field=models.CharField(error_messages={'unique': 'Existe otra Organizacion o Empresa con este RFC.'}, max_length=13, null=True, unique=True),
        ),
    ]