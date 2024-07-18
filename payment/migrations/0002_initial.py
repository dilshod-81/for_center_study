# Generated by Django 4.2.13 on 2024-07-18 06:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0001_initial'),
        ('course', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='givesalary',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='givesalary',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='genraldata',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='course.student'),
        ),
        migrations.AddField(
            model_name='discounted_students',
            name='recepient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='discounted_students',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.student'),
        ),
        migrations.AddField(
            model_name='addcashtowallet',
            name='recepient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='addcashtowallet',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.student'),
        ),
    ]