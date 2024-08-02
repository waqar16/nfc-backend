import json
import jwt
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import CustomUserCreateSerializer
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

User = get_user_model()


class CustomGoogleLogin(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        token = body.get('access_token')
        profile_type = body.get('profile_type')

        if not token:
            return JsonResponse({'error': 'Token not provided'}, status=400)

        if profile_type not in ['individual', 'employee', 'company']:
            return JsonResponse({'error': 'Invalid profile type'}, status=400)

        try:
            # Decode the JWT token
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            email = decoded_token.get('email')
            name = decoded_token.get('name')
            first_name, last_name = name.split(' ', 1) if ' ' in name else (name, '')

            if not email:
                return JsonResponse({'error': 'Failed to retrieve email from token'}, status=400)

            username = decoded_token.get('preferred_username', email)

            # Check if user exists by email
            user = User.objects.filter(email=email).first()

            if user:
                if user.has_usable_password():
                    return JsonResponse({'error': 'Account already exists with this email. Please login with your email and password.'}, status=400)
                
                # Update user profile_type if needed
                # if user.profile_type != profile_type:
                #     user.profile_type = profile_type
                #     user.save()
            else:
                # Create a new user if none exists
                user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name, profile_type=profile_type)
                user.set_unusable_password()
                user.save()

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
            })

        except jwt.PyJWTError as e:
            return JsonResponse({'error': 'Invalid token', 'details': str(e)}, status=400)


class DeleteGoogleAccountView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request):
        user = request.user
        # temporary left this commented will change this later for security purpose 
        
        # if user.authentication_type != 'google':
        #     return JsonResponse({'error': 'Invalid request'}, status=400)

        user.delete()
        return JsonResponse({'message': 'Account deleted successfully'}, status=204)


class CustomUserCreateView(APIView):
    def post(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def public_user_detail_view(request, pk):
    
#     # Retrieve the user or return a 404 if not found
#     user = get_object_or_404(User, id=pk)
    
#     # Serialize the user data
#     serializer = CustomUserSerializer(user)
    
#     # Return the serialized data
#     return Response(serializer.data)


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