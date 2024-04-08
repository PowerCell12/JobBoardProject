from django.contrib import admin
from django.core.exceptions import ValidationError

from FinalExam.Company.forms import CompanyForm
from FinalExam.Company.models import Company, Posts, JobApplication


# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Address','CompanyEmail','Owner']
    fields = ['Name', 'CompanyImage', 'Address', 'Description','CompanyEmail']
    form = CompanyForm
    search_fields = ['Name', 'Address', 'CompanyEmail']
    list_filter = ['Owner', 'Address']
    date_hierarchy = 'date_created'



    def save_model(self, request, obj, form, change):

        if not change and not obj.Owner:
            obj.Owner = request.user

        super().save_model(request, obj, form, change)


    def delete_model(self, request, obj):

        if request.user != obj.Owner:
           error_message = "You do not have permission to delete this company."
           raise ValidationError(error_message)

        super().delete_model(request, obj)




@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ['JobName', 'Description', 'Salary']
    search_fields = ['JobName']
    list_filter = ['Seniority', 'Salary', 'CompanyFK__Name']
    date_hierarchy = 'date_created'
