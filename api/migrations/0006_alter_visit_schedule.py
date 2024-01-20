# Generated by Django 5.0.1 on 2024-01-20 08:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_schedule_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='schedule',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visits', to='api.schedule'),
        ),
    ]
