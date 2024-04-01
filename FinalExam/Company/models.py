
from django.contrib.auth import get_user_model
from django.db import models

class Company(models.Model):
    Name = models.CharField(max_length=50, unique=True)
    CompanyImage = models.ImageField(upload_to='images/company_pics/', default='default_company_image.png')
    Description = models.CharField(null=True, blank=True)
    Address = models.CharField(max_length=255, null=True, blank=True)
    CompanyEmail = models.EmailField(null=True)
    Owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.Name}'

    class Meta:
        verbose_name_plural = 'Companies'


CHOICES = [
    ('Junior/Intern', 'Junior/Intern'),
    ('Mid-Level', 'Mid-Level'),
    ('Senior', 'Senior'),
    ('Team Lead', 'Team Lead'),
]





class Posts(models.Model):
    JobName = models.CharField(max_length=50)
    Description = models.CharField(null=True, blank=True)
    Salary = models.PositiveIntegerField(null=True, blank=True)
    Location = models.CharField(max_length=60, null=True, blank=True)
    Seniority = models.CharField(choices=CHOICES, null=True, blank=True)
    CompanyFK = models.ForeignKey(to="Company.Company", on_delete=models.CASCADE)
    Recruiter = models.ForeignKey(to="app_auth.Recruiters", on_delete=models.CASCADE, blank=True, null=True)
    Moderator = models.ForeignKey(to='app_auth.Moderators', on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)



class JobApplication(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    JobName = models.CharField(max_length=255)
    Message = models.TextField(blank=True, null=True)
    Resume = models.FileField(upload_to='files/resumes/', blank=True, null=True)
    application_date = models.DateField(auto_now_add=True)
    CompanyFk = models.ForeignKey(to='Company.Company', on_delete=models.CASCADE)
    PostFk = models.ForeignKey(to='Company.Posts', on_delete=models.CASCADE)