# Generated by Django 4.1.1 on 2023-02-03 14:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0040_invitacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitacion',
            name='fecha_elaboracion',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
