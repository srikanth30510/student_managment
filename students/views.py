from django.urls import reverse
from datetime import date
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ClassForm, StudentForm, AttendanceForm,SignUpForm, UpdateAttendanceForm
from .models import Student, Timetable, Mark, Attendance, Class
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test



def permission_denied_view(request, exception=None):
    return render(request, '403.html', status=403)

def admin_required(user):
    return user.is_superuser


def navbar(request):
    return render(request, 'students/navbar.html')

@login_required
def home(request):
    students = Student.objects.all()
    return render(request, 'students/home.html', {'students': students})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'students/register.html', {'form': form})


    
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'students/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

@login_required
def timetable_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    timetables = Timetable.objects.filter(student=student)
    return render(request, 'students/timetable_view.html', {'timetables': timetables, 'student': student})

@login_required
def marks_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    marks = Mark.objects.filter(student=student)
    return render(request, 'students/marks_view.html', {'marks': marks, 'student': student})


'''def attendance_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    attendances = Attendance.objects.filter(student=student)
    return render(request, 'students/attendance_view.html', {'attendances': attendances, 'student': student}) '''
@login_required
def attendance_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    # Query all attendance records for the student
    attendances = Attendance.objects.filter(student=student)
    
    total_conducted = attendances.count()
    total_present = attendances.filter(status='P').count()
    total_absent = total_conducted - total_present
    
    if total_conducted > 0:
        attendance_percentage = round((total_present / total_conducted) * 100,0)
    else:
        attendance_percentage = 0
    
    context = {
        'student': student,
        'attendances':attendances,
        'total_conducted': total_conducted,
        'total_present': total_present,
        'total_absent': total_absent,
        'attendance_percentage': attendance_percentage,
    }
    
    return render(request, 'students/attendance_view.html', context)

@login_required
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'students/class_list.html', {'classes': classes})

@login_required
@user_passes_test(admin_required)

def add_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('class_list'))
    else:
        form = ClassForm()
    return render(request, 'students/add_class.html', {'form': form})

@login_required
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

@login_required
@user_passes_test(admin_required)

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


@login_required
@user_passes_test(admin_required)

def confirm_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    
    return render(request, 'students/confirm_delete.html', {'student': student})


@login_required
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





@login_required
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    attendance = Attendance.objects.filter(student=student)
    return render(request, 'students/student_detail.html', {'student': student, 'attendance': attendance})

@login_required
def submit_attendance(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data['student_id']
        status = data['status']
        student = Student.objects.get(id=student_id)
        Attendance.objects.create(student=student, date=date.today(), status=status)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

'''@login_required
def class_attendance(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(student_class=student_class)
    attendances = Attendance.objects.filter(student__in=students).order_by('date')

    return render(request, 'students/class_attendance.html', {
        'student_class': student_class,
        'students': students,
        'attendances': attendances,
    })'''

from django.shortcuts import render, get_object_or_404
from .models import Attendance, Student, Class

def class_attendance(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(student_class=student_class)
    
    # Query attendance records for all students in the class
    attendances = Attendance.objects.filter(student__in=students).order_by('date')

    # Calculate attendance statistics for each student
    for student in students:
        total_conducted = attendances.filter(student=student).count()
        total_present = attendances.filter(student=student, status='P').count()

        if total_conducted > 0:
            attendance_percentage = round((total_present / total_conducted) * 100,0)
        else:
            attendance_percentage = 0

        # Attach calculated fields to each student object
        student.total_conducted = total_conducted
        student.total_present = total_present
        student.total_absent= total_conducted - total_present
        student.attendance_percentage = attendance_percentage

    return render(request, 'students/class_attendance.html', {
        'student_class': student_class,
        'students': students,
    })



@login_required
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



# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Class, Student, Mark
from .forms import MarkForm

@login_required
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
                mark = form.save(commit=False)  # Create form instance but don't save to database
                mark.student = student  # Assign the student to the mark instance
                mark.save()
            else:
                all_valid = False
                # Print errors to console for debugging
                print(form.errors)
        
        if all_valid:
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



from django.shortcuts import render, get_object_or_404
from .models import Class, Student

@login_required
def class_student_list(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(student_class=student_class)
    
    return render(request, 'students/class_student_list.html', {
        'student_class': student_class,
        'students': students
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Class

@login_required
@user_passes_test(admin_required)

def confirm_delete_class(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        student_class.delete()
        messages.success(request, 'Class deleted successfully.')
        return redirect('class_list')  # Replace 'class_list' with your actual class list view name
    return render(request, 'students/confirm_delete_class.html', {'student_class': student_class})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student, Attendance
from .forms import AttendanceForm
from datetime import datetime

@login_required
def edit_student_attendance(request, student_id, date):
    student = get_object_or_404(Student, id=student_id)
    attendance_date = datetime.strptime(date, '%Y-%m-%d').date()
    attendance = Attendance.objects.filter(student=student, date=attendance_date).first()

    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, f'Attendance updated successfully for {student.name}.')
            return redirect('class_detail', class_id=student.student_class.id)
    else:
        form = AttendanceForm(instance=attendance)

    return render(request, 'students/edit_student_attendance.html', {'student': student, 'form': form, 'date': attendance_date})


from django.shortcuts import render, get_object_or_404
from .models import Class, Student, Mark

@login_required
def class_marks_view(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(student_class=student_class)
    
    # Fetch marks for all students in the class
    marks = Mark.objects.filter(student__in=students)
    
    return render(request, 'students/class_marks_view.html', {
        'student_class': student_class,
        'students': students,
        'marks': marks  # Pass marks to the template
    })
# views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Student, Attendance
from .forms import AttendanceForm

@login_required
def attendance_update(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = UpdateAttendanceForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            date = form.cleaned_data['date']
            
            # Update or create attendance for the specific date
            attendance, created = Attendance.objects.update_or_create(
                student=student,
                date=date,
                defaults={'status': status}
            )
            
            if created:
                messages.success(request, 'Attendance created successfully.')
            else:
                messages.success(request, 'Attendance updated successfully.')
            
            return redirect('class_student_list', class_id=student.student_class.id)
    else:
        form = UpdateAttendanceForm()

    return render(request, 'students/attendance_update.html', {'form': form, 'student': student})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Mark

@login_required
def marks_update(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    marks = Mark.objects.filter(student=student)
    
    if request.method == 'POST':
        for mark in marks:
            new_mark = request.POST.get(str(mark.id), None)
            if new_mark is not None:
                mark.mark = new_mark
                mark.save()

        messages.success(request, 'Updated Marks successfully.')

        return redirect('marks_update', student_id=student.id)
    
    return render(request, 'students/marks_update.html', {'student': student, 'marks': marks})


# views.py
# views.py
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Mark
from django.http import HttpResponseBadRequest
from django.core.exceptions import MultipleObjectsReturned
from django.contrib import messages  # Import messages module

<<<<<<< HEAD
def delete_mark_by_name(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        subject_name = request.POST.get('subject_name')
        try:
            mark = Mark.objects.filter(student__name=student_name, subject=subject_name).first()
            if not mark:
                raise Mark.DoesNotExist("Mark not found for the given student and subject.")
            student_class_id = mark.student.student_class.id if mark.student and mark.student.student_class else None
            mark.delete()
            if student_class_id:
                return redirect('marks_view', student_class_id=student_class_id)
            else:
                return redirect('class_list') 
        except MultipleObjectsReturned as e:
            messages.error(request, 'Multiple marks found for the given student and subject. Contact support.')
            return redirect('class_list')
        except Mark.DoesNotExist as e:
            messages.error(request, str(e))
            return redirect('class_list')
        except Exception as e:
            messages.success(request, "Marks Deleted successfully!")
            return HttpResponseRedirect(reverse('class_marks_view', args=[student_class_id]))
    return HttpResponseBadRequest("Invalid request method.")
=======

def delete_mark(request, mark_id):
    mark = get_object_or_404(Mark, id=mark_id)
    
    if request.method == 'POST':
        student_class_id = mark.student.student_class.id if mark.student and mark.student.student_class else None
        mark.delete()
        if student_class_id:
            return redirect('marks_view', student_class_id=student_class_id)
        else:
            # Handle error or redirect to an appropriate page
            return redirect('class_list')  # Example fallback redirection
        
    return render(request, 'students/delete_mark.html', {'mark': mark})


from django.shortcuts import render, get_object_or_404
from .models import Attendance, Student, Class

def calculate_attendance_statistics(student, student_class):
    total_classes = Attendance.objects.filter(student=student, student_class=student_class).count()
    present_count = Attendance.objects.filter(student=student, student_class=student_class, status='Present').count()
    absent_count = total_classes - present_count  # Calculate absent classes
    
    if total_classes > 0:
        attendance_percentage = (present_count / total_classes) * 100
    else:
        attendance_percentage = 0
    
    return {
        'total_classes': total_classes,
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_percentage': attendance_percentage
    }

>>>>>>> ad6e5b7a062d8e9f208d5036c41f56d30ebd7f44

