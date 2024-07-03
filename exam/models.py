from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ExamType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EducationalLevel(models.Model):
    level = models.CharField(max_length=100)

    def __str__(self):
        return self.level

class Exam(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    syllabus = models.TextField()
    exam_pattern = models.TextField()
    eligibility_criteria = models.TextField()
    registration_procedure = models.TextField()
    important_dates = models.TextField()
    exam_centres = models.TextField()
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    educational_level = models.ForeignKey(EducationalLevel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PreparationResource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=100, choices=[('Book', 'Book'), ('Online Course', 'Online Course'), ('Sample Paper', 'Sample Paper'), ('Preparation Tip', 'Preparation Tip')])
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bookmarked_exams = models.ManyToManyField(Exam, related_name='bookmarked_by')

    def __str__(self):
        return self.user.username

class UserExamRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exam.name}"

class UserDashboard(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    registered_exams = models.ManyToManyField(UserExamRegistration, related_name='registered_exams')
    recommended_exams = models.ManyToManyField(Exam, related_name='recommended_to')

    def __str__(self):
        return f"{self.user.user.username}'s Dashboard"