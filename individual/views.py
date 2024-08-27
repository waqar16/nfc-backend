from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import UserProfile, Receivedprofile
from company.models import Company
from .serializers import UserProfileSerializer, ShareProfileSerializer, ReceivedprofileSerializer
from .utils import encrypt_data, decrypt_data
from django.contrib.auth import get_user_model
from company.serializers import CompanySerializer
from django.core.mail import send_mail
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
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

        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
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
def user_profile_detail(request, pk):
    try:
        profile = UserProfile.objects.get(user=pk)
    except UserProfile.DoesNotExist:
        # If UserProfile does not exist, try to fetch from Company model
        try:
            company = Company.objects.get(user=pk)
            # Serialize the Company data
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        except Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Ensure only the owner can update or delete
    if request.method in ['PUT', 'DELETE'] and profile.user != request.user:
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
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
        profile_url = f'https://app.onesec.shop/profile/{user.id}'
    elif profile_type == 'company':
        try:
            profile = Company.objects.get(user=user)
        except Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        profile_url = f'https://letsconnect.onesec.shop/company/{user.id}'
    else:
        return Response({'detail': 'Invalid profile type.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'profile_url': profile_url}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nfc_write(request):
    try:
        profile_data = request.data
        if not profile_data:
            return Response({'error': 'Profile data is required'}, status=status.HTTP_400_BAD_REQUEST)

        encrypted_data = encrypt_data(profile_data)
        print("Encrypted Data:", encrypted_data)
        print("Decrypted Data:", decrypt_data(encrypted_data))
        return Response({'encrypted_data': encrypted_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nfc_read(request):
    try:
        encrypted_data = request.data.get('encrypted_data')
        print("Received Encrypted Data:", encrypted_data)
        if not encrypted_data:
            return Response({'error': 'Encrypted text is required'}, status=status.HTTP_400_BAD_REQUEST)

        decrypted_data = decrypt_data(encrypted_data)
        print("Decrypted Data:", decrypted_data)
        return Response(decrypted_data, status=status.HTTP_200_OK)
    except Exception as e:
        print("Error:", str(e))
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

User = get_user_model()

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def share_profile(request):
    user = request.user
    
    if request.method == 'POST':
        shared_to_email = request.data.get('shared_to')
        
        try:
            shared_to_user = User.objects.get(email=shared_to_email)
        except User.DoesNotExist:
            # Send email with profile URL
            if user.profile_type == 'company':
                profile_url = f'https://letsconnect.onesec.shop/company/{user.id}'
                sender_name = user.username
            else:
                profile_url = f'https://letsconnect.onesec.shop/profile/{user.id}'
                sender_name = f"{user.first_name} {user.last_name}"
            
            subject = 'Profile Shared with You'
            message = f'Hi there,\n\n{sender_name} has shared their profile with you. You can view the profile at the following URL:\n\n{profile_url}\n\nBest regards,\nOneSec Team'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [shared_to_email]
            
            send_mail(subject, message, from_email, recipient_list)
            
            return Response({'message': 'User does not exist, but email sent successfully'}, status=status.HTTP_200_OK)
        
        # Create ShareProfile entry
        share_profile_data = {
            'user': user.id,
            'shared_to': shared_to_user.id
        }

        if user.profile_type == 'company':
            profile_url = f'https://letsconnect.onesec.shop/company/{user.id}'
            sent_to = shared_to_user.username
            sender_name = user.username
        else:
            profile_url = f'https://letsconnect.onesec.shop/profile/{user.id}'
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

        else:
            user_profile = UserProfile.objects.get(user=user)

        received_profile_data = {
            'user': shared_to_user.id,
            'shared_from': user.id,
            'shared_from_email': user_profile.email,
            'profile_type_who_shared': user.profile_type
        }
        received_profile_serializer = ReceivedprofileSerializer(data=received_profile_data)
        if received_profile_serializer.is_valid():
            received_profile_serializer.save()
        else:
            return Response(received_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Send email with profile URL
        subject = 'Profile Shared with You'
        message = f'Hi {sent_to},\n\n{sender_name} has shared their profile with you. You can view the profile at the following URL:\n\n{profile_url}\n\nBest regards,\nOneSec Team'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [shared_to_email]
        
        send_mail(subject, message, from_email, recipient_list)

        return Response({'message': 'Profile shared successfully and email sent'}, status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':
        try:
            received_profiles = Receivedprofile.objects.filter(user=request.user)
            paginator = StandardResultsSetPagination()
            result_page = paginator.paginate_queryset(received_profiles, request)
            serializer = ReceivedprofileSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            print("Error fetching received cards:", str(e))
            return Response({"error": "Error fetching received cards"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
