from django import forms
from .models import Attendance,Student,Class


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

