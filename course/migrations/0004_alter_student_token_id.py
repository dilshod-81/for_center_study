# Generated by Django 4.2.13 on 2024-07-05 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_dynamicfield_registrationdata_alter_attendance_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='token_id',
            field=models.CharField(default='37012419', max_length=150, unique=True),
        ),
    ]