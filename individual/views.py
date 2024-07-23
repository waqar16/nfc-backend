from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import UserProfile, Receivedprofile
from .serializers import UserProfileSerializer, ShareProfileSerializer, ReceivedprofileSerializer
from .utils import encrypt_data, decrypt_data
from django.contrib.auth import get_user_model

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
@permission_classes([IsAuthenticatedOrReadOnly])  # Only authenticated users can modify
def user_profile_detail(request, pk):
    try:
        profile = UserProfile.objects.get(user=pk)
    except UserProfile.DoesNotExist:
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_profile_url(request):
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Construct the URL to be shared
    profile_url = f'http://localhost:3000/profile/{user.id}'
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
    


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def share_profile(request):
    user = request.user
    
    if request.method == 'POST':
        shared_to_email = request.data.get('shared_to')

        try:
            shared_to_user = User.objects.get(email=shared_to_email)
        except User.DoesNotExist:
            return Response({'error': 'User to share with does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Create ShareProfile entry
        share_profile_data = {
            'user': user.id,
            'shared_to': shared_to_user.id
        }
        print(share_profile_data)
        share_profile_serializer = ShareProfileSerializer(data=share_profile_data)
        if share_profile_serializer.is_valid():
            share_profile_serializer.save()
        else:
            return Response(share_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create Receivedprofile entry
        received_profile_data = {
            'user': shared_to_user.id,
            'shared_from': user.id
        }
        print(received_profile_data)
        received_profile_serializer = ReceivedprofileSerializer(data=received_profile_data)
        if received_profile_serializer.is_valid():
            received_profile_serializer.save()
        else:
            return Response(received_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Profile shared successfully'}, status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':
        user = request.user
        try:   
            received_profiles = Receivedprofile.objects.filter(user=user)
            serializer = ReceivedprofileSerializer(received_profiles, many=True)
            print("Serializer data:", serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error fetching received cards:", str(e))  # Debugging line
            return Response({"error": "Error fetching received cards"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)