from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from django.conf.urls import url, include


urlpatterns = [
    path('register/', views.register, name='register'),
    path('delete_account/',views.delete_account, name='delete_account'),
    path('token/',TokenObtainPairView.as_view()),
    path('token/',TokenVerifyView.as_view()),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),

    path('current_user/', views.currentUser, name='current_user'),
    path('employer/',views.EmployerUser,name='employer'),
    path('employerupdate/',views.updateemployer,name='employerupdate'),


    path('update_user/', views.updateUser, name='update_user'),
    path('change_password/',views.ChangePasswordView.as_view()),
    path('uploadresume/', views.uploadResume, name='uploadresume'),
    path('download_resume/', views.downloadResume, name='downloadresume'),

    path('logout/',views.LogoutView.as_view())

]



