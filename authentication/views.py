from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer, CustomUserCreateSerializer

User = get_user_model()


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile_type(request):
    if request.method == 'GET':
        profiles = Profile.objects.filter(user=request.user)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        data = {
            'user': request.user,
            'profile_type': request.data.get('profile_type')
        }
        print(data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['POST'])
# def custom_register(request):
#     serializer = CustomUserCreateSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         response_data = {
#             'id': user.id,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'email': user.email,
#             'username': user.username,
#         }
#         return Response(response_data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)