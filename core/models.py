from django.db import models
from django.contrib.postgres.fields import ArrayField

class Level(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.name)


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Klass(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey("accounts.UserAccount", on_delete=models.CASCADE)

    level = models.ForeignKey("core.Level", on_delete=models.CASCADE)

    def add_grade_column(self):
        students_list = Student.objects.filter(klass=self)
        for student in students_list:
            student.grades.append(0)
            student.save()
            print(student.grades)

    def remove_grade_column(self, index):
        students_list = Student.objects.filter(klass=self)
        for student in students_list:
            student.grades.pop(index)
            student.save()
            print(student.grades)

    def __str__(self) -> str:
        return f"{self.name} | {self.user}"
    

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    grades = ArrayField(models.FloatField(), blank=True, default=list)
    
    klass = models.ForeignKey("core.Klass", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.klass.name} ==> {self.first_name} {self.last_name}"

class Faq(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
