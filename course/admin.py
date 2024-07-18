from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib import admin
from .models import Task, Grade

admin.site.register(DynamicField)
admin.site.register(RegistrationData)
admin.site.register(Deal)
admin.site.register(StudentCourse)

class AttendanceInline(admin.TabularInline):
      model = Attendance


class AttendanceGroupAdmin(admin.ModelAdmin):
      list_display = ('course',  'time', 'status')
      inlines = [AttendanceInline]


class StudentAdmin(admin.ModelAdmin):
      model = Student
      list_display=( 'id', 'full_name', 'wallet', 'token_id')
      search_fields = ['name', 'email']  # Enable search on name and email

admin.site.register(AttendanceGroup, AttendanceGroupAdmin)
admin.site.register(Student, StudentAdmin)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ['students']  # Use filter_horizontal for many-to-many fields
    search_fields = ['name', 'students__name', 'students__email']  # Enable search on the course title




@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'owner', 'date', 'course')
    list_filter = ('owner', 'date', 'course')
    search_fields = ('task_name', 'owner__username', 'course__name')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'task', 'grade')
    list_filter = ('student', 'task__task_name')
    search_fields = ('student__full_name', 'task__task_name')


admin.site.register(Course_for_news)

admin.site.register(Receiption)
admin.site.register(Certificates_example)
admin.site.register(Certificate)

