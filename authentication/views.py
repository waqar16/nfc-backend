from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import CustomUserCreateSerializer


User = get_user_model()

    
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