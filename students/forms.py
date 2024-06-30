from django import forms
from .models import Attendance,Student,Class,Mark
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

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = [ 'subject', 'mark'] 
    
class UpdateAttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }