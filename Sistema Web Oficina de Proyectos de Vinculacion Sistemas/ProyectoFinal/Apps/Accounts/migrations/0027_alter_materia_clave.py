# Generated by Django 4.1.1 on 2023-01-16 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0026_alter_materia_clave'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materia',
            name='clave',
            field=models.CharField(error_messages={'unique': 'Existe otra materia con esta clave.'}, max_length=10, null=True, unique=True),
        ),
    ]
