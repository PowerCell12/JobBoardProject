from django.contrib import admin
from django.core.exceptions import ValidationError

from FinalExam.Company.forms import CompanyForm
from FinalExam.Company.models import Company
# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Address','CompanyEmail','Owner']
    fields = ['Name', 'CompanyImage', 'Address', 'Description','CompanyEmail']
    form = CompanyForm

    def save_model(self, request, obj, form, change):

        if not change and not obj.Owner:
            obj.Owner = request.user

        super().save_model(request, obj, form, change)


    def delete_model(self, request, obj):

        if request.user != obj.Owner:
           error_message = "You do not have permission to delete this company."
           raise ValidationError(error_message)

        super().delete_model(request, obj)
