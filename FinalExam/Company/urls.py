from django.urls import path


# DescriptionPost

from FinalExam.Company.views import CreatePost, DescriptionPostView, EditPostView, DeletePost, ApplyToPost, DescriptionCompanyView, \
    RelatedJobs, JobApplicationView, download_resume

urlpatterns = [
    path('create_post/', CreatePost, name='create-post'),
    path('<int:pk>/description_post/',  DescriptionPostView.as_view(), name='description-post'),
    path('<int:pk>/edit_post/',  EditPostView.as_view(), name='edit-post'),
    path('<int:pk>/delete_post/',  DeletePost, name='delete-post'),
    path('<int:pk>/apply/',  ApplyToPost, name='apply-to-post'),
    path('<int:pk>/description_company/',  DescriptionCompanyView.as_view(), name='description-company'),
    path('<int:pk>/view-related-jobs/', RelatedJobs, name='view-related-jobs'),
    path('<int:pk>/job-application/', JobApplicationView, name='job-application'),
    path('<int:pk>/download-resume/', download_resume.as_view(), name='download-resume'),
]
