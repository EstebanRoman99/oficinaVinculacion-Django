# Generated by Django 4.1.1 on 2023-01-06 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0021_remove_avisos_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisos',
            name='docente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Accounts.docente'),
        ),
        migrations.AlterField(
            model_name='avisos',
            name='estudiante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Accounts.estudiante'),
        ),
    ]
