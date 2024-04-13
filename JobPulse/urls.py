from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

from JobPulse.Company.models import Company
from JobPulse.Company.views import home

def about_us(request):

    context = {
        'user': request.user
    }

    return render(request,  'about_us.html', context)


def companies(request):

    companies = Company.objects.all().order_by('-date_created')

    context = {
        'companies': companies,
        'user': request.user
    }

    return render(request, 'companies.html', context)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', home, name='home'),
    path('profile/', include('JobPulse.app_auth.urls')),
    path('company/', include('JobPulse.Company.urls')),
    path('about_us/', about_us, name='about-us'),
    path('companies/', companies, name='companies'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
