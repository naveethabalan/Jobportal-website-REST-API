from .models import EmployerProfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, EmployeeSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import SignUpSerializer, UserSerializer,EmployeeSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import User

from .utils import send_activation_email,send_reset_password_email

from rest_framework import status

from .validators import validate_file_extension
from django.http import HttpResponse, FileResponse
from django.conf import settings
import os
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import UserProfile
from .validators import validate_file_extension

# Create your views here.

@api_view(['POST'])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                username=data['email'],
                email=data['email'],
                password=make_password(data['password'])
            )

            send_activation_email(user.email)  # Corrected indentation here

            return Response({
                'message': 'User registered.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response({
                'error': 'User already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

    else:
        return Response(user.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # Ensures that only authenticated users can delete their account
def delete_account(request):
    user = request.user  # Get the authenticated user

    if user.is_authenticated:
        # Delete the user account
        user.delete()

        return Response({'message': 'User account deleted successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Authentication required to delete the account'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def currentUser(request):

    user = UserSerializer(request.user)

    return Response(user.data)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        user = request.user

        if not user.check_password(password):
            return Response({'detail': 'Invalid old password.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request):
    user = request.user


    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.username = data['email']
    user.email = data['email']

    if 'password' in data and data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)




# Import your file validation utility

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def uploadResume(request):
    user = request.user

    try:
        resume = request.FILES['resume']
    except KeyError:
        return Response({'error': 'Please provide a resume file in the request.'}, status=status.HTTP_400_BAD_REQUEST)

    if not resume:
        return Response({'error': 'Please upload your resume.'}, status=status.HTTP_400_BAD_REQUEST)

    if not validate_file_extension(resume.name):
        return Response({'error': 'Please upload only PDF files.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(user, many=False)

    try:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.resume = resume
        user_profile.save()
    except Exception as e:
        return Response({'error': f'Error saving the resume: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def downloadResume(request, filename):
    user = request.user

    try:
        user_profile = user.userprofile
        resume_path = user_profile.resume.path
    except UserProfile.DoesNotExist:
        return Response({'error': 'Resume not found for the user.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Error fetching the resume: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Set the appropriate content type for PDF files
    content_type = 'application/pdf'

    # Open the file in binary mode
    with open(resume_path, 'rb') as resume_file:
        response = HttpResponse(resume_file.read(), content_type=content_type)

    # Set the Content-Disposition header for the response
    response['Content-Disposition'] = f'attachment; filename={filename}'

    return response

class LogoutView(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            "Logout":"Success....!"
        }
        return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def EmployerUser(request):

    user = EmployeeSerializer(request.user)

    return Response(user.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateemployer(request):
    user = request.user
    data = request.data

    # Update fields on the User model
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.username = data.get('email', user.username)
    user.email = data.get('email', user.email)

    # Check if the user has an associated employer profile
    if hasattr(user, 'employerprofile'):
        employer_profile = user.employerprofile
    else:
        # If the user doesn't have an associated employer profile, create one
        employer_profile = EmployerProfile(user=user)

    # Update fields on the EmployerProfile
    employer_profile.company_name = data.get('company_name', employer_profile.company_name)
    employer_profile.services = data.get('services', employer_profile.services)
    employer_profile.employees = data.get('employees', employer_profile.employees)
    employer_profile.website = data.get('website', employer_profile.website)



    employer_profile.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

