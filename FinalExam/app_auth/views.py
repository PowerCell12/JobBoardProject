from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from FinalExam.app_auth.forms import SignUpUserForm, SignUpRecruiterForm, EditUserForm, EditModeratorForm, \
    EditUserProfileForm
from FinalExam.app_auth.models import UserProfile, Recruiters, Moderators

# Create your views
User = get_user_model()


def SignUpView(request):

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == "recruiter":
            return redirect(reverse('signup-recruiter'))
        elif action == 'user':
            return redirect(reverse('signup-user'))

    return render(request, 'app_auth/signup.html')




def SignUpUser(request):


    form = SignUpUserForm()

    if request.method == "POST":
        form = SignUpUserForm(request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password1')

            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user)

            login(request, user)

            return redirect(reverse('home'))

    context = {
        'form': form
    }

    return render(request, 'app_auth/signup_user.html', context)


def SignUpRecruiter(request):
    form = SignUpRecruiterForm()

    if request.method == 'POST':
        form = SignUpRecruiterForm(request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password1')

            selected_companies = form.cleaned_data['companies']
            company = [company for company in selected_companies]

            user = User.objects.create_user(username=username, password=password, is_staff=True)
            user_profile = UserProfile.objects.create(user=user)
            recruiter = Recruiters.objects.create(user_profile=user_profile)
            recruiter.companies.set(company)

            login(request, user)

            return redirect(reverse('home'))

    context = {
        'form': form
    }


    return render(request, 'app_auth/signup_recruiter.html', context)


@login_required(login_url='/profile/login')
def LogOutView(request, pk):

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'Cancel':
            return redirect(reverse('home'))
        elif action == "LogOut":
            logout(request)
            return redirect(reverse('home'))




    context = {
        'user': request.user
    }

    return render(request, 'app_auth/logout_profile.html', context)




@login_required(login_url='/profile/login') ## fix profile picture
def profile_description(request, pk):

    form = EditUserProfileForm()

    if request.method == "POST":
        if request.user.is_staff == False:
            form = EditUserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        elif request.user.is_superuser:
            form = EditUserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        else:
            form = EditUserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)


        if form.is_valid():
            form.save()
            return redirect(reverse('description-profile', kwargs={'pk': pk}))

    context = {
        'user': request.user,
        'form': form
    }


    return render(request, 'app_auth/description_profile.html', context)




@login_required(login_url='/profile/login')
def profile_edit(request, pk):
    formUser = EditUserForm(instance=request.user)
    context = {
        'form': formUser,
        'user': request.user
    }

    if request.user.is_superuser is True:

        UserModerator = EditModeratorForm(instance=request.user.userprofile.moderators)

        context1 = {
            'UserModerator': UserModerator
        }

        context = {**context, **context1}

        if request.method == "POST":
            formUser = EditUserForm(request.POST, instance=request.user)
            UserModerator = EditModeratorForm(request.POST, instance=request.user.userprofile.moderators)

            if formUser.is_valid() and UserModerator.is_valid():
                formUser.save()
                UserModerator.save()

                return redirect(reverse('description-profile', kwargs={'pk': pk}))

    else:

        if request.method == "POST":
            formUser = EditUserForm(request.POST, instance=request.user)

            if formUser.is_valid():
                formUser.save()

                return redirect(reverse('description-profile', kwargs={'pk': pk}))

    return render(request, 'app_auth/edit-profile.html', context)




class profile_delete(LoginRequiredMixin, View):
    login_url = '/profile/login'

    def get(self, request, pk):
        context ={
            'user': request.user
        }
        return render(request, 'app_auth/delete_profile.html', context)

    def post(self, request, pk):
        action = request.POST.get('action')

        if action == 'Cancel':
            return redirect(reverse('description-profile', kwargs={'pk': pk}))
        elif action == "Delete":
            request.user.userprofile.user.delete()
            logout(request)
            return redirect(reverse('home'))