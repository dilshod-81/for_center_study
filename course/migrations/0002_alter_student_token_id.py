# Generated by Django 4.2.7 on 2024-07-01 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='token_id',
            field=models.CharField(default='31519270', max_length=150),
        ),
    ]
