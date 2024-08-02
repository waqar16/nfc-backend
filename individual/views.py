from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import UserProfile, Receivedprofile
from .serializers import UserProfileSerializer, ShareProfileSerializer, ReceivedprofileSerializer
from .utils import encrypt_data, decrypt_data
from django.contrib.auth import get_user_model
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.views.decorators.csrf import csrf_exempt
import json

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
        

# class ScheduleMeetingView(APIView):
#     # permission_classes = [IsAuthenticated]

#     def post(self, request):
#         date_time = request.data.get('dateTime')
#         attendee_email = request.data.get('attendeeEmail')
#         # user_token = request.data.get('userToken')
#         google_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImUyNmQ5MTdiMWZlOGRlMTMzODJhYTdjYzlhMWQ2ZTkzMjYyZjMzZTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxMDM2NDYxOTA5MDE4LXYzMmY5czM1aGVma2JlcTcwZ3RlcmgxMnNpb3VnNWE1LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTAzNjQ2MTkwOTAxOC12MzJmOXMzNWhlZmtiZXE3MGd0ZXJoMTJzaW91ZzVhNS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExNzIzMTE5NDE0ODA3MjQyNTA2MiIsImVtYWlsIjoidGhldGVjaGNvcm5lcjlAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5iZiI6MTcyMjI3ODk5NywibmFtZSI6IlRoZVRlY2hDb3JuZXIiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTEE0MTZwOTBhajdEY19oYWxFa01vMi1RUWlRYVVXbjdzMzF0RDNZUkgxa0FjbEhoND1zOTYtYyIsImdpdmVuX25hbWUiOiJUaGVUZWNoQ29ybmVyIiwiaWF0IjoxNzIyMjc5Mjk3LCJleHAiOjE3MjIyODI4OTcsImp0aSI6IjBhN2Q1ZWRmNGIxOWNjZjYyNjJhMDExZWEwZTY4ZTM5N2E4NjYzNjMifQ.2QgOtgKZhXZGMrK-N0JorwZuuqRP-mCh0uCSbG0s6P9jLa1x60kUGrzuW09n-nON2yuyRDBaQeHIoafjN5D8VvEQsRNBBVQNqUJGJqXiWGoFMt1m_IsE805s5xlGkKep558qLpXpSdxDad9RhuKcgGp7kVrecqRIl9E1bXas4u22tbPTffsngMq8MwRs3JY4mdXfYCadxsQrrlXK1IXE07U5B8zib9iIC8AC_9DKRSd7tD2l-htLI2Xjlk1HUcPI_iIqkzUG3h3ZTz6N-r1d16jLkPxZtZ-wIbWIV5dwkk8sgFVBpqi3XeMtBeTVjmTv7Mp3mhM2rCvoQn8zSasXRg"

#         if not google_token:
#             return Response({"error": "Google token is missing."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Use the Google token to build credentials
#             credentials = Credentials.from_authorized_user_info({"token": google_token})

#             service = build('calendar', 'v3', credentials=credentials)

#             event = {
#                 'summary': 'Scheduled Meeting',
#                 'description': 'Meeting scheduled through the app.',
#                 'start': {
#                     'dateTime': date_time,
#                     'timeZone': 'UTC',
#                 },
#                 'end': {
#                     'dateTime': (datetime.datetime.fromisoformat(date_time) + datetime.timedelta(hours=1)).isoformat(),
#                     'timeZone': 'UTC',
#                 },
#                 'attendees': [
#                     {'email': attendee_email},
#                 ],
#             }

#             event = service.events().insert(calendarId='primary', body=event).execute()
#             return Response({'message': 'Meeting scheduled successfully.', 'event': event}, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]


def google_calendar_callback(request):
    state = request.GET.get('state')
    code = request.GET.get('code')

    if not code:
        return JsonResponse('Authorization code missing', status=400)

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

    # Exchange the authorization code for tokens
    flow.fetch_token(code=code)
    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)
    print("Credentials:", credentials_to_dict(credentials))
    return redirect('google_calendar_events')


def google_calendar_init_view(request):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['state'] = state
    return redirect(authorization_url)


def google_calendar_redirect_view(request):
    state = request.session['state']
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
        state=state
    )
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    return redirect('google_calendar_events')


def google_calendar_events_view(request):
    if 'credentials' not in request.session:
        return redirect('google_calendar_init')

    credentials = Credentials(**request.session['credentials'])

    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary').execute()
    events = events_result.get('items', [])

    return JsonResponse(events, safe=False)


@csrf_exempt
@api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])
def google_calendar_create_event_view(request):
    if 'credentials' not in request.session:
        return redirect('google_calendar_init')

    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method.')

    credentials = Credentials(**request.session['credentials'])
    print("Credentials:", credentials)
    service = build('calendar', 'v3', credentials=credentials)

    # event_data = json.loads(request.body.decode('utf-8'))
    # event = {
    #     'summary': event_data.get('summary', 'No title'),
    #     'location': event_data.get('location', ''),
    #     'description': event_data.get('description', ''),
    #     'start': {
    #         'dateTime': event_data['start']['dateTime'],
    #         'timeZone': event_data['start']['timeZone'],
    #     },
    #     'end': {
    #         'dateTime': event_data['end']['dateTime'],
    #         'timeZone': event_data['end']['timeZone'],
    #     },
    #     'attendees': [{'email': email} for email in event_data.get('attendees', [])],
    #     'conferenceData': {
    #         'createRequest': {
    #             'conferenceSolutionKey': {'type': 'hangoutsMeet'},
    #             'requestId': 'randomString' 
    #         }
    #     },
    # }
    event_data = {
        'attendees': ['wa4752928@gmail.com']
    }

    event = {
        'summary': 'Static Event Title',
        'start': {
            'dateTime': '2024-08-01T10:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2024-08-01T11:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [{'email': email} for email in event_data.get('attendees', [])],
    }
    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()

    return JsonResponse(event)


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
