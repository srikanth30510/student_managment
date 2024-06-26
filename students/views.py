from django.urls import reverse
from datetime import date
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ClassForm, StudentForm, AttendanceForm,SignUpForm
from .models import Student, Timetable, Mark, Attendance, Class
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

def navbar(request):
    return render(request, 'students/navbar.html')

def home(request):
    students = Student.objects.all()
    return render(request, 'students/home.html', {'students': students})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect('login')
        else:
            form=SignUpForm()
        return render(request,'students/register.html',{'form':form})
    
def login_view(request):
    if request.method == 'POST':
        form =AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                form=AuthenticationForm()
            return render(request,'students/login.html',{'form': form})
        
def logout_view(request):
    logout(request)
    return redirect('home')

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
        'students': forms  
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

def class_attendance(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(student_class=student_class)
    attendances = Attendance.objects.filter(student__in=students).order_by('date')

    return render(request, 'students/class_attendance.html', {
        'student_class': student_class,
        'students': students,
        'attendances': attendances,
    })


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


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Class, Attendance, Student
from .forms import AttendanceFormSet

def update_attendance_view(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(class_instance=class_instance)

    # Fetch existing attendance records or create new ones if they don't exist
    attendance_records = [Attendance.objects.get_or_create(student=student, date=date.today())[0] for student in students]

    if request.method == 'POST':
        formset = AttendanceFormSet(request.POST, queryset=Attendance.objects.filter(student__in=students, date=date.today()))
        if formset.is_valid():
            formset.save()
            return redirect('attendance_success')  # Redirect to a success page or similar
    else:
        formset = AttendanceFormSet(queryset=Attendance.objects.filter(student__in=students, date=date.today()))

    return render(request, 'students/update_attendance.html', {'class_instance': class_instance, 'formset': formset})


# views.py
# views.py
# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Class, Student, Mark
from .forms import MarkForm
from django.forms import modelformset_factory
'''
def class_marks(request, class_id):
    student_class = get_object_or_404(Class, pk=class_id)
    students = Student.objects.filter(student_class=student_class)

    # Create a formset for Marks
    MarkFormSet = modelformset_factory(Mark, form=MarkForm, extra=len(students), can_delete=True)

    if request.method == 'POST':
        formset = MarkFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('students/marks_success.html')  # Redirect to a success page or similar
    else:
        initial_data = [{'student': student.id} for student in students]
        formset = MarkFormSet(queryset=Mark.objects.none(), initial=initial_data)

    return render(request, 'students/class_marks.html', {
        'student_class': student_class,
        'students': students,
        'formset': formset,
    })

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from .models import Class, Student, Mark
from .forms import MarkForm

def class_marks(request, class_id):
    student_class = get_object_or_404(Class, pk=class_id)
    students = Student.objects.filter(student_class=student_class)

    # Create a formset for Marks
    MarkFormSet = modelformset_factory(Mark, form=MarkForm, extra=len(students))

    if request.method == 'POST':
        formset = MarkFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return render(request, 'students/marks_success.html', {'student_class': student_class})
    else:
        initial_data = [{'student': student.id} for student in students]
        formset = MarkFormSet(queryset=Mark.objects.none(), initial=initial_data)

    return render(request, 'students/class_marks.html', {
        'student_class': student_class,
        'students': students,
        'formset': formset,
    })

def submit_marks(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data['student_id']
        subject = data['subject']
        mark = data['mark']

        # Get the student object
        student = Student.objects.get(id=student_id)

        # Create and save the mark object
        Mark.objects.create(student=student, subject=subject, mark=mark)
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400) '''


## views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Class, Student, Mark
from .forms import MarkForm

def class_marks(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(student_class=student_class)
    
    if request.method == 'POST':
        forms = [
            (student, MarkForm(request.POST, prefix=str(student.id), initial={'student': student}))
            for student in students
        ]
        
        all_valid = True
        for student, form in forms:
            if form.is_valid():
                form.save(commit=False)  # Save the form instance if valid
            else:
                all_valid = False
                # Print errors to console for debugging
                print(form.errors)
        
        if all_valid:
            for student, form in forms:
                form.save()  # Save the form with commit=True to save to database
            messages.success(request, "Marks submitted successfully!")
            return HttpResponseRedirect(reverse('class_marks', args=[class_id]))
    
    else:
        forms = [
            (student, MarkForm(prefix=str(student.id), initial={'student': student}))
            for student in students
        ]
    
    return render(request, 'students/class_marks.html', {
        'student_class': student_class,
        'students': forms
    })
