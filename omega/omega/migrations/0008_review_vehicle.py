# Generated by Django 5.0.1 on 2024-04-07 03:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omega', '0007_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='Vehicle',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='omega.vehicle'),
        ),
    ]