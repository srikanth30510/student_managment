from django.contrib import admin
from .models import Student,Timetable,Mark,Attendance
# Register your models here.

admin.site.register(Student)
admin.site.register(Timetable)
admin.site.register(Mark)
admin.site.register(Attendance)