from django.urls import path

from FinalExam.Company.views import CreatePost, DescriptionPost, EditPost, DeletePost, ApplyToPost, DescriptionCompany, \
    RelatedJobs, JobApplicationView

urlpatterns = [
    path('create_post/', CreatePost, name='create-post'),
    path('<int:pk>/description_post/',  DescriptionPost, name='description-post'),
    path('<int:pk>/edit_post/',  EditPost, name='edit-post'),
    path('<int:pk>/delete_post/',  DeletePost, name='delete-post'),
    path('<int:pk>/apply/',  ApplyToPost, name='apply-to-post'),
    path('<int:pk>/description_company/',  DescriptionCompany, name='description-company'),
    path('<int:pk>/view-related-jobs/', RelatedJobs, name='view-related-jobs'),
    path('<int:pk>/job-application/', JobApplicationView, name='job-application'),
]
