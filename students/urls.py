from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('',views.home,name='home'),
    path('navbar', views.navbar, name='navbar'),
    path('student_list/', views.student_list, name='student_list'),
    path('marks/<int:student_id>/', views.marks_view, name='marks_view'),
    path('students/attendance/<int:student_id>/', views.attendance_view, name='attendance_view'),  
    path('timetable/<int:student_id>/', views.timetable_view, name='timetable_view'),
    path('classes/', views.class_list, name='class_list'),
    path('classes/<int:class_id>/', views.class_detail, name='class_detail'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('submit_attendance/', views.submit_attendance, name='submit_attendance'),
    path('classes/add/', views.add_class, name='add_class'),
    path('classes/<int:class_id>/add_student/', views.add_student_to_class, name='add_student_to_class'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    
    path('students/<int:student_id>/timetable/', views.timetable_view, name='timetable_view'),
    path('students/<int:student_id>/marks/', views.marks_view, name='marks_view'),
    path('students/edit_student/<int:pk>/', views.edit_student, name='edit_student'),
    path('students/confirm_delete/<int:pk>/', views.confirm_delete, name='confirm_delete'),
    # path('classes/<int:class_id>/attendance/', views.class_attendance, name='class_attendance'),
    path('classes/<int:class_id>/attendance/', views.class_attendance, name='class_attendance'),
    path('logout/', views.logout_view, name='logout'),


    path('classes/<int:class_id>/marks/', views.class_marks, name='class_marks'),


    path('students/class/<int:class_id>/', views.class_student_list, name='class_student_list'),

    path('confirm_delete_class/<int:class_id>/', views.confirm_delete_class, name='confirm_delete_class'),

    path('edit_student_attendance/<int:student_id>/<str:date>/', views.edit_student_attendance, name='edit_student_attendance'),


   

    
]
