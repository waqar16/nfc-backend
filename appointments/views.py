import datetime
import base64
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from django.conf import settings
import requests
from rest_framework.decorators import api_view
from google.auth.transport.requests import Request
from .models import Appointment
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.pagination import PageNumberPagination
from company.models import Company, Employee
from individual.models import UserProfile


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2  # Number of results per page
    page_size_query_param = 'page_size'
    max_page_size = 100


User = get_user_model()


def google_auth_request(request):
    title = request.GET.get('title')
    description = request.GET.get('description')
    start_datetime = request.GET.get('start_datetime')
    attendee_email = request.GET.get('attendee_email')
    user_id = request.GET.get('user_id')
    username = request.GET.get('username')

    # Store the meeting details in the session
    request.session['meeting_details'] = {
        'title': title,
        'description': description,
        'start_datetime': start_datetime,
        'attendee_email': attendee_email,
        'user_id': user_id,
        'username': username
    }

    # Check if user is already authenticated
    if 'google_credentials' in request.session:
        return redirect('/api/schedule-meeting/' + build_query_params(request.session['meeting_details']))

    flow = Flow.from_client_secrets_file(
        settings.CREDENTIALS,
        scopes=[
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email',
            'openid',
        ],

        redirect_uri=request.build_absolute_uri('/google/callback/')
    )
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return redirect(authorization_url)


def google_auth_callback(request):
    flow = Flow.from_client_secrets_file(
        settings.CREDENTIALS,
        scopes=[
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email',
            'openid',
        ],
        redirect_uri=request.build_absolute_uri('/google/callback/')
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    request.session['google_credentials'] = {
        'access_token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'expires_in': credentials.expiry.timestamp(),
    }

    # Access token
    access_token = credentials.token

    # Fetch ID token from Google API
    token_info_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
    response = requests.get(f'{token_info_url}?access_token={access_token}')
    token_info = response.json()

    id_token = token_info.get('id_token')

    request.session['google_credentials'] = {
        'access_token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'expires_in': credentials.expiry.timestamp(),
        'id_token': id_token,
    }
    # Retrieve meeting details from the session
    meeting_details = request.session.get('meeting_details')

    # if not meeting_details:
    #     return redirect('https://letsconnect.onesec.shop/schedule-meeting')

    # Construct the query parameters from the session data
    query_params = build_query_params(meeting_details)

    return redirect(f'/api/schedule-meeting/{query_params}')


@api_view(['POST', 'GET'])
def schedule_meeting(request):
    credentials_data = request.session.get('google_credentials')
    if not credentials_data:
        meeting_details = request.session.get('meeting_details')
        query_params = build_query_params(meeting_details)
        request.session.pop('google_credentials', None)
        return redirect(f'/api/schedule-meeting/{query_params}')
    
    # payload = {
    #     'access_token2': credentials_data['access_token'],
    #     'profile_type': 'individual',
    # }

    # # Make the POST request to your custom Google login endpoint
    # custom_google_login_url = 'https://localhost:8000/auth/custom-google-login/'
    # google_response = requests.post(custom_google_login_url, json=payload, verify=False)

    google_user_info = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers={'Authorization': f'Bearer {credentials_data["access_token"]}'})

    if google_user_info.status_code == 200:
        print("Custom Google login successful")
        google_user_info = google_user_info.json()
        print(google_user_info)
        email = google_user_info.get('email')
        name = google_user_info.get('name')
        first_name, last_name = name.split(' ', 1) if ' ' in name else (name, '')
        # picture = google_user_info.get('picture')
        host_object, created = User.objects.get_or_create(email=email, defaults={'first_name': first_name, 'last_name': last_name})
        host = host_object.id
        # host = google_response.json().get('user_id')
        # return Response(google_response.json())
    else:
        print(f"Custom Google login failed with status code {google_user_info.status_code}")
        # return Response(google_response.json())

    # # Extract the access token from credentials_data
    # access_token = credentials_data['access_token']

    # # Exchange the access token for an ID token
    # token_uri = 'https://oauth2.googleapis.com/token'
    # data = {
    #     'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
    #     'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token',
    #     'subject_token': access_token,
    #     'requested_token_type': 'urn:ietf:params:oauth:token-type:id_token'
    # }
    # response = requests.get(token_uri, data=data)

    # if response.status_code == 200:
    #     id_token = response.json().get('id_token')
    #     if not id_token:
    #         print("Failed to retrieve ID token")
    #         return Response({'error': 'Failed to retrieve ID token'}, status=400)

    #     # Prepare the payload
    #     payload = {
    #         'id_token': id_token,
    #         'profile_type': 'individual',
    #     }

    #     # Make the POST request to your custom Google login endpoint
    #     custom_google_login_url = 'https://localhost:8000/auth/custom-google-login/'
    #     google_response = requests.post(custom_google_login_url, json=payload)

    #     if google_response.status_code == 200:
    #         print("Custom Google login successful")
    #         host = google_response.json().get('user_id')
    #         return Response(google_response.json())
    #     else:
    #         print(f"Custom Google login failed with status code {google_response.status_code}")
    #         return Response(google_response.json())
    # else:
    #     print(f"Failed to exchange access token with status code {response.status_code}")
    #     # return Response(response.json())

    try:
        credentials = Credentials(
            token=credentials_data['access_token'],
            refresh_token=credentials_data['refresh_token'],
            token_uri='https://oauth2.googleapis.com/token',
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET
        )

        # Refresh the token if it is expired
        if credentials.expired:
            credentials.refresh(Request())

        print(credentials_data)
        print("Request Data:", request.data)

        # payload = {
        #     'access_token': credentials_data['access_token'],
        #     'profile_type': 'individual',
        # }
        # response = requests.post('https://127.0.0.1:8000/auth/custom-google-login/', json=payload, verify=False)

        title = request.query_params.get('title')
        description = request.query_params.get('description')
        start_datetime = request.query_params.get('start_datetime')
        attendee_email = request.query_params.get('attendee_email')
        user_id = request.query_params.get('user_id') #attendee
        username = request.query_params.get('username') #ateeendee

        # Ensure all required fields are present
        if not title:
            return Response({'error': 'title is required'}, status=400)
        if not description:
            return Response({'error': 'description is required'}, status=400)
        if not start_datetime:
            return Response({'error': 'start_datetime is required'}, status=400)
        if not attendee_email:
            return Response({'error': 'attendee_email is required'}, status=400)

        start_time = datetime.datetime.fromisoformat(start_datetime).isoformat()
        end_time = (datetime.datetime.fromisoformat(start_datetime) + datetime.timedelta(hours=1)).isoformat()

        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            },
            'attendees': [
                {'email': attendee_email},
            ],
            'conferenceData': {
                'createRequest': {
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    },
                    'requestId': 'sample123'
                }
            },
            'reminders': {
                'useDefault': True,
            },
        }

        response = requests.post(
            'https://www.googleapis.com/calendar/v3/calendars/primary/events',
            headers={'Authorization': f'Bearer {credentials.token}', 'Content-Type': 'application/json'},
            json=event
        )
        if response.status_code == 200:
            # return Response(response.json())
            # Fetch the user instance
            user = get_object_or_404(User, id=user_id)
            host = get_object_or_404(User, id=host)
            Appointment.objects.create(
                attendee=user,
                host=host,
                host_email=host.email,
                attendee_email=user.email,
                title=title,
                description=description,
                datetime=start_datetime,
                google_event_id=response.json()['id'],
                meeting_status='pending'
            )
            if user.profile_type == 'individual':
                # return redirect(f'https://letsconnect.onesec.shop/profile/{username}?status=success')
                return redirect(f'https://letsconnect.onesec.shop/')
            else:
                # return redirect(f'https://letsconnect.onesec.shop/company/{username}?status=success')
                return redirect(f'https://letsconnect.onesec.shop/')

            # return redirect('https://calendar.google.com/calendar/u/0/r')
        
        elif response.status_code == 401:
            # If the token is invalid, reauthorize the user
            # Retrieve meeting details from the session
            meeting_details = request.session.get('meeting_details')
            query_params = build_query_params(meeting_details)
            request.session.pop('google_credentials', None)
            return redirect(f'/api/schedule-meeting/{query_params}')
        else:
            # return Response(response.json(), status=response.status_code)

            if user.profile_type == 'individual':
                # return redirect(f'https://letsconnect.onesec.shop/profile/{username}?status=failure')
                return redirect('https://calendar.google.com/calendar/u/0/r')
            else:
                # return redirect(f'https://letsconnect.onesec.shop/company/{username}?status=failure')
                return redirect('https://calendar.google.com/calendar/u/0/r')
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_meetings(request):
    user = request.user

    # Appointments where the authenticated user is the host
    host_appointments = Appointment.objects.filter(host=user)

    # Appointments where the authenticated user is an attendee
    attendee_appointments = Appointment.objects.filter(attendee=user)

    # Create a dictionary to store unique appointments by ID
    appointments_dict = {}

    # Process host appointments
    for appointment in host_appointments:
        appointments_dict[appointment.id] = {
            'title': appointment.title,
            'description': appointment.description,
            'host_email': appointment.host.email,
            'datetime': appointment.datetime,
            'meeting_status': appointment.meeting_status,
            'type': 'host'  # Distinguish the type
        }

    # Process attendee appointments
    for appointment in attendee_appointments:
        # If the appointment is already in the dictionary, update the type if needed
        if appointment.id in appointments_dict:
            appointments_dict[appointment.id]['type'] = 'host & attendee'
        else:
            appointments_dict[appointment.id] = {
                'title': appointment.title,
                'description': appointment.description,
                'attendee_email': appointment.attendee.email,
                'datetime': appointment.datetime,
                'meeting_status': appointment.meeting_status,
                'type': 'attendee'  # Distinguish the type
            }

    # Convert dictionary to a list
    combined_data = list(appointments_dict.values())

    # Pagination
    paginator = StandardResultsSetPagination()
    paginated_data = paginator.paginate_queryset(combined_data, request)

    return paginator.get_paginated_response(paginated_data)


def download_vcard(request, user_id):
    user = get_object_or_404(User, id=user_id)

    def get_base64_image(url):
        if not url:
            return None  # Return None if no URL is provided
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for invalid responses
            return base64.b64encode(response.content).decode('utf-8')
        except requests.exceptions.RequestException:
            return None  # Handle invalid or inaccessible URLs gracefully

    if user.profile_type == 'employee':
        employee_profile = get_object_or_404(Employee, email=user.email)
        profile_pic_base64 = get_base64_image(employee_profile.profile_pic)
        vcard_data = f"""
BEGIN:VCARD
VERSION:3.0
N:{employee_profile.last_name};{employee_profile.first_name};;;
FN:{employee_profile.first_name} {employee_profile.last_name}
TITLE:{employee_profile.position}
TEL;TYPE=WORK,VOICE:{employee_profile.phone}
TEL;TYPE=HOME,VOICE:{employee_profile.phone}
ADR;TYPE=WORK,PREF:;;{employee_profile.address};;;;
ADR;TYPE=HOME:;;{employee_profile.address};;;;
EMAIL;TYPE=INTERNET:{employee_profile.email}
""".strip()

        # Only add the photo section if the profile picture is available
        if profile_pic_base64:
            vcard_data += f"\nPHOTO;ENCODING=b;TYPE=JPEG:{profile_pic_base64}"

        vcard_data += "\nEND:VCARD"
        filename = f"{employee_profile.first_name}_{employee_profile.last_name}_contact.vcf"

    elif user.profile_type == 'individual':
        user_profile = get_object_or_404(UserProfile, email=user.email)
        profile_pic_base64 = get_base64_image(user_profile.profile_pic)
        vcard_data = f"""
BEGIN:VCARD
VERSION:3.0
N:{user_profile.last_name};{user_profile.first_name};;;
FN:{user_profile.first_name} {user_profile.last_name}
TITLE:{user_profile.position}
TEL;TYPE=WORK,VOICE:{user_profile.phone}
TEL;TYPE=HOME,VOICE:{user_profile.phone}
ADR;TYPE=WORK,PREF:;;{user_profile.address};;;;
ADR;TYPE=HOME:;;{user_profile.address};;;;
EMAIL;TYPE=INTERNET:{user_profile.email}
""".strip()

        # Only add the photo section if the profile picture is available
        if profile_pic_base64:
            vcard_data += f"\nPHOTO;ENCODING=b;TYPE=JPEG:{profile_pic_base64}"

        vcard_data += "\nEND:VCARD"
        filename = f"{user_profile.first_name}_{user_profile.last_name}_contact.vcf"

    elif user.profile_type == 'company':
        company = get_object_or_404(Company, email=user.email)
        logo_base64 = get_base64_image(company.company_logo)
        vcard_data = f"""
BEGIN:VCARD
VERSION:3.0
FN:{company.admin_name}
ORG:{company.company_name}
TEL;TYPE=WORK,VOICE:{company.phone}
TEL;TYPE=HOME,VOICE:{company.phone}
ADR;TYPE=WORK,PREF:;;{company.address};;;;
ADR;TYPE=HOME:;;{company.address};;;;
EMAIL;TYPE=INTERNET:{company.email}
""".strip()

        # Only add the logo section if the company logo is available
        if logo_base64:
            vcard_data += f"\nPHOTO;ENCODING=b;TYPE=JPEG:{logo_base64}"

        vcard_data += "\nEND:VCARD"
        filename = f"{company.admin_name}_contact.vcf"

    else:
        return HttpResponseForbidden("Invalid account type")

    # Send the vCard file as a response
    response = HttpResponse(vcard_data, content_type='text/vcard')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

# def download_vcard(request, user_id):
#     user = get_object_or_404(User, id=user_id)

#     def get_base64_image(url):
#         response = requests.get(url)
#         return base64.b64encode(response.content).decode('utf-8')

#     if user.profile_type == 'employee':
#         employee_profile = get_object_or_404(Employee, email=user.email)
#         profile_pic_base64 = get_base64_image(employee_profile.profile_pic)
#         vcard_data = f"""
# BEGIN:VCARD
# VERSION:3.0
# N:{employee_profile.last_name};{employee_profile.first_name};;;
# FN:{employee_profile.first_name} {employee_profile.last_name}
# TITLE:{employee_profile.position}
# PHOTO;ENCODING=b;TYPE=JPEG:{profile_pic_base64}
# TEL;TYPE=WORK,VOICE:{employee_profile.phone}
# TEL;TYPE=HOME,VOICE:{employee_profile.phone}
# ADR;TYPE=WORK,PREF:;;{employee_profile.address};;;;
# ADR;TYPE=HOME:;;{employee_profile.address};;;;
# EMAIL;TYPE=INTERNET:{employee_profile.email}
# END:VCARD
# """.strip()
#         filename = f"{employee_profile.first_name}_{employee_profile.last_name}_contact.vcf"

#     elif user.profile_type == 'individual':
#         user_profile = get_object_or_404(UserProfile, email=user.email)
#         profile_pic_base64 = get_base64_image(user_profile.profile_pic)
#         vcard_data = f"""
# BEGIN:VCARD
# VERSION:3.0
# N:{user_profile.last_name};{user_profile.first_name};;;
# FN:{user_profile.first_name} {user_profile.last_name}
# TITLE:{user_profile.position}
# PHOTO;ENCODING=b;TYPE=JPEG:{profile_pic_base64}
# TEL;TYPE=WORK,VOICE:{user_profile.phone}
# TEL;TYPE=HOME,VOICE:{user_profile.phone}
# ADR;TYPE=WORK,PREF:;;{user_profile.address};;;;
# ADR;TYPE=HOME:;;{user_profile.address};;;;
# EMAIL;TYPE=INTERNET:{user_profile.email}
# END:VCARD
# """.strip()
#         filename = f"{user_profile.first_name}_{user_profile.last_name}_contact.vcf"

#     elif user.profile_type == 'company':
#         company = get_object_or_404(Company, email=user.email)
#         logo_base64 = get_base64_image(company.company_logo)
#         vcard_data = f"""
# BEGIN:VCARD
# VERSION:3.0
# FN:{company.admin_name}
# ORG:{company.company_name}
# PHOTO;ENCODING=b;TYPE=JPEG:{logo_base64}
# TEL;TYPE=WORK,VOICE:{company.phone}
# TEL;TYPE=HOME,VOICE:{company.phone}
# ADR;TYPE=WORK,PREF:;;{company.address};;;;
# ADR;TYPE=HOME:;;{company.address};;;;
# EMAIL;TYPE=INTERNET:{company.email}
# END:VCARD
# """.strip()
#         filename = f"{company.admin_name}_contact.vcf"

#     else:
#         return HttpResponseForbidden("Invalid account type")

#     response = HttpResponse(vcard_data, content_type='text/vcard')
#     response['Content-Disposition'] = f'attachment; filename="{filename}"'
#     return response


def build_query_params(meeting_details):
    return f"?title={meeting_details['title']}&description={meeting_details['description']}&start_datetime={meeting_details['start_datetime']}&attendee_email={meeting_details['attendee_email']}&user_id={meeting_details['user_id']}"
