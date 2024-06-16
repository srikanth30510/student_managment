from django.db import models

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
    
class Timetable(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    subject = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day} - {self.subject} - {self.start_time} - {self.end_time}"
    
class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    mark = models.IntegerField()

    def __str__(self):
        return f"{self.student.name} - {self.subject}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=[('P', 'Present'), ('A', 'Absent')])

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
