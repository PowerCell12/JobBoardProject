from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, View, ListView

from JobPulse.Company.forms import CreatePostForm, SearchForm, EditPostForm, ApplyToPostForm
from JobPulse.Company.models import Posts, Company, JobApplication


def home(request):
    posts = Posts.objects.all()

    form = SearchForm(request.GET)
    if form.is_valid():
        filter_by = form.cleaned_data['search_field']
        try:
            posts = posts.filter(Q(JobName__icontains=filter_by)  | Q(Location__icontains=filter_by) | Q(Seniority__icontains=filter_by) | Q(Salary=int(filter_by)))
        except ValueError as vl:
            posts = posts.filter(Q(JobName__icontains=filter_by)  | Q(Location__icontains=filter_by) | Q(Seniority__icontains=filter_by))


    posts = posts.order_by('-date_created')
    paginated = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginated.get_page(page_number)

    count1 = posts.count()
    context = {
        'user': request.user,
        'posts': page_obj,
        'form': form,
        'search_field': request.GET.get('search_field'),
        'count1': count1
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





class DescriptionPostView(DetailView):
    model = Posts
    template_name = 'Company/description_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['post'] = Posts.objects.get(pk=self.kwargs['pk'])
        return context


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Posts
    form_class  = EditPostForm
    template_name = 'Company/edit_post.html'
    login_url = '/profile/login'

    def get_success_url(self):
        return reverse_lazy('description-post', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['post'] = Posts.objects.get(pk=self.kwargs['pk'])
        return context




@login_required(login_url='/profile/login')
def DeletePost(request, pk):
    post = Posts.objects.get(pk=pk)

    if request.method == "POST":
        action = request.POST.get('action')

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

            subject  = form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name'] + " Applied: " + post.JobName + " - " + post.CompanyFK.Name

            message = [
                f"A job application has been submitted by: {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
                f"- Email: {form.cleaned_data['email']}",
                f"- Position: {post.JobName}",
            ]

            if form.cleaned_data['Message']:
                message.append(f"\nWith the Message:\n{form.cleaned_data['Message']}")

            message = "\n".join(message)


            from_email = form.cleaned_data['email']

            recipient_list = []

            if post.Recruiter == None:
                recipient_list = [post.Moderator.user_profile.user.email]
            else:
                recipient_list = [post.Recruiter.user_profile.user.email]

            email = EmailMessage(subject, message, from_email, recipient_list)
            email.attach("Resume.pdf", form.cleaned_data['Resume'].read(), form.cleaned_data['Resume'].content_type)

            email.send()



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



class DescriptionCompanyView(DetailView):
    model = Company
    template_name = 'Company/description_company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['posts'] = Posts.objects.filter(CompanyFK=self.object)
        context['company'] = Company.objects.get(pk=self.kwargs['pk'])
        return context






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





class download_resume(LoginRequiredMixin, View):
    login_url = '/profile/login/'

    def get(self, request, pk):
        application = JobApplication.objects.get(pk=pk)
        return FileResponse(application.Resume.open(), as_attachment=True, filename='resume.pdf')
