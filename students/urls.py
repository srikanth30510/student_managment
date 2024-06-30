from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls import handler403
from django.conf.urls.static import static


handler403 = views.permission_denied_view

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('home/',views.home,name='home'),
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


    path('class_marks/<int:class_id>/', views.class_marks, name='class_marks'),

    path('class_marks_view/<int:class_id>/', views.class_marks_view, name='class_marks_view'),

# urls.py
    path('students/<int:student_id>/attendance_update/', views.attendance_update, name='attendance_update'),

    path('students/marks_update/<int:student_id>/', views.marks_update, name='marks_update'),

<<<<<<< HEAD
    # path('delete_mark/<int:mark_id>/delete/', views.delete_mark, name='delete_mark'),
    path('delete_mark_by_name/', views.delete_mark_by_name, name='delete_mark_by_name'),
=======
    path('delete_mark/<int:mark_id>/', views.delete_mark, name='delete_mark'),

>>>>>>> ad6e5b7a062d8e9f208d5036c41f56d30ebd7f44






    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)