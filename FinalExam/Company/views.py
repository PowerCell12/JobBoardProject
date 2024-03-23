from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import render, redirect
from FinalExam.Company.forms import CreatePostForm, SearchForm, EditPostForm, ApplyToPostForm
from FinalExam.Company.models import Posts, Company, JobApplication


def home(request):
    posts = Posts.objects.all()

    form = SearchForm(request.GET)
    if form.is_valid():
        filter_by = form.cleaned_data['search_field']
        posts = posts.filter(JobName__icontains=filter_by)

    posts = posts.order_by('-date_created')
    paginated = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginated.get_page(page_number)

    context = {
        'user': request.user,
        'posts': page_obj,
        'form': form,
        'search_field': request.GET.get('search_field')
    }
    return render(request, 'home.html', context)


@login_required(login_url='/profile/login')
def CreatePost(request):
    form = CreatePostForm()

    if request.method == 'POST':
        form = CreatePostForm(request.POST)

        if form.is_valid():

            if request.user.email == '':
                    raise ValidationError("Set up your email address so that you can create posts")


            post = form.save(commit=False)

            if request.user.is_superuser:
                post.Moderator = request.user.userprofile.moderators
            else:
                post.Recruiter = request.user.userprofile.recruiters

            post.save()

            return redirect('home')

    context = {
        'user': request.user,
        'form': form
    }

    return render(request, 'Company/create_post.html', context)




def DescriptionPost(request, pk):
    post = Posts.objects.get(pk=pk)

    something = request.user.id

    context = {
        'post': post,
        'user': request.user
    }

    return render(request, 'Company/description_post.html', context)


@login_required(login_url='/profile/login')
def EditPost(request, pk):
    post = Posts.objects.get(pk=pk)

    form = EditPostForm(instance=post)

    if request.method == 'POST':
        form = EditPostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('description-post', pk=pk)

    context = {
        'user': request.user,
        'post': post,
        'form': form
    }

    return render(request, 'Company/edit_post.html', context)


@login_required(login_url='/profile/login')
def DeletePost(request, pk):
    post = Posts.objects.get(pk=pk)

    if request.method == "POST":
        action = request.POST.get('acton')

        if action == 'Cancel':
            return redirect('description-post', pk=pk)

        post.delete()
        return redirect('home')

    context = {
        'user': request.user,
        'post': post
    }

    return render(request, 'Company/delete_post.html', context)


@login_required(login_url='/profile/login')
def ApplyToPost(request, pk):
    post = Posts.objects.get(pk=pk)
    form = ApplyToPostForm(instance=request.user)

    if request.method == "POST":
        form = ApplyToPostForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():

            if post.Recruiter != None: ## recruiter
                subject  = "A job application for " + post.JobName
                message ="A job application from " + form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name'] + " has been made for the post: " + post.JobName + "with the message:" +  form.cleaned_data['Message']
                from_email = form.cleaned_data['email']
                recipient_list = [post.Recruiter.user_profile.user.email]
                send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)



            elif post.Moderator != None: ## moderator
                subject  = "A job application for " + post.JobName
                message ="A job application from " + form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name'] + " has been made for the post: " + post.JobName + " with the message:" +  form.cleaned_data['Message']
                from_email = form.cleaned_data['email']
                recipient_list = [post.Moderator.user_profile.user.email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)


            form.save()

            JobApplication.objects.create(
                user = request.user,
                JobName = post.JobName,
                CompanyFk = post.CompanyFK,
                PostFk = post,
                Message = form.cleaned_data['Message'],
                Resume = form.cleaned_data['Resume']
            )

            return redirect('home')

    context = {
        'user': request.user,
        'post': post,
        'form': form
    }

    return render(request, 'Company/apply_to_post.html', context)



def DescriptionCompany(request, pk):
    company = Company.objects.get(pk=pk)
    related_posts = company.posts_set.all()

    context = {
        'company': company,
        'user': request.user,
        'posts': related_posts
    }

    return render(request, 'Company/description_company.html', context)




@login_required(login_url='/profile/login')
def RelatedJobs(request, pk):
    related_posts = Posts.objects.all()

    if request.user.is_superuser:
        related_posts = request.user.userprofile.moderators.posts_set.all()
    else:
       related_posts = request.user.userprofile.recruiters.posts_set.all()


    context = {
        'user': request.user,
        'posts': related_posts
    }

    return render(request, 'Company/view_related_jobs.html', context)


@login_required(login_url='/profile/login')
def JobApplicationView(request, pk):
    related_applications = JobApplication.objects.filter(user_id=request.user.id)



    context = {
        'user': request.user,
        'applications': related_applications
    }

    return render(request, 'Company/job_application.html', context)



@login_required(login_url='/profile/login')
def download_resume(request, pk):
    application = JobApplication.objects.get(pk=pk)
    return FileResponse(application.Resume.open(), as_attachment=True, filename='resume.pdf')
