# Generated by Django 4.1.1 on 2023-02-03 05:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0039_estudiante_estudiante_aut'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitacion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('anteproyecto', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Accounts.anteproyecto')),
                ('estudiante_destinatario', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Accounts.estudiante_autorizado')),
                ('estudiante_remitente', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Accounts.estudiante')),
            ],
        ),
    ]
