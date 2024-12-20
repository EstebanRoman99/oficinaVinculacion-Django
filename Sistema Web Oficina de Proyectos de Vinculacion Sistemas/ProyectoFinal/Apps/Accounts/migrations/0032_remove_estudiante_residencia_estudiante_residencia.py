# Generated by Django 4.1.1 on 2023-01-17 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0031_remove_estudiante_anteproyecto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudiante',
            name='residencia',
        ),
        migrations.CreateModel(
            name='Estudiante_Residencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('ACTIVO', 'ACTIVO'), ('INACTIVO', 'INACTIVO')], default='ACTIVO', max_length=15)),
                ('estudiante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Accounts.estudiante')),
                ('residencia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Accounts.residencia')),
            ],
        ),
    ]
