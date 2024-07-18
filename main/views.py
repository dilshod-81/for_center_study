from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.generics import get_object_or_404
from django.utils import timezone
from course.models import *
from payment.models import *
from datetime import date, timedelta, datetime
from course.forms import *
from payment.utils import income_of_teacher_between_dates, calculate_total_discounted_amount
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import FileResponse
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib import messages
from payment.models import PayToCourse, Student, Course, AddCashToWallet, GiveSalary
from django.utils.timezone import now
from django.views.generic import ListView
from users.models import User


"""Bu ustoz o'tadigan darslarni filter qiluvchi funksiya """
def get_courses(request):
    if request.user.is_authenticated:
        teacher = request.user
        courses = Course.objects.filter(teacher=teacher)

        return courses
    else:
        pass


" Userlarni ularning klanlarigan qarab sahifalarga yuboruvchi index "
@login_required
def index(request):
    if request.user.is_teacher == True:
        return redirect('teacher-dashboard')
    elif request.user.is_admin == True:
        return redirect('reception-dashboard')
    elif request.user.is_student == True:
        return redirect('student-dashboard')
    elif request.user.is_staff == True:
        return redirect('income')
    else:
        return HttpResponse('Something is wrong with your account')


"Reception uchun dashboard"


@login_required
def reception_dashboard(request):
    if request.user.is_admin or request.user.is_staff:
        form = CourseFilterForm(request.GET)
        tulov = AddCashToWallet.objects.all().order_by('-date', '-time')

        receiptions = Receiption.objects.all().order_by('-created_at', 'status')

        if form.is_valid() and form.cleaned_data['course']:
            receiptions = receiptions.filter(full_name__icontains=form.cleaned_data['course'])

        courses = Course.objects.filter(is_ended=False)
        for course in courses:
            if course.days == "1":
                course.days = "Dush-Chor-Jum"
            elif course.days == "2":
                course.days = "Sesh-Pay-Shan"

        context = {
            'students': Student.objects.all(),
            'courses': courses,
            'course_id': Course_for_news.objects.all(),
            'receiptions': receiptions,
            'tulov': tulov,
            'form': form
        }
        return render(request, 'reception-dashboard.html', context)
    else:
        messages.warning(request, "Bu sahifaga kirish mumkin emas.")
        return redirect('index')



"""Teacher uchun dasahboard"""

# @login_required
# def teacher_dashboard(request):
#     if not request.user.is_teacher:
#         return HttpResponse("Unauthorized access", status=403)
#     teacher = request.user
#     courses = Course.objects.filter(teacher=teacher)
#
#     todays_courses = []
#     todays_income = 0
#
#     start = date.today() - timedelta(days=30)
#     end = date.today()
#     income_between_dates = income_of_teacher_between_dates(request, start, end)
#
#     "Bugun bu o'qituvchida qaysi va qachon darsi borligini ko'rsatib turuvchi filter"
#     for course in courses:
#         weekday = date.today().weekday()
#         if int(course.days) == 1 and course.start_date <= date.today():
#             if weekday == 0 or weekday == 2 or weekday == 4:
#                 todays_courses.append(course)
#         elif int(course.days) == 2 and course.start_date <= date.today():
#             if weekday == 1 or weekday == 3 or weekday == 5:
#                 todays_courses.append(course)
#
#     "Bugun  o'qituvchi qancha daromad topganini ko'rsatib turuvchi filter"
#     pay_to_courses = PayToCourse.objects.filter(course__in=todays_courses, date=date.today())
#
#     for i in pay_to_courses:
#         todays_income += i.transfer_summ / 2
#
#     "Ma'lum bir oraliqdagi o'qituvchini qacha daromad qilganini hisoblash uchun forma"
#     if request.method == "POST":
#         start = request.POST['start']
#         end = request.POST['end']
#         income_between_dates = income_of_teacher_between_dates(request, start, end)
#         start = datetime.strptime(start, '%Y-%m-%d').date()  # Convert to date object
#         end = datetime.strptime(end, '%Y-%m-%d').date()  # Convert to date object
#
#
#     context = {
#         'todays_courses': todays_courses,
#         "courses": courses,
#         'start': start,
#         'end': end,
#         'income_between_dates': income_between_dates,
#         'todays_income': todays_income,
#         'pay_to_courses': pay_to_courses,
#     }
#
#     return render(request, 'teacher_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher:
        return HttpResponse("Unauthorized access", status=403)

    teacher = request.user
    courses = Course.objects.filter(teacher=teacher)
    todays_courses = []
    todays_income = 0

    start = date.today() - timedelta(days=30)
    end = date.today()
    income_between_dates = income_of_teacher_between_dates(request, start, end)

    # Filter today's courses
    for course in courses:
        weekday = date.today().weekday()
        if int(course.days) == 1 and course.start_date <= date.today():
            if weekday == 0 or weekday == 2 or weekday == 4:
                todays_courses.append(course)
        elif int(course.days) == 2 and course.start_date <= date.today():
            if weekday == 1 or weekday == 3 or weekday == 5:
                todays_courses.append(course)
    pay_to_courses = PayToCourse.objects.filter(course__in=todays_courses, date=date.today())
    # Calculate today's income for the teacher
    student_courses = StudentCourse.objects.filter(course__in=todays_courses)
    for student_course in student_courses:
        pay_to_courses = PayToCourse.objects.filter(course=student_course.course, date=date.today())
        for payment in pay_to_courses:
            todays_income += student_course.price

    # Handle form submission for income between dates
    if request.method == "POST":
        start = request.POST['start']
        end = request.POST['end']
        income_between_dates = income_of_teacher_between_dates(request, start, end)
        start = datetime.strptime(start, '%Y-%m-%d').date()  # Convert to date object
        end = datetime.strptime(end, '%Y-%m-%d').date()  # Convert to date object

    context = {
        'todays_courses': todays_courses,
        'courses': courses,
        'start': start,
        'end': end,
        'income_between_dates': income_between_dates,
        'todays_income': todays_income,
        'pay_to_courses': pay_to_courses,
    }

    return render(request, 'teacher_dashboard.html', context)

"""Har bor kurs yo'qlamasi uchun detail sahifa"""


@login_required
def attendance_detail(request, id):
    teacher = request.user
    course = Course.objects.get(id=id, teacher=teacher)
    students_of_course = course.students.all()
    attendance_group = AttendanceGroup.objects.filter(course=course).order_by("date")
    for i in students_of_course:
        for a in attendance_group:
            abs_students = []
            abs = Attendance.objects.filter(attendance=a)
            for b in abs:
                abs_students.append(b.student)
            if not i in abs_students:
                Attendance.objects.create(
                    student=i,
                    present=False,
                    attendance=a,
                    date=a.date

                )

        i.attendances = Attendance.objects.filter(student=i, attendance__in=attendance_group).order_by('date')

    context = {
        'course': course,
        'students': students_of_course,
        'attendance_group': attendance_group,
        'courses': get_courses(request)

    }
    return render(request, 'attendance-detail.html', context)
"""Yo'qlamani amalga oshirish"""



# @login_required
# def attendance(request, id):
#     attendancegroup = get_object_or_404(AttendanceGroup, id=id)
#     students = attendancegroup.course.students.all()
#
#     if request.method == "POST":
#         for student in students:
#             present = str(student.id) in request.POST
#             status = request.POST.get(f'status_{student.id}', 'sababsiz')
#
#             # Create or update the attendance record
#             attendance_record = Attendance.objects.create(
#                 attendance=attendancegroup,
#                 student=student,
#                 present=present,
#                 date=attendancegroup.date,
#                 status=status
#             )
#
#             # Update the wallet and create payment record if needed
#             if status in ['sababsiz', 'kelgan']:
#                 student.wallet -= attendancegroup.course.price
#                 student.save()
#                 if attendancegroup.course.price != 0:
#                     PayToCourse.objects.create(
#                         student=student,
#                         course=attendancegroup.course,
#                         transfer_summ=attendancegroup.course.price,
#                     )
#
#         total_number_of_students = students.count()
#         total_number_of_not_attended_students = Attendance.objects.filter(
#             attendance=attendancegroup,
#             present=False
#         ).count()
#
#         attendancegroup.status = f"{total_number_of_not_attended_students} of {total_number_of_students} students did not participate in that lesson"
#         attendancegroup.save()
#
#         messages.success(request, 'Davomat olindi.')
#         return redirect('course-detail', attendancegroup.course.id)
#
#     context = {
#         'students': students,
#         "attendancegroup": attendancegroup,
#         'courses': get_courses(request)
#     }
#     return render(request, 'attendance.html', context)

"""Har bor kurs  uchun detail sahifa"""
@login_required
def attendance(request, id):
    attendancegroup = get_object_or_404(AttendanceGroup, id=id)
    students = attendancegroup.course.students.all()

    if request.method == "POST":
        for student in students:
            present = str(student.id) in request.POST
            status = request.POST.get(f'status_{student.id}', 'sababsiz')

            # Find the StudentCourse record
            try:
                student_course = StudentCourse.objects.get(student=student, course=attendancegroup.course)
                price = student_course.price
            except StudentCourse.DoesNotExist:
                messages.error(request, f"No course price found for student {student.full_name}.")
                continue

            # Create or update the attendance record
            attendance_record = Attendance.objects.create(
                attendance=attendancegroup,
                student=student,
                present=present,
                date=attendancegroup.date,
                status=status
            )

            # Update the wallet and create payment record if needed
            if status in ['sababsiz', 'kelgan']:
                student.wallet -= price
                student.save()
                if price != 0:
                    PayToCourse.objects.create(
                        student=student,
                        course=attendancegroup.course,
                        transfer_summ=price,
                    )

        total_number_of_students = students.count()
        total_number_of_not_attended_students = Attendance.objects.filter(
            attendance=attendancegroup,
            present=False
        ).count()

        attendancegroup.status = f"{total_number_of_not_attended_students} of {total_number_of_students} students did not participate in that lesson"
        attendancegroup.save()

        messages.success(request, 'Davomat olindi.')
        return redirect('course-detail', attendancegroup.course.id)

    context = {
        'students': students,
        "attendancegroup": attendancegroup,
        'courses': get_courses(request)
    }
    return render(request, 'attendance.html', context)


@login_required
def course_detail(request, id):
    teacher = request.user
    course = Course.objects.get(id=id)


    """Quyidagi kodlar ustozni bugun shu guruhda darsi borligi yoki yo'qligini ko'rsatib turadi."""
    weekday = date.today().weekday()
    have_a_class = False

    if int(course.days) == 1 and course.start_date <= date.today():
        if weekday == 0 or weekday == 2 or weekday == 4:
            have_a_class = True
    elif int(course.days) == 2 and course.start_date <= date.today():
        if weekday == 1 or weekday == 3 or weekday == 5:
            have_a_class = True

        '''attendanceni boshlash'''
    if request.method == "POST":
        if AttendanceGroup.objects.filter(course=course, date=date.today()):
            attendance_a = AttendanceGroup.objects.get(course=course, date=date.today())

            messages.warning(request, "Davomatni o'zgartitib bo'lmaydi.")
            have_a_class = False

        else:
            attendance = AttendanceGroup.objects.create(
                course=course,
                time=course.time,
                date=date.today(),
                teacher=teacher,
                status='none'
            )
            messages.warning(request, "Ma'lumotlar olinganidan keyin uni o'zgartirib bo'lmaydi.")
            return redirect('attendance', attendance.id)

    context = {
        'course': course,
        'have_a_class': have_a_class,
        'courses': get_courses(request),

    }
    return render(request, 'course-detail.html', context)




@login_required
def make_payment(request):
    students = Student.objects.all()
    courses = Course.objects.all()


    if request.method == "POST":
        student = get_object_or_404(Student, id=request.POST['student_id'])
        course = get_object_or_404(Course, id=request.POST['course_id'])
        summ = int(request.POST['summ'])


        # Create an AddCashToWallet entry
        AddCashToWallet.objects.create(
            recepient=request.user,
            summ=summ,
            date=now(),
            student=student
        )
        messages.success(request, 'To\'lov qabul qilindi.')

        return redirect('reception-dashboard')


    context = {
        'students': students,
        'courses': courses,

    }
    return render(request, 'reception-dashboard.html', context)



"O'quvchi qo'shish"




@login_required
def print_chek(request, id):
    add_cash_to_wallet = get_object_or_404(AddCashToWallet, id=id)

    tulov = []
    qr_code_url = None

    tulov.append({
        'student': add_cash_to_wallet.student.full_name,
        'transfer_summ': add_cash_to_wallet.summ,
        'date': add_cash_to_wallet.date,
        'time': add_cash_to_wallet.time,
    })

    # Generate QR code for PDF download
    pdf_url = request.build_absolute_uri(f'/download_pdf/{add_cash_to_wallet.id}/')
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(pdf_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    add_cash_to_wallet.qr_code.save(f'qr_code_{add_cash_to_wallet.id}.png', ContentFile(buffer.getvalue()))

    # Prepare context to pass to the template
    context = {
        'pay_to_course': add_cash_to_wallet,
        'tulov': tulov,
        'qr_code_url': add_cash_to_wallet.qr_code.url,
    }

    return render(request, 'admin/print_cheque.html', context)


def download_pdf(request, id):
    add_cash_to_wallet = get_object_or_404(AddCashToWallet, id=id)

    # Generate QR code for PDF download
    pdf_url = request.build_absolute_uri(f'/download_pdf/{add_cash_to_wallet.id}/')
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(pdf_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Draw text content
    p.drawString(100, 800, f"Student: {add_cash_to_wallet.student.full_name}")
    p.drawString(100, 780, f"Summa: {add_cash_to_wallet.summ}")
    p.drawString(100, 760, f"Date: {add_cash_to_wallet.date}")
    p.drawString(100, 740, f"Time: {add_cash_to_wallet.time}")
    p.drawString(100, 720, "Academy: MRIT IT ACADEMY")
    p.drawString(100, 700, "Status: Hamyon uchun tulov")

    # Draw QR code
    qr_img_width, qr_img_height = qr_img.size
    p.drawInlineImage(qr_img, 100, 590, width=100, height=100)

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='cheque.pdf')

def create_student(request):

    if request.method == "POST":
        Receiption.objects.create(
            full_name=request.POST['full_name'],
            phone_number=request.POST['phone_number'],
            course_id=request.POST['course'],
            info_text=request.POST['info_text']
        )
        messages.success(request, 'O\'quvchi yaratildi')
        return redirect('reception-dashboard')
    course_id = Course_for_news.objects.get(id = request.POST['course_id'])

    return render(request, 'reception-dashboard.html', {'course_id': course_id})
#yangi

def create_coures_new(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        teacher_id = request.POST.get('teacher')
        title = request.POST.get('title')
        price = request.POST.get('price')
        students_ids = request.POST.getlist('students')
        time = request.POST.get('time')
        days = request.POST.get('days')
        room = request.POST.get('room')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_ended = request.POST.get('is_ended', False) == 'on'

        # Fetch the User instance for the teacher
        teacher = User.objects.get(id=teacher_id)

        # Create the Course instance
        course = Course.objects.create(
            name=name,
            teacher=teacher,
            title=title,
            price=price,
            days=days,
            room=room,
            time = time

        )
        # Add students to the course
        students = Student.objects.filter(id__in=students_ids)
        course.students.set(students)
        course.save()

        return redirect('create-course')  # Redirect to an appropriate page after saving

    # Prepare the context for GET request
    context = {
        'users': User.objects.filter(is_teacher=True),  # Assuming a custom user model or a way to filter teachers
        'students': Student.objects.all(),
        # 'days': [
        #     ('1', 'Dush-Chor-Jum-shanba'),
        #     ('2', 'Sesh-Pay-Shan')
        # ],
        'days': Course._meta.get_field('days').choices
    }
    return render(request, 'boss/create_course.html', context)


def add_student_to_course(request):
    if request.method == "POST":
        course = Course.objects.get(id=request.POST['course_id'])
        student = Student.objects.get(id=request.POST['student_id'])
        price = request.POST['price']
        if student in course.students.all():
            messages.warning(request, "O'quvchi mavjud.")

        else:
            StudentCourse.objects.create(course=course, student=student, price=price)
            course.students.add(student)
            messages.success(request, "O'quvchi qo'shildi.")
        return redirect('reception-dashboard')
    return HttpResponse('O\'quvchi qo\'shildi')

#yangi 16.07.2024
def student_course_list(request):
    student_courses = StudentCourse.objects.all()
    return render(request, 'admin/student_course_list.html', {'student_courses': student_courses})

class Aas(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'is_staff', 'is_admin', 'is_teacher', 'is_student',
                  'is_superuser')



class CreateUser(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    form_class = Aas
    template_name = 'boss/create_user.html'
    success_url = reverse_lazy('create-user')
    success_message = "Amal muvaffaqiyali bajarildi."

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance

        # Create Student if the user is a student
        if user.is_student:
            Student.objects.create(
                user=user,
                full_name=f"{user.first_name} {user.last_name}",
                phone_number=user.phone_number,
                wallet=0,
                token_id=str(random.randint(100000000000, 99999999999999999)),
                image=None
            )
        return response


@login_required
def payments(request):
    students = Student.objects.all().order_by('-id')
    if request.user.is_staff == True:
        all_payments = AddCashToWallet.objects.all().order_by('-date')
        if request.method == 'POST':
            start = request.POST['start']
            end = request.POST['end']
            if request.POST['student_id']:
                all_payments = AddCashToWallet.objects.filter(date__gte=start, date__lte=end,
                                                              student=Student.objects.get(
                                                                  id=request.POST['student_id'])).order_by('date')
            else:
                all_payments = AddCashToWallet.objects.filter(date__gte=start, date__lte=end).order_by('date')
        context = {
            "payments": all_payments,
            'students': students
        }
        return render(request, 'boss/all_payments.html', context)

    else:
        messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
        return redirect('index')


@login_required
def teachers(request):
    if request.user.is_staff == True:
        teachers = User.objects.filter(is_teacher=True)
        for i in teachers:
            i.courses = Course.objects.filter(teacher=i)

        return render(request, 'boss/all_teachers.html', {"teachers": teachers})

    else:
        messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
        return redirect('index')


@login_required
def give_salary(request, teacher_id):
    teacher = User.objects.get(id=teacher_id, is_teacher=True)

    if request.user.is_staff == True and teacher.is_teacher == True:

        if request.method == 'POST':
            salary_summ = request.POST['summ']
            GiveSalary.objects.create(teacher=teacher, salary_summ=salary_summ, sender=request.user)
            messages.success(request, "Amal bajarildi.")
            return redirect('teachers')
        return render(request, 'boss/giving_salary.html', {"teacher": teacher})

    else:
        messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
        return redirect('index')



class TeacherListView(ListView):
    model = User
    template_name = 'boss/all_teachers.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_teacher=True)
        active = self.kwargs.get('active', None)
        if active is not None:
            queryset = queryset.filter(is_active=active)
        return queryset






@login_required
def students(request):
    if request.user.is_staff == True:
        students = Student.objects.all().order_by('-id')
        # Prepare a dictionary to hold students and their active courses
        students_with_active_courses = []
        for student in students:
            active_courses = Course.objects.filter(is_ended=False, students=student)
            students_with_active_courses.append({
                'student': student,
                'courses': active_courses,
            })

        return render(request, 'boss/all_students.html', {
            "students": students_with_active_courses
        })
    else:
        messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
        return redirect('index')



@login_required
def salaries(request):
    teachers = User.objects.filter(is_teacher=True)
    if request.user.is_staff == True:
        all_salaries = GiveSalary.objects.all().order_by('-date')
        if request.method == 'POST':
            start = request.POST['start']
            end = request.POST['end']

            try:
                all_salaries = GiveSalary.objects.filter(date__gte=start, date__lte=end, teacher=User.objects.filter(
                    id=request.POST['teacher_id'])).order_by('date')
            except:
                all_salaries = GiveSalary.objects.filter(date__gte=start, date__lte=end).order_by('date')

        return render(request, 'boss/all_salaries.html', {"salaries": all_salaries, 'teachers': teachers})

    else:
        messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
        return redirect('index')


def courses(request):
    teachers = User.objects.filter(is_teacher=True)
    if request.user.is_staff == True:
        courses = Course.objects.all()
        return render(request, 'boss/all_courses.html', {'courses': courses})
    else:
        messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
        return redirect('index')


class EditCourse(UpdateView, LoginRequiredMixin, SuccessMessageMixin):
    model = Course
    template_name = 'boss/edit_course.html'
    fields = ('name', 'teacher', 'title', 'price', 'students', 'days', 'room', 'end_date', 'is_ended')
    success_url = '/staff/courses'
    success_message = "Amal  muvaffaqiyali bajarildi."

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from course.models import StudentCourse, Student, Course


@login_required
def edit_student_courses(request, id):
    student_course = get_object_or_404(StudentCourse, id=id)
    if request.method == "POST":
        student_id = request.POST.get('student')
        course_id = request.POST.get('course')
        price = request.POST.get('price')

        student = get_object_or_404(Student, id=student_id)
        course = get_object_or_404(Course, id=course_id)

        student_course.student = student
        student_course.course = course
        student_course.price = price
        student_course.save()

        messages.success(request, "Student course updated successfully.")
        return redirect('student-course-list')  # Redirect to the student courses list

    students = Student.objects.all()
    courses = Course.objects.all()
    context = {
        'student_course': student_course,
        'students': students,
        'courses': courses,
    }
    return render(request, 'edit_student_courses.html', context)

class NewCourse(CreateView, LoginRequiredMixin, SuccessMessageMixin):
    model = Course
    template_name = 'boss/create_course.html'
    fields = ('name', 'teacher', 'title', 'price', 'students', 'days', 'room')
    success_message = "Amal  muvaffaqiyali bajarildi."
    success_url = '/'
    context_object_name = 'course_new'





def update_status(request, receiption_id):
    receiption = get_object_or_404(Receiption, pk=receiption_id)
    # Toggle status (assuming status is a boolean field)
    receiption.status = not receiption.status
    receiption.save()
    messages.success(request, f"{receiption.full_name} - o'quvchining  {receiption.course } kursiga  statusi yangilandi.")
    return redirect('reception-dashboard')

def toggle_status(request, pk):
    reception = get_object_or_404(Receiption, pk=pk)
    reception.status = not reception.status
    reception.save()
    return redirect(request.META.get('HTTP_REFERER', 'all-reception'))


def edit_receiption(request, receiption_id):
    receiption = get_object_or_404(Receiption, pk=receiption_id)

    if request.method == 'POST':
        form = ReceiptionForm(request.POST, instance=receiption)
        if form.is_valid():
            form.save()
            messages.success(request,f"{receiption.full_name}- o'quvchining {receiption.course} kursiga ma'lumotlari yangilandi.")
            return redirect('reception-dashboard')
    else:
        form = ReceiptionForm(instance=receiption)

    return render(request,'edit_receiption.html',{'form':form})

class ReceiptionUpdateView(UpdateView):
    model = Receiption
    fields = ['full_name', 'phone_number', 'course', 'status']
    template_name = 'edit_reception.html'
    success_url = reverse_lazy('all-reception')


@login_required
def attendance_detail_for_admin(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    teacher = course.teacher
    kun= Course._meta.get_field('days').choices  #yangi
    students_of_course = course.students.all()
    # students_count = students.count()
    attendance_group = AttendanceGroup.objects.filter(course=course).order_by("date")
    for i in students_of_course:
        for a in attendance_group:
            abs_students = []
            abs = Attendance.objects.filter(attendance=a)
            for b in abs:
                abs_students.append(b.student)
            if not i in abs_students:
                Attendance.objects.create(
                    student=i,
                    present=False,
                    attendance=a,
                    date=a.date
                )

        i.attendances = Attendance.objects.filter(student=i, attendance__in=attendance_group).order_by('date')

    context = {
        'course': course,
        'students': students_of_course,
        'teacher': teacher,
        'attendance_group': attendance_group,
        # 'students_count': students_count,
        'courses': get_courses(request),
        'kun': kun   #yangi
    }
    return render(request, 'course_details.html', context)


@login_required
def add_discount(request):
    if request.user.is_admin or request.user.is_staff:
        if request.method == 'POST':
            form = DiscountedStudentsForm(request.POST)
            if form.is_valid():
                discount = form.save(commit=False)
                discount.recepient = request.user  # Set the recipient to the logged-in user
                discount.save()

                # Create corresponding AddCashToWallet entry
                AddCashToWallet.objects.create(
                    student=discount.student,
                    summ=discount.discount_summ,
                    date=timezone.now().date(),
                    time=timezone.now().time(),
                    recepient=discount.recepient  # This is now set to request.user
                )

                # Success message
                messages.success(
                    request,
                    f"Siz {discount.student.full_name} ga chegirmali {discount.discount_summ} sum taqdim etdingiz !!!"
                )
                return redirect('income')  # Redirect to the income page

        else:
            form = DiscountedStudentsForm()

    return render(request, 'add_discount.html', {'form': form})


@login_required
def view_discount(request):
    discounts = Discounted_students.objects.select_related('student').all().order_by('-date','-time')

    total_discount = calculate_total_discounted_amount
    context = {
        'discounts': discounts,
        'total_discount': total_discount,

    }
    return render(request, 'view_discount.html', context)


