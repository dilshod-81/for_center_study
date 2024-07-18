from django.urls import path
from .views import *
from course.views import *
from payment.views import *

urlpatterns = [
      path('', index, name='index'),
      path('reception-dashboard', reception_dashboard, name='reception-dashboard'),
      path('teacher-dashboard', teacher_dashboard, name='teacher-dashboard'),
      path('student-dashboard/', student_dashboard, name='student-dashboard'),
      path('create-task/', create_task, name='create_task'),
      path('evaluate-task-detail/<int:id>/', evaluate_task_detail, name='evaluate_task_detail'),
      path('evaluate-task/', evaluate_task, name='evaluate_task'),
      path('edit_grade/<int:grade_id>/', edit_grade, name='edit_grade'),
      path('update-status/<int:receiption_id>/', update_status, name='update-status'),
      path('receiption/update-status/<int:pk>/', toggle_status, name='update-status1'),
      path('attendance-detail/<int:id>', attendance_detail, name='attendance-detail'),
      path('course-detail/<int:id>', course_detail, name='course-detail'),
      path('attendance/<int:id>', attendance, name='attendance'),
      path('edit_receiption/<int:receiption_id>/', edit_receiption, name='edit_receiption'),
      path('receiption/edit/<int:pk>/', ReceiptionUpdateView.as_view(), name='edit_receiption1'),
      #Post viewlar
      #path('make-payment', make_payment, name='make-payment'),
      path('make-payment/', make_payment, name='make-payment'),
      path('print_chek/<int:id>/', print_chek, name='print_chek'),
      path('create-student', create_student, name='create-student'),
      path('receiption/', ReceiptionAdminListView.as_view(), name='all-reception'),
      path('receiption/active/', ReceiptionAdminListView.as_view(), {'status': True}, name='active-reception'),
      path('receiption/inactive/', ReceiptionAdminListView.as_view(), {'status': False}, name='inactive-reception'),

      path('add-student-to-course', add_student_to_course, name='add-student-to-course'),
      path('add_discount/', add_discount, name='add_discount'),
      path('view_discount/', view_discount, name='view_discount'),
      path('download_pdf/<int:id>/', download_pdf, name='download_pdf'),
      #Boss views
      path('staff/create-user', CreateUser.as_view(), name='create-user'),
      path('staff/edit-user/<int:pk>/', CreateUser.as_view(), name='create-user'),
      path('staff/courses/ended/', CourseListView.as_view(), {'ended': True}, name='ended-courses'),
      path('staff/courses/ongoing/', CourseListView.as_view(), {'ended': False}, name='ongoing-courses'),
      #path('staff/create-user', create_user_view, name='create-user'),
      path('staff/payments', payments, name='payments'),
      path('staff/teachers', teachers, name='teachers'),
      path('staff/teachers/active/', TeacherListView.as_view(), {'active': True}, name='active-teachers'),
      path('staff/teachers/inactive/', TeacherListView.as_view(), {'active': False}, name='inactive-teachers'),
      path('staff/students', students, name='students'),
      path('staff/salaries', salaries, name='salaries'),
      path('staff/give-salary/<int:teacher_id>', give_salary, name='give-salary'),
      path('staff/courses', courses, name='courses'),
      path('staff/edit-course/<int:pk>', EditCourse.as_view(), name='edit-course'),
      #path('staff/new-course', NewCourse.as_view(), name='create-course'),
      path('staff/new-course', create_coures_new, name='create-course'),
      path('course/<int:course_id>/', attendance_detail_for_admin, name='course_details'),
      path('register/', register, name='register'),
      path('register_student/', register_student, name='registerstudent'),
      path('success/', success, name='success'),
      path('submissions/', view_submissions, name='view_submissions'),  # led
      path('add_dynamic_field/', add_dynamic_field, name='add_dynamic_field'), #regis > add_denamik , list_denamik
      path('list_dynamic_fields/',list_dynamic_fields, name='list_dynamic_fields'),
      path('edit_dynamic_field/<int:pk>/',edit_dynamic_field, name='edit_dynamic_field'),
      path('delete_dynamic_field/<int:pk>/', delete_dynamic_field, name='delete_dynamic_field'),
      path('search/', search_certificates, name='search_certificates'),
      path('courses/download/<int:student_id>/<int:course_id>/', download_certificate, name='download_certificate'),
      path('ajax/search/', ajax_search_certificates, name='ajax_search_certificates'),
      path('uquvchi', DealListView.as_view(), name='deal'),
      path('uquvchi/create/', deal_create_view, name='deal_create'),
      path('student-courses/', student_course_list, name='student-course-list'),
      path('edit-student-courses/<int:id>/', edit_student_courses, name='edit-student-courses'),

]



