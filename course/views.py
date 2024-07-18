from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import *
from django.http import HttpResponse
from django.http import JsonResponse
from payment.models import AddCashToWallet
from main.views import get_courses
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Course, Student, Certificates_example
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
@login_required
def student_dashboard(request):
    if request.user.is_student:
        # Fetch the Student instance related to the user
        try:
            student = request.user.student
        except Student.DoesNotExist:
            return HttpResponse("Student profile not found.")

        # Redirect if the wallet balance is less than -500000
        if student.wallet <= -500000:
            return HttpResponse("Sizning hamyoningizda katta qarz bor. Ilova foydalanish bloklandi.")
        student_attendance = Attendance.objects.filter(student=student)
        # Get all courses the student is enrolled in
        courses = Course.objects.filter(students=student)
        payments = AddCashToWallet.objects.filter(student=student).order_by('-date','-time')




        if courses.exists():
            tasks = Task.objects.filter(course__in=courses).select_related('course')
            grades = Grade.objects.filter(student=student)
            context = {
                'tasks': tasks,
                'grades': grades,
                'student_wallet': student.wallet,
                'payments': payments,

            }
            return render(request, 'student_dashboard.html', context)
        else:
            return HttpResponse("You are not enrolled in any course.")

    else:
        return redirect('login')



@login_required
def create_task(request):
    teacher = request.user
    courses = Course.objects.filter(teacher=teacher)

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect('teacher-dashboard')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})


@login_required
def evaluate_task_detail(request, id):
    task = get_object_or_404(Task, pk=id)

    if request.user.is_teacher and request.user == task.owner:
        course = task.course
        students = course.students.all()

        if request.method == 'POST':
            form = GradeForm(course, request.POST)
            if form.is_valid():
                grade = form.save(commit=False)
                grade.task = task
                grade.save()
                return redirect('teacher-dashboard')
        else:
            form = GradeForm(course=course)  # Pass the course argument here

        grades = task.grades.all()

        context = {
            'task': task,
            'students': students,
            'grades': grades,
            'form': form,
        }

        return render(request, 'evaluate_task_detail.html', context)
    else:
        return redirect('login')
@login_required
def evaluate_task(request):

    if request.user.is_teacher:
        tasks = Task.objects.all()
        students = Student.objects.all()

        context = {
            'tasks': tasks,
            'students': students
        }

        return render(request, 'evaluate_task.html', context)
    else:
        return redirect('login')


@login_required
def edit_grade(request, grade_id):
    grade = get_object_or_404(Grade, pk=grade_id)
    task = grade.task

    if request.user.is_teacher and request.user == task.owner:
        if request.method == 'POST':
            form = EditGradeForm(request.POST, instance=grade)
            if form.is_valid():
                form.save()
                return redirect('evaluate_task')
        else:
            form = EditGradeForm(instance=grade)

        context = {
            'form': form,
            'grade': grade,
        }
        return render(request, 'edit_grade.html', context)
    else:
        return redirect('login')


def register(request):
    if request.method == 'POST':
        form = DynamicForm(request.POST)
        if form.is_valid():
            # Get all dynamic fields
            dynamic_fields = DynamicField.objects.all()
            # Create a dictionary to store the form data with field types
            registration_data = {}
            for field in dynamic_fields:
                field_name = field.name
                field_value = form.cleaned_data[field_name]
                field_type = field.get_field_type_display()
                registration_data[field_name] = {'value': field_value, 'type': field_type}
            # Save the data to the model
            RegistrationData.objects.create(data=registration_data)
            return redirect('success')
    else:
        form = DynamicForm()
    return render(request, 'register.html', {'form': form})

def register_student(request):
    if request.method == 'POST':
        form = DynamicForm(request.POST)
        if form.is_valid():
            # Get all dynamic fields
            dynamic_fields = DynamicField.objects.all()
            # Create a dictionary to store the form data with field types
            registration_data = {}
            for field in dynamic_fields:
                field_name = field.name
                field_value = form.cleaned_data[field_name]
                field_type = field.get_field_type_display()
                registration_data[field_name] = {'value': field_value, 'type': field_type}
            # Save the data to the model
            RegistrationData.objects.create(data=registration_data)
            return redirect('success')
    else:
        form = DynamicForm()
    return render(request, 'register_student.html', {'form': form})

def success(request):
    return render(request, 'success.html')



# myapp/views.py
def view_submissions(request):
    submissions = RegistrationData.objects.all()
    context = {
        'submissions': submissions
    }
    return render(request, 'view_submissions.html', context)


def add_dynamic_field(request):
    if request.method == 'POST':
        form = DynamicFieldForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_dynamic_fields')
    else:
        form = DynamicFieldForm()
    return render(request, 'add_dynamic_field.html', {'form': form})

def list_dynamic_fields(request):
    fields = DynamicField.objects.all()
    return render(request, 'list_dynamic_fields.html', {'fields': fields})

def edit_dynamic_field(request, pk):
    field = get_object_or_404(DynamicField, pk=pk)
    if request.method == 'POST':
        form = DynamicFieldForm(request.POST, instance=field)
        if form.is_valid():
            form.save()
            return redirect('list_dynamic_fields')
    else:
        form = DynamicFieldForm(instance=field)
    return render(request, 'edit_dynamic_field.html', {'form': form})


def delete_dynamic_field(request, pk):
    field = get_object_or_404(DynamicField, pk=pk)
    if request.method == 'POST':
        field.delete()
        return JsonResponse({'message': 'Field deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def search_certificates(request):
    query = request.GET.get('q')
    certificates = Certificate.objects.all()

    if query:
        certificates = certificates.filter(student__full_name__icontains=query)

    context = {
        'certificates': certificates,
        'query': query
    }
    return render(request, 'courses/search_certificates.html', context)




def ajax_search_certificates(request):
    query = request.GET.get('q', '')
    if query:
        students = Student.objects.filter(full_name__icontains=query)
        results = []
        for student in students:
            courses = student.course_set.filter(is_ended=True)
            for course in courses:
                results.append({
                    'student_name': student.full_name,
                    'course_name': course.name,
                    'download_url': f'/courses/download/{student.id}/{course.id}/',
                    'student_id': student.id,
                    'course_id': course.id
                })
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})





def generate_certificate(student, course):
    # Get the certificate template for the course
    try:
        template_obj = Certificates_example.objects.get(course=course)
        template_path = template_obj.pdf.path
    except Certificates_example.DoesNotExist:
        return None

    # Use the template to create a new certificate
    reader = PdfReader(template_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]

        # Create a new PDF with the student name and course name
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica-Bold", 33)
        can.setFillColorRGB(1, 1, 1)  # Set the text color to white
        can.drawString(100, 350, student.full_name)  # Adjust coordinates
        can.save()

        # Move to the beginning of the BytesIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)

        # Merge the new PDF with the existing page
        page.merge_page(new_pdf.pages[0])
        writer.add_page(page)

    # Save the new PDF to a BytesIO buffer
    output = BytesIO()
    writer.write(output)
    output.seek(0)

    return output


def download_certificate(request, student_id, course_id):
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)

    if not course.is_ended:
        return HttpResponse("Course has not ended yet.", status=400)

    pdf_buffer = generate_certificate(student, course)
    if pdf_buffer is None:
        return HttpResponse("Certificate template not found.", status=404)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.full_name}_{course.name}.pdf"'
    return response



from django.shortcuts import render
from django.views.generic import ListView
from .models import Course

class CourseListView(ListView):
    model = Course
    template_name = 'boss/all_courses.html'
    context_object_name = 'courses'

    def get_queryset(self):
        queryset = super().get_queryset()
        ended = self.kwargs.get('ended', None)
        if ended is not None:
            queryset = queryset.filter(is_ended=ended)
        return queryset



from django.shortcuts import render
from django.views.generic import ListView
from .models import ReceiptionAdmin

class ReceiptionAdminListView(ListView):
    model = Receiption
    template_name = 'reception_list.html'
    context_object_name = 'receptions'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.kwargs.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset



class DealListView(ListView):
    model = Deal
    template_name = 'admin/deal.html'
    context_object_name = 'uquvchi'

from .forms import DealForm

def deal_create_view(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('deal')  # Redirect to a list view or another page after saving
    else:
        form = DealForm()
    return render(request, 'admin/deal_form.html', {'form': form})


