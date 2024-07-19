from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings
from social_django.utils import load_strategy
from social_core.backends.google import GoogleOAuth2
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

User = get_user_model()


class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        strategy = load_strategy(request)
        backend = GoogleOAuth2(strategy)
        user = backend.do_auth(code)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key})
        
        return JsonResponse({'error': 'Authentication failed'}, status=400)
