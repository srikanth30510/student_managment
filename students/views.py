from django.urls import reverse
from datetime import date
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ClassForm, StudentForm, AttendanceForm
from .models import Student, Timetable, Mark, Attendance, Class
from django.contrib import messages

def navbar(request):
    return render(request, 'students/navbar.html')

def home(request):
    students = Student.objects.all()
    return render(request, 'students/home.html', {'students': students})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

def timetable_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    timetables = Timetable.objects.filter(student=student)
    return render(request, 'students/timetable_view.html', {'timetables': timetables, 'student': student})

def marks_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    marks = Mark.objects.filter(student=student)
    return render(request, 'students/marks_view.html', {'marks': marks, 'student': student})

def attendance_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    attendances = Attendance.objects.filter(student=student)
    return render(request, 'students/attendance_view.html', {'attendances': attendances, 'student': student})

def class_list(request):
    classes = Class.objects.all()
    return render(request, 'students/class_list.html', {'classes': classes})

def add_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('class_list'))
    else:
        form = ClassForm()
    return render(request, 'students/add_class.html', {'form': form})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('student_list'))
    else:
        form = StudentForm()
    return render(request, 'students/add_student.html', {'form': form})

# def edit_student(request,pk):
#     student=get_object_or_404(Student,pk=pk)
#     if request.method == 'POST':
#         form = StudentForm(request.POST,instance=student)
#         if form.is_valid():
#             form.save()
#             return redirect('student_list')
#     else:
#         form = StudentForm(instance=student)
#     return render(request, 'edit_student.html',{'form':form})

# def confirm_delete(request,pk):
#     student=get_object_or_404(Student,pk=pk)
#     if request.method == 'POST':
#         student.delete()
#         return redirect('student_list')
#     return render(request,'confirm_delete.html',{'student':student})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from .forms import StudentForm

def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'students/edit_student.html', {'form': form})

def confirm_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    
    return render(request, 'students/confirm_delete.html', {'student': student})



def class_detail(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(student_class=student_class)
    
    if request.method == 'POST':
        forms = [
            (student, AttendanceForm(request.POST, prefix=str(student.id), initial={'student': student, 'date': date.today()}))
            for student in students
        ]
        
        all_valid = True
        for student, form in forms:
            if form.is_valid():
                pass
            else:
                all_valid = False
        
        if all_valid:
            for student, form in forms:
                attendance = form.save(commit=False)
                attendance.date = date.today()
                attendance.save()
            messages.success(request, "Attendance submitted successfully!")
            return HttpResponseRedirect(reverse('class_detail', args=[class_id]))
    
    else:
        forms = [
            (student, AttendanceForm(prefix=str(student.id), initial={'student': student, 'date': date.today()}))
            for student in students
        ]
    
    return render(request, 'students/class_detail.html', {
        'student_class': student_class,
        'students': forms  # List of tuples: (student, form)
    })






def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    attendance = Attendance.objects.filter(student=student)
    return render(request, 'students/student_detail.html', {'student': student, 'attendance': attendance})

def submit_attendance(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data['student_id']
        status = data['status']
        student = Student.objects.get(id=student_id)
        Attendance.objects.create(student=student, date=date.today(), status=status)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

def add_student_to_class(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.student_class = student_class
            student.save()
            return HttpResponseRedirect(reverse('class_detail', args=[class_id]))
    else:
        form = StudentForm()
    return render(request, 'students/add_student_to_class.html', {'form': form, 'student_class': student_class})
