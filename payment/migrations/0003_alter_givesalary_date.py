# Generated by Django 4.2.13 on 2024-07-09 08:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_givesalary_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='givesalary',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2024, 7, 9), null=True),
        ),
    ]
