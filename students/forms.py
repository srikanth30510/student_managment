from django import forms
from .models import Attendance,Student,Class,Mark, Timetable,Period
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'student_class','email','phone']



class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status', 'student', 'date']
        widgets = {
            'student': forms.HiddenInput(),
            'date': forms.HiddenInput(),
            'status': forms.RadioSelect(choices=[('P', 'Present'), ('A', 'Absent')])
        }

class SignUpForm(UserCreationForm):
    email=forms.EmailField(max_length=200,help_text='Required')

    class Meta:
        model=User
        fields=('username','email','password1','password2')

from django.forms import modelformset_factory

AttendanceFormSet = modelformset_factory(Attendance, fields=('student', 'status'), extra=0)

# class MarkForm(forms.ModelForm):
#     class Meta:
#         model = Mark
#         fields = ['test', 'subject', 'mark']
#         widgets = {
#             'test': forms.Select(attrs={'class': 'form-select'}),  # Example of adding a class to the form field
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['test'].required = True 
from django import forms
from .models import Mark

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['test', 'subject', 'mark']
        widgets = {
            'test': forms.Select(attrs={'class': 'form-select'}),  # Example of adding a class to the form field
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['test'].required = True 

    
# class UpdateAttendanceForm(forms.ModelForm):
#     class Meta:
#         model = Attendance
#         fields = ['status', 'date']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'})
#         }
# forms.py
class UpdateAttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status', 'date', 'period']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'period': forms.Select()
        }


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = '__all__'

from .models import Attendance, Period

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'period', 'status']
        widgets = {
            'student': forms.HiddenInput(),
            'date': forms.HiddenInput(),
            'period': forms.HiddenInput(),
        }

class PeriodForm(forms.ModelForm):
    class Meta:
        model=Period
        fields=['name','start_time','end_time','date']

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['day', 'time', 'subject', 'teacher', 'student_class']