from rest_framework import status
from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# from .models import Profile
from .serializers import CustomUserCreateSerializer
# from djoser.views import UserCreateView

User = get_user_model()


# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def profile_type(request):
#     if request.method == 'GET':
#         profiles = Profile.objects.filter(user=request.user)
#         serializer = ProfileSerializer(profiles, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ProfileSerializer(data=request.data)
#         data = {
#             'user': request.user,
#             'profile_type': request.data.get('profile_type')
#         }
#         print(data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomUserCreateView(APIView):
    def post(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')

        try:
            user = User.objects.get(email=email, verification_code=verification_code)
            user.is_active = True
            user.verification_code = None  # Clear the verification code
            user.save()
            return Response({"detail": "Account successfully verified."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)



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