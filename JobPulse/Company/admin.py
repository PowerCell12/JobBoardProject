from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.utils.safestring import mark_safe

from JobPulse.Company.forms import CompanyForm, PostsForm
from JobPulse.Company.models import Company, Posts, JobApplication
from django.db import models

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

        if change and request.user != obj.Owner:
            error_message = "You do not have permission to edit this company."
            raise ValidationError(error_message)

        super().save_model(request, obj, form, change)


    def delete_model(self, request, obj):

        if request.user != obj.Owner:
           error_message = "You do not have permission to delete this company."
           raise ValidationError(error_message)

        super().delete_model(request, obj)


    def show_description(self, obj):
        if obj.Description:
            return mark_safe(f'<div class="admin_description">{obj.Description}</div>')
        else:
            return "-"


    def get_fieldsets(self, request, obj=None):

        if not obj:
            fieldsets = (
                (None, {'fields': ('Name', 'CompanyImage', 'Description', 'Address', 'CompanyEmail')}),
            )

            return fieldsets


        if request.user.is_superuser:
            fieldsets = (
                (None, {'fields': ('Name', 'CompanyImage', mark_safe('Description'), 'Address', 'CompanyEmail')}),
            )
        else:
            fieldsets = (
                (None, {'fields': ('Name', 'CompanyImage', 'show_description', 'Address', 'CompanyEmail')}),
            )



        return fieldsets

    show_description.short_description = 'Description'



    class Media:
        css = {
            'all': ('admin_custom.css',),
        }


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ['JobName', 'Salary', 'Location']
    search_fields = ['JobName']
    list_filter = ['Seniority', 'Salary', 'CompanyFK__Name']
    date_hierarchy = 'date_created'
    form = PostsForm


    def show_description(self, obj):
        if obj.Description:
            return mark_safe(f'<div class="admin_description">{obj.Description}</div>')
        else:
            return "-"





    def get_fieldsets(self, request, obj=None):

      if not obj:
        fieldsets = (
           (None, {'fields': ('JobName', 'Description', 'Salary', 'Location', 'Seniority', 'CompanyFK', 'Recruiter', 'Moderator')}),
        )

        return fieldsets

      if request.user.is_superuser:
        fieldsets = (
               (None, {'fields': ('JobName', mark_safe('Description'), 'Salary', 'Location', 'Seniority', 'CompanyFK', 'Recruiter', 'Moderator')}),
          )

      else:
          if obj.Recruiter:
            fieldsets = (
               (None, {'fields': ('JobName', 'show_description', 'Salary', 'Location', 'Seniority', 'CompanyFK', 'Recruiter')}),
          )
          else:
            fieldsets = (
               (None, {'fields': ('JobName', 'show_description', 'Salary', 'Location', 'Seniority', 'CompanyFK', 'Moderator')}),
              )


      return fieldsets

    show_description.short_description = 'Description'




    class Media:
        css = {
            'all': ('admin_custom.css',),
        }