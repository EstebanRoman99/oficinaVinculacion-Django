# Generated by Django 4.1.1 on 2023-02-03 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0038_estudiante_autorizado_is_registrado'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='estudiante_aut',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Accounts.estudiante_autorizado'),
        ),
    ]
