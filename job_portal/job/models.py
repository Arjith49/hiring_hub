from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_type=models.CharField(max_length=100)


class Department(models.Model):
    departmentname=models.CharField(max_length=100)

# class Skill(models.Model):
#     CATEGORY_CHOICES = [
#         ('industry_knowledge', 'Industry Knowledge'),
#         ('tools_technologies', 'Tools & Technologies'),
#         # Add more categories as needed
#     ]

#     skill_name = models.CharField(max_length=100)
#     category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='tools_technologies')

#     def __str__(self):
#         return self.skill_name

class Skill(models.Model):
    sk_name = models.CharField(max_length=100)
    
class Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True)
    location = models.CharField(max_length=100, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)  # Many-to-many relationship

class Company(models.Model):
    Company_id=models.ForeignKey(User,on_delete=models.CASCADE)
    Department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    Company_Name=models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    Details=models.CharField(max_length=1000)
    logo = models.ImageField(upload_to='company_logos/', blank=True)

class Job(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    location = models.CharField(max_length=100)
    posted_at = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()

    

class Application(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ])