from django.http import JsonResponse
import requests
from nfc_backend.settings import EMAIL_HOST_USER
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import UserProfile, Receivedprofile
from company.models import Company
from company.models import Employee
from company.serializers import EmployeeSerializer
from rest_framework.authtoken.models import Token
from .serializers import UserProfileSerializer, ShareProfileSerializer, ReceivedprofileSerializer
# from .utils import encrypt_data, decrypt_data
from django.contrib.auth import get_user_model
from company.serializers import CompanySerializer
from django.core.mail import send_mail
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


User = get_user_model()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_profile_list(request):
    if request.method == 'GET':
        if request.user.is_superuser:
            profiles = UserProfile.objects.all()  # Super admin can access all profiles
        else:
            profiles = UserProfile.objects.filter(user=request.user)  # Other users can only access their own profile
        
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)

        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            user = request.user
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def user_profile_detail(request, username):
    try:
        profile = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        # If UserProfile does not exist, try to fetch from Company model
        try:
            company = Company.objects.get(username=username)
            # Serialize the Company data
            serializer = CompanySerializer(company)
            return Response(serializer.data)
    
        except Company.DoesNotExist:
            # If neither UserProfile nor Company found, try fetching from Employee
            try:
                employee = Employee.objects.get(username=username)
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Employee.DoesNotExist:
                # Return 404 if no record found in any of the models
                return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    # Ensure only the owner can update or delete
    if request.method in ['PUT', 'DELETE'] and profile.user != request.user:
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(profile, data=request.data)
        
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        if serializer.is_valid():
            serializer.save()
            user = request.user
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.save()
    
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_profile_url(request):
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    profile_type = user.profile_type  # Assume 'profile_type' is a field in the user model

    if profile_type == 'individual':
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        profile_url = f'https://letsconnect.onesec.shop/profile/{user.username}'
    
    elif profile_type == 'employee':
        try:
            profile = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        profile_url = f'https://letsconnect.onesec.shop/profile/{user.username}'
    
    elif profile_type == 'company':
        try:
            profile = Company.objects.get(user=user)
        except Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        profile_url = f'https://letsconnect.onesec.shop/company/{user.username}'
    else:
        return Response({'detail': 'Invalid profile type.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'profile_url': profile_url}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def nfc_write(request):
#     try:
#         profile_data = request.data
#         if not profile_data:
#             return Response({'error': 'Profile data is required'}, status=status.HTTP_400_BAD_REQUEST)

#         encrypted_data = encrypt_data(profile_data)
#         print("Encrypted Data:", encrypted_data)
#         print("Decrypted Data:", decrypt_data(encrypted_data))
#         return Response({'encrypted_data': encrypted_data}, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def nfc_read(request):
#     try:
#         encrypted_data = request.data.get('encrypted_data')
#         print("Received Encrypted Data:", encrypted_data)
#         if not encrypted_data:
#             return Response({'error': 'Encrypted text is required'}, status=status.HTTP_400_BAD_REQUEST)

#         decrypted_data = decrypt_data(encrypted_data)
#         print("Decrypted Data:", decrypted_data)
#         return Response(decrypted_data, status=status.HTTP_200_OK)
#     except Exception as e:
#         print("Error:", str(e))
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# User = get_user_model()

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def share_profile(request):
    user = request.user
    
    if request.method == 'POST':
        shared_to_email = request.data.get('shared_to')
        
        try:
            shared_to_user = User.objects.get(email=shared_to_email)
        except User.DoesNotExist:

            try:
                # Send email with profile URL
                if user.profile_type == 'company':
                    profile_url = f'https://letsconnect.onesec.shop/company/{user.username}'
                    sender_name = user.username
                elif user.profile_type == 'employee':
                    profile_url = f'https://letsconnect.onesec.shop/profile/{user.username}'
                    sender_name = f"{user.first_name} {user.last_name}"
                else:
                    profile_url = f'https://letsconnect.onesec.shop/profile/{user.username}'
                    sender_name = f"{user.first_name} {user.last_name}"
                
                subject = 'Profile Shared with You'
                message = f'Hi there,\n\n{sender_name} has shared their profile with you. You can view the profile at the following URL:\n\n{profile_url}\n\nBest regards,\nOneSec Team'
                from_email = EMAIL_HOST_USER
                recipient_list = [shared_to_email]
                
                send_mail(subject, message, from_email, recipient_list)
                
                return Response({'message': 'User does not exist, but email sent successfully'}, status=status.HTTP_200_OK)
        
            except Exception as e:
                # Log the error for debugging purposes
                print("Error sending email:", str(e))
                # Return a user-friendly message
                return Response({'message': 'User does not exist, but email could not be sent'}, status=status.HTTP_200_OK)
    
        # Create ShareProfile entry
        share_profile_data = {
            'user': user.id,
            'shared_to': shared_to_user.id
        }

        if user.profile_type == 'company':
            profile_url = f'https://letsconnect.onesec.shop/company/{user.username}'
            sent_to = shared_to_user.username
            sender_name = user.username
        elif user.profile_type == 'employee':
            profile_url = f'https://letsconnect.onesec.shop/profile/{user.username}'
            sent_to = f"{shared_to_user.first_name} {shared_to_user.last_name}"
            sender_name = f"{user.first_name} {user.last_name}"
        else:
            profile_url = f'https://letsconnect.onesec.shop/profile/{user.username}'
            sent_to = f"{shared_to_user.first_name} {shared_to_user.last_name}"
            sender_name = f"{user.first_name} {user.last_name}"
        
        share_profile_serializer = ShareProfileSerializer(data=share_profile_data)
        if share_profile_serializer.is_valid():
            share_profile_serializer.save()
        else:
            return Response(share_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create Receivedprofile entry
        if user.profile_type == 'company':
            user_profile = Company.objects.get(user=user)

        elif user.profile_type == 'employee':
            user_profile = Employee.objects.get(user=user)

        else:
            user_profile = UserProfile.objects.get(user=user)

        received_profile_data = {
            'user': shared_to_user.id,
            'shared_from': user.id,
            'shared_from_email': user_profile.email,
            'shared_from_username': user_profile.username,
            'profile_type_who_shared': user.profile_type,
        }
        received_profile_serializer = ReceivedprofileSerializer(data=received_profile_data)
        if received_profile_serializer.is_valid():
            received_profile_serializer.save()
        else:
            return Response(received_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Send email with profile URL
        subject = 'Profile Shared with You'
        message = f'Hi {sent_to},\n\n{sender_name} has shared their profile with you. You can view the profile at the following URL:\n\n{profile_url}\n\nBest regards,\nOneSec Team'
        from_email = EMAIL_HOST_USER
        recipient_list = [shared_to_email]
        
        send_mail(subject, message, from_email, recipient_list)

        return Response({'message': 'Profile shared successfully and email sent'}, status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':
        try:
            received_profiles = Receivedprofile.objects.filter(user=request.user).order_by('-shared_at')
            paginator = StandardResultsSetPagination()
            result_page = paginator.paginate_queryset(received_profiles, request)
            serializer = ReceivedprofileSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            print("Error fetching received cards:", str(e))
            return Response({"error": "Error fetching received cards"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

       
@api_view(['POST'])
def share_back_profile(request):
    access_token = request.data.get('access_token')
    profile_type = request.data.get('profile_type')

    if not access_token:
        return Response({'error': 'No access token provided'}, status=status.HTTP_400_BAD_REQUEST)

    if profile_type not in ['individual', 'employee', 'company']:
        return Response({'error': 'Invalid profile type'}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch user info from Google
    google_user_info = requests.get(
        'https://www.googleapis.com/oauth2/v3/userinfo',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    if google_user_info.status_code == 200:
        google_user_info = google_user_info.json()
        email = google_user_info.get('email')
        name = google_user_info.get('name')
        first_name, last_name = name.split(' ', 1) if ' ' in name else (name, '')
        picture = google_user_info.get('picture')
        username = email.split('@')[0] if email else None

        if not email:
            return Response({'error': 'Failed to retrieve email from token'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user exists by email
        user = User.objects.filter(email=email).first()

        if user:
            if user.has_usable_password():
                return Response({'error': "Your account does not use Google Sign-in. Don't worry login with email and password"}, status=status.HTTP_400_BAD_REQUEST)
            # else:
            #     # Update user profile_type if needed
            #     if user.profile_type != profile_type:
            #         user.profile_type = profile_type
            #         user.save()
        else:
            # Create a new user if none exists
            user = User.objects.create(
                username=username,  # or use some other unique identifier for the username
                email=email,
                first_name=first_name,
                last_name=last_name,
                profile_type=profile_type,
                authentication_type='google'
            )
            user.set_unusable_password()
            user.save()
            
            user_profile = UserProfile.objects.create(user=user, profile_pic=picture, first_name=first_name, last_name=last_name, email=email, username=username)
            user_profile.save()

        # Generate or retrieve auth token
        token, created = Token.objects.get_or_create(user=user)

        return JsonResponse({
            'message': 'Login successful',  
            'user_id': user.id,
            'username': user.username,
            'auth_token': token.key,
            'profile_type': user.profile_type,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_pic': picture,
            'authentication_type': user.authentication_type
        })

    else:
        return Response({'error': 'Google login failed'}, status=status.HTTP_400_BAD_REQUEST)