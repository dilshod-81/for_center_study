# Generated by Django 4.2.13 on 2024-07-18 06:53

import course.validators
import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date(2024, 7, 18))),
                ('present', models.BooleanField(default=True)),
                ('status', models.CharField(blank=True, choices=[('sababli', 'sababli'), ('sababsiz', 'sababsiz'), ('kelgan', 'kelgan')], default='kelgan', max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(choices=[('1', '7.30:9.30'), ('2', '10.00:12:00'), ('3', '13.00:15.00'), ('4', '15.30:17.30')], max_length=150)),
                ('date', models.DateField(default=datetime.date(2024, 7, 18))),
                ('status', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='certificates/')),
            ],
        ),
        migrations.CreateModel(
            name='Certificates_example',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='certificates/')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('title', models.TextField(blank=True, null=True)),
                ('price', models.PositiveBigIntegerField()),
                ('time', models.CharField(max_length=150)),
                ('days', models.CharField(choices=[('1', 'Dush-Chor-Jum'), ('2', 'Sesh-Pay-Shan')], max_length=150)),
                ('room', models.PositiveBigIntegerField()),
                ('start_date', models.DateField(blank=True, default=datetime.date(2024, 7, 18), null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_ended', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Course_for_news',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='kurs nomini kiriting', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveBigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DynamicField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('field_type', models.CharField(choices=[('char', 'CharField'), ('int', 'IntegerField'), ('choice', 'ChoiceField')], max_length=10)),
                ('choices', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=5, validators=[course.validators.validate_grade])),
            ],
        ),
        migrations.CreateModel(
            name='Receiption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(help_text='Raqam faqat +998 dan boshlanib 9 ta raqamdan tashkil topishi lozim misol uchun: +998991234567', max_length=13, validators=[course.validators.validate_phone_number])),
                ('created_at', models.DateField(default=datetime.date(2024, 7, 18))),
                ('info_text', models.TextField(max_length=100)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ReceiptionAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(help_text='Raqam faqat +998 dan boshlanib 9 ta raqamdan tashkil topishi lozim misol uchun: +998991234567', max_length=13, validators=[course.validators.validate_phone_number])),
                ('created_at', models.DateField(default=datetime.date(2024, 7, 18))),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=120)),
                ('wallet', models.IntegerField(default=0)),
                ('token_id', models.CharField(default='68524924', max_length=150, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='students/')),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('task_name', models.CharField(max_length=100)),
                ('file', models.FileField(blank=True, null=True, upload_to='tasks/')),
                ('task', models.TextField()),
                ('task_description', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Kurs', to='course.course')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
