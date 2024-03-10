from django.conf.urls import url
from django.urls import path
from .views import TopicStatsAPI


from Backend import views


urlpatterns=[
    url(r'^Job/$',views.JobAPI),


    url(r'^Jobid/([0-9]+)/$',views.JobIDAPI),
    path('topic-stats/<str:topic>/', TopicStatsAPI, name='topic-stats-api'),
    path('topic-stats/<str:topic>/', TopicStatsAPI, name='topic-stats-api'),
    path('Job/<int:pk>/apply/',views.applyToJob, name='apply_to_job'),
    path('Job/applied/', views.getCurrentUserAppliedJobs, name='current_user_applied_jobs'),
    path('Job/<str:pk>/checkapply/', views.isApplied, name='is_applied_to_job'),
    path('Job/currentuser/',views.getCurrentUserJobs, name='current_user_jobs'),
    path('Job/<str:pk>/candidates/', views.getCandidatesApplied, name='get_candidates_applied'),






]