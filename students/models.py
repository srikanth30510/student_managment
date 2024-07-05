from django.utils import timezone
from django.db import models
from django.shortcuts import render, get_object_or_404


class Class(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=10, unique=True)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    

    
class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test=models.CharField(max_length=10, choices=[('Test1', 'Test1'), ('Test2', 'Test2'),('Test3', 'Test3'),('Test4', 'Test4')])
    subject = models.CharField(max_length=50)
    mark = models.IntegerField()
    def __str__(self):
        return f"{self.student.name} - {self.subject}"

# class Attendance(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     date = models.DateField()
#     status = models.CharField(max_length=1, choices=[('P', 'Present'), ('A', 'Absent')])

#     def __str__(self):
#         return f"{self.student.name} - {self.date} - {self.status}" 

class Period(models.Model):
    name = models.CharField(max_length=50)  # e.g., 'Morning', 'Afternoon', etc.
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    


    
def class_details(request, class_id):
    student_class = get_object_or_404(Class, pk=class_id)
    students = Student.objects.filter(student_class=student_class)
    attendance_forms = [Attendance(initial={'student': student}) for student in students]

    if request.method == 'POST':
        # Handle the form submission logic here
        pass

    return render(request, 'class_detail.html', {
        'student_class': student_class,
        'students': students,
        'attendance_forms': attendance_forms,
    })



class Timetable(models.Model):
    day = models.CharField(max_length=50)
    time = models.TimeField()
    subject = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='timetables')

    def __str__(self):
        return f"{self.day} - {self.time} - {self.subject} - {self.teacher}"
    


