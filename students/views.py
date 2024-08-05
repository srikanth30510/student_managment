from django.http import HttpResponseRedirect, JsonResponse,HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ClassForm, PeriodForm, StudentForm, AttendanceForm,SignUpForm, TimetableForm, UpdateAttendanceForm,MarkForm
from .models import Student, Timetable, Mark, Attendance, Class,Period
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.forms import modelformset_factory
from django.core.exceptions import MultipleObjectsReturned
from django.urls import reverse
from datetime import date, datetime
import json

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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'students/register.html', {'form': form})

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
    classes = Class.objects.all()  

    if request.method == 'POST':
        class_id = request.POST.get('class_id')  
        if class_id == 'all':
            students = Student.objects.all()
        else:
            students = Student.objects.filter(student_class_id=class_id)
    else:
        students = Student.objects.all()

    return render(request, 'students/student_list.html', {'students': students, 'classes': classes})


def timetable_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    timetables = Timetable.objects.filter(student=student)
    return render(request, 'students/timetable_view.html', {'timetables': timetables, 'student': student})

'''def marks_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    marks = Mark.objects.filter(student=student)
    return render(request, 'students/marks_view.html', {'marks': marks, 'student': student})'''

from django.shortcuts import render, get_object_or_404
from .models import Student, Mark

def marks_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    marks = Mark.objects.filter(student=student)
    
    # Organize marks by test names
    marks_by_test = {}
    for mark in marks:
        test_name = mark.test
        if test_name not in marks_by_test:
            marks_by_test[test_name] = []
        marks_by_test[test_name].append(mark)
    
    
    return render(request, 'students/marks_view.html', {
        
        'marks_by_test': marks_by_test,
        'mark':mark  
    })


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

''' def class_marks(request, class_id):
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
    }) '''

def class_student_list(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(student_class=student_class)
    
    return render(request, 'students/class_student_list.html', {
        'student_class': student_class,
        'students': students
    }) 

def confirm_delete_class(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        student_class.delete()
        messages.success(request, 'Class deleted successfully.')
        return redirect('class_list')  # Replace 'class_list' with your actual class list view name
    return render(request, 'students/confirm_delete_class.html', {'student_class': student_class})

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

'''def class_marks_view(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(student_class=student_class)
    
    # Fetch marks for all students in the class
    marks = Mark.objects.filter(student__in=students)
    
    return render(request, 'students/class_marks_view.html', {
        'student_class': student_class,
        'students': students,
        'marks': marks  # Pass marks to the template
    })'''

from django.shortcuts import render, get_object_or_404
from .models import Class, Student, Mark

def class_marks_view(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(student_class=student_class)
    
    # Fetch marks for all students in the class
    marks = Mark.objects.filter(student__in=students)
    
    # Organize marks by test names
    marks_by_test = {}
    for mark in marks:
        test_name = mark.test
        if test_name not in marks_by_test:
            marks_by_test[test_name] = []
        marks_by_test[test_name].append(mark)
    
    return render(request, 'students/class_marks_view.html', {
        'student_class': student_class,
        'students': students,
        'marks_by_test': marks_by_test,
        'marks':mark  # Pass marks organized by test to the template
    })


def attendance_update(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = UpdateAttendanceForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            date = form.cleaned_data['date']
            period = form.cleaned_data['period']
            try:
                attendance = Attendance.objects.get(student=student, date=date, period=period)
                attendance.status = status
                attendance.save()
                messages.success(request, 'Attendance updated successfully.')
            except Attendance.DoesNotExist:
                attendance = Attendance(student=student, date=date, period=period, status=status)
                attendance.save()
                messages.success(request, 'Attendance recorded successfully.')
            
            return redirect('class_student_list', class_id=student.student_class.id)
    else:
        form = UpdateAttendanceForm()
    return render(request, 'students/attendance_update.html', {'form': form, 'student': student})

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



# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.contrib import messages
# from .models import Class, Student, Mark
# from .forms import MarkForm

# def class_marks(request, class_id):
#     student_class = get_object_or_404(Class, id=class_id)
#     students = Student.objects.filter(student_class=student_class)
    
#     if request.method == 'POST':
#         forms = [
#             (student, MarkForm(request.POST, prefix=str(student.id), instance=Mark(student=student)))
#             for student in students
#         ]
        
#         all_valid = True
#         for student, form in forms:
#             if form.is_valid():
#                 form.save()
#             else:
#                 all_valid = False
#                 print(form.errors)
        
#         if all_valid:
#             messages.success(request, "Marks submitted successfully!")
#             return HttpResponseRedirect(reverse('class_marks', args=[class_id]))
    
#     else:
#         forms = [
#             (student, MarkForm(prefix=str(student.id), instance=Mark(student=student)))
#             for student in students
#         ]
    
#     return render(request, 'students/class_marks.html', {
#         'student_class': student_class,
#         'students': forms
#     })

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
        test_name = request.POST.get('test_name')
        all_valid = True

        forms = []  # Initialize the forms list

        for student in students:
            form_data = request.POST.copy()
            form_data[f'{student.id}-test'] = test_name  # Ensure the test name is set in the form data with prefix
            form = MarkForm(form_data, prefix=str(student.id), instance=Mark(student=student))
            forms.append((student, form))  # Append the form to the forms list
            if form.is_valid():
                form.save()
            else:
                all_valid = False
                print(form.errors)
        
        if all_valid:
            messages.success(request, "Marks submitted successfully!")
            return HttpResponseRedirect(reverse('class_marks', args=[class_id]))
    
    else:
        forms = [
            (student, MarkForm(prefix=str(student.id), instance=Mark(student=student)))
            for student in students
        ]
    
    return render(request, 'students/class_marks.html', {
        'student_class': student_class,
        'students': forms
    })

def add_period(request):
    if request.method == 'POST':
        form=PeriodForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('class_list'))    
    else:
        form=PeriodForm()
    return render(request,'students/add_period.html',{'form':form})



def add_timetable(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('class_list'))  
    else:
        form = TimetableForm()
    return render(request, 'students/add_timetable.html', {'form': form})

def view_timetable(request, class_id):
    student_class = Class.objects.get(id=class_id)
    timetables = student_class.timetables.all()
    return render(request, 'students/view_timetable.html', {'student_class': student_class, 'timetables': timetables})