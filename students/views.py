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

def navbar(request):
    return render(request, 'students/navbar.html')

def home(request):
    students = Student.objects.all()
    return render(request, 'students/home.html', {'students': students})

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    
    return render(request, 'students/register.html', {'form': form})

    
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'students/login.html', {'form': form})

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
from django.shortcuts import render, get_object_or_404
from .models import Student, Attendance

def attendance_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    attendances = Attendance.objects.filter(student=student)
    
    total_conducted = attendances.count()
    total_present = attendances.filter(status='Present').count()
    total_absent = attendances.filter(status='Absent').count()
    attendance_percentage = round((total_present / total_conducted) * 100,0 ) if total_conducted > 0 else 0

    context = {
        'attendances': attendances,
        'student': student,
        'total_conducted': total_conducted,
        'total_present': total_present,
        'total_absent': total_absent,
        'attendance_percentage': attendance_percentage
    }
    
    return render(request, 'students/attendance_view.html', context)



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



# def class_detail(request, class_id):
#     student_class = get_object_or_404(Class, id=class_id)
#     students = Student.objects.filter(student_class=student_class)
    
#     if request.method == 'POST':
#         forms = [
#             (student, AttendanceForm(request.POST, prefix=str(student.id), initial={'student': student, 'date': date.today()}))
#             for student in students
#         ]
        
#         all_valid = True
#         for student, form in forms:
#             if form.is_valid():
#                 pass
#             else:
#                 all_valid = False
        
#         if all_valid:
#             for student, form in forms:
#                 attendance = form.save(commit=False)
#                 attendance.date = date.today()
#                 attendance.save()
#             messages.success(request, "Attendance submitted successfully!")
#             return HttpResponseRedirect(reverse('class_detail', args=[class_id]))
    
#     else:
#         forms = [
#             (student, AttendanceForm(prefix=str(student.id), initial={'student': student, 'date': date.today()}))
#             for student in students
#         ]
    
#     return render(request, 'students/class_detail.html', {
#         'student_class': student_class,
#         'students': forms  
#     })

# views.py
# views.py
# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.contrib import messages
# from .models import Class, Student, Attendance, Period
# from .forms import AttendanceForm

# def class_detail(request, class_id):
#     student_class = get_object_or_404(Class, pk=class_id)
#     students = Student.objects.filter(student_class=student_class)
#     periods = Period.objects.all()

#     if request.method == 'POST':
#         for student in students:
#             date = request.POST.get('date')
#             period_id = request.POST.get('period')
#             status = request.POST.get(f'status_{student.id}')
            
#             # Debugging output
#             print(f"Student ID: {student.id}, Date: {date}, Period ID: {period_id}, Status: {status}")
            
#             if not status:
#                 messages.error(request, f'Status for student {student.name} is missing.')
#                 return HttpResponseRedirect(reverse('class_detail', args=[class_id]))

#             period = Period.objects.get(id=period_id)
#             attendance, created = Attendance.objects.get_or_create(
#                 student=student, date=date, period=period,
#                 defaults={'status': status}
#             )
#             if not created:
#                 attendance.status = status
#                 attendance.save()
#         messages.success(request, 'Attendance submitted successfully.')
#         return HttpResponseRedirect(reverse('class_detail', args=[class_id]))

#     forms = [(student, AttendanceForm(initial={'student': student, 'date': '2024-07-01', 'period': periods[0]})) for student in students]

#     return render(request, 'students/class_detail.html', {
#         'student_class': student_class,
#         'students': forms,
#         'periods': periods,
#     })
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Student, Attendance, Period, Class
from .forms import AttendanceForm

def class_detail(request, class_id):
    student_class = get_object_or_404(Class, pk=class_id)
    students = Student.objects.filter(student_class=student_class)
    
    today = timezone.now().date()
    selected_date = request.GET.get('date', today)
    periods = Period.objects.filter(date=selected_date)
    
    if request.method == 'POST':
        date = request.POST.get('date')
        period_id = request.POST.get('period')
        period = get_object_or_404(Period, id=period_id)
        
        # Check if attendance for this period already exists on the selected date
        existing_attendance = Attendance.objects.filter(period=period, date=date).exists()
        if existing_attendance:
            messages.success(request, f'ఇందాకే  "{period.name}" on {date} తీసుకున్నావు raa')
            return redirect('class_detail', class_id=class_id)
        
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            attendance, created = Attendance.objects.get_or_create(
                student=student, date=date, period=period,
                defaults={'status': status}
            )
            if not created:
                attendance.status = status
                attendance.save()

        messages.success(request, 'Attendance submitted successfully.')
        return redirect('class_detail', class_id=class_id)

    forms = [(student, AttendanceForm(initial={'student': student, 'date': selected_date, 'period': periods[0] if periods else None})) for student in students]

    return render(request, 'students/class_detail.html', {
        'student_class': student_class,
        'students': forms,
        'periods': periods,
        'selected_date': selected_date,
    })


def get_periods(request):
    date = request.GET.get('date')
    periods = Period.objects.filter(date=date)
    periods_data = [{'id': period.id, 'name': period.name, 'start_time': period.start_time, 'end_time': period.end_time} for period in periods]
    return JsonResponse({'periods': periods_data})



from .models import Period

def create_periods():
    periods = [
        {'name': 'Morning', 'start_time': '08:00:00', 'end_time': '12:00:00'},
        {'name': 'Afternoon', 'start_time': '12:00:00', 'end_time': '16:00:00'},
    ]
    for period in periods:
        Period.objects.get_or_create(**period)



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
    
    attendance_data = []
    for student in students:
        attendances = Attendance.objects.filter(student=student)
        total_conducted = attendances.count()
        total_present = attendances.filter(status='Present').count()
        total_absent = attendances.filter(status='Absent').count()
        attendance_percentage = (total_present / total_conducted) * 100 if total_conducted > 0 else 0
        
        attendance_data.append({
            'student': student,
            'total_conducted': total_conducted,
            'total_present': total_present,
            'total_absent': total_absent,
            'attendance_percentage': attendance_percentage,
        })

    return render(request, 'students/class_attendance.html', {
        'student_class': student_class,
        'attendance_data': attendance_data,
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

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
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
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from .models import Student, Attendance
# from .forms import AttendanceForm
# from datetime import date

# def attendance_update(request, student_id):
#     student = get_object_or_404(Student, id=student_id)
#     if request.method == 'POST':
#         form = UpdateAttendanceForm(request.POST)
#         if form.is_valid():
#             status = form.cleaned_data['status']
#             date = form.cleaned_data['date']
            
#             # Check if attendance for this student on this date already exists
#             try:
#                 attendance = Attendance.objects.get(student=student, date=date)
                
#                 # Update existing attendance record
#                 attendance.status = status
#                 attendance.save()
                
#                 messages.success(request, 'Attendance updated successfully.')
#             except Attendance.DoesNotExist:
#                 # Create new attendance record if none exists for this date
#                 attendance = Attendance(student=student, date=date, status=status)
#                 attendance.save()
                
#                 messages.success(request, 'Attendance recorded successfully.')
            
#             return redirect('class_student_list', class_id=student.student_class.id)
#     else:
#         # Handle GET request or form initialization
#         form = UpdateAttendanceForm()
    
#     # Render the template with the form
#     return render(request, 'students/attendance_update.html', {'form': form, 'student': student})

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student, Attendance, Period
from .forms import UpdateAttendanceForm

def attendance_update(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = UpdateAttendanceForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            date = form.cleaned_data['date']
            period = form.cleaned_data['period']
            
            # Check if attendance for this student on this date and period already exists
            try:
                attendance = Attendance.objects.get(student=student, date=date, period=period)
                
                # Update existing attendance record
                attendance.status = status
                attendance.save()
                
                messages.success(request, 'Attendance updated successfully.')
            except Attendance.DoesNotExist:
                # Create new attendance record if none exists for this date and period
                attendance = Attendance(student=student, date=date, period=period, status=status)
                attendance.save()
                
                messages.success(request, 'Attendance recorded successfully.')
            
            return redirect('class_student_list', class_id=student.student_class.id)
    else:
        # Handle GET request or form initialization
        form = UpdateAttendanceForm()
    
    # Render the template with the form
    return render(request, 'students/attendance_update.html', {'form': form, 'student': student})


# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Mark

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



