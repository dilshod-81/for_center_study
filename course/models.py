from random import choices
from django.db import models
from users.models import User
from datetime import date
from django.utils import timezone
import random
from .validators import validate_grade, validate_phone_number
from django.db.models import Sum

# Create your models here.
times = (
    ('1', '7.30:9.30'),
    ('2', '10.00:12:00'),
    ('3', '13.00:15.00'),
    ('4', '15.30:17.30'),
)
days = (
    ('1', 'Dush-Chor-Jum'),
    ('2', 'Sesh-Pay-Shan')
)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=120)
    wallet = models.IntegerField(default=0)

    token_id = models.CharField(default=str(random.randint(10000000, 99999999)), max_length=150, unique=True)
    image = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return str(self.full_name)

    @staticmethod
    def get_wallet_sums():

        negative_wallet_sum = Student.objects.filter(wallet__lt=0).aggregate(Sum('wallet'))['wallet__sum'] or 0
        positive_wallet_sum = Student.objects.filter(wallet__gt=0).aggregate(Sum('wallet'))['wallet__sum'] or 0
        return negative_wallet_sum, positive_wallet_sum

class Course_for_news(models.Model):
    name = models.CharField(max_length=200, default="kurs nomini kiriting")

    def __str__(self):
        return self.name


class Receiption(models.Model):

    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(
        max_length=13,
        validators=[validate_phone_number],
        help_text="Raqam faqat +998 dan boshlanib 9 ta raqamdan tashkil topishi lozim misol uchun: +998991234567"
    )
    course = models.ForeignKey(Course_for_news, on_delete=models.CASCADE)
    created_at = models.DateField(default=date.today())
    info_text=models.TextField(max_length=100)
    status = models.BooleanField(default=False)

    def __str__(self):
        return (f"{self.full_name}"
                f"{self.course}"
                f"{self.phone_number} "
                f"{self.status} "
                f"{self.created_at}")

#yangi
class ReceiptionAdmin(models.Model):

    name = models.CharField(max_length=200)
    phone_number = models.CharField(
        max_length=13,
        validators=[validate_phone_number],
        help_text="Raqam faqat +998 dan boshlanib 9 ta raqamdan tashkil topishi lozim misol uchun: +998991234567"
    )
    course = models.ForeignKey(Course_for_news, on_delete=models.CASCADE)
    created_at = models.DateField(default=date.today())
    status = models.BooleanField(default=False)

    def __str__(self):
        return (f"{self.full_name}"
                f"{self.course}"
                f"{self.phone_number} "
                f"{self.status} "
                f"{self.created_at}")


class Course(models.Model):
    name = models.CharField(max_length=120)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(null=True, blank=True)
    price = models.PositiveBigIntegerField()
    students = models.ManyToManyField(Student)
    time = models.CharField(max_length=150)
    days = models.CharField(max_length=150, choices=days)
    room = models.PositiveBigIntegerField()
    start_date = models.DateField(default=date.today(), blank=True, null=True)
    end_date = models.DateField(null=True, blank=True)
    is_ended = models.BooleanField(default=False)

    def __str__(self):
        return (f"{self.name} "
                f"{self.teacher} "
                f"{self.title} "
                f"{self.price} "
                f"{self.students}"
                f"{self.time} "
                f"{self.days} "
                f"{self.room}")

class AttendanceGroup(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    time = models.CharField(max_length=150, choices=times)
    date = models.DateField(default=date.today())
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=150)

    def __str__(self):
        return str(self.status)

    #yangi 16.07.2024
class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Attendance(models.Model):
    attendance = models.ForeignKey(AttendanceGroup, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=date.today())
    present = models.BooleanField(default=True)
    STATUS_CHOICES = [
        ('sababli', 'sababli'),
        ('sababsiz', 'sababsiz'),
        ('kelgan', 'kelgan')
    ]
    status = models.CharField(max_length=150, choices=STATUS_CHOICES, default='kelgan', blank=True, null=True)

    def __str__(self):
        return str(self.student) + " " + str(self.present)


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_teacher': True})
    date = models.DateTimeField(default=timezone.now)
    task_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='tasks/', blank=True, null=True)
    task = models.TextField()
    task_description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='Kurs')

    def __str__(self):
        return str(self.task_name) + str(self.owner)


    class Meta:
        ordering = ['-date']


class Grade(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5, validators=[validate_grade])

    def __str__(self):
        return f"{self.student.full_name} - {self.task.task_name} - {self.grade}"


class DynamicField(models.Model):
    FIELD_TYPES = [
        ('char', 'CharField'),
        ('int', 'IntegerField'),
        ('choice', 'ChoiceField'),
    ]

    name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=10, choices=FIELD_TYPES)
    choices = models.TextField(blank=True, null=True)  # Used for ChoiceField

    def __str__(self):
        return self.name


class RegistrationData(models.Model):
    # This will store the name of the field and its value as a JSON object
    data = models.JSONField()

    def __str__(self):
        return str(self.data)



class Certificates_example(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='certificates/')

    def __str__(self):
        return str(self.course)


class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='certificates/')

    def __str__(self):
        return f'Certificate for {self.student.full_name} - {self.course.name}'

from .models import User

class Deal(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField()
    def __str__(self):
        return (f"{self.student} "
                f"{self.teacher} "
                f"{self.course} "
                f"{self.price} "

              )

