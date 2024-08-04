from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Interaction, Contact
from .serializers import InteractionSerializer, ContactSerializer
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from .utils import fetch_country_from_ip, get_public_ip
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncHour
from django.db.models import F
import calendar



# @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# def create_interaction(request):
#     data = request.data
#     ip_address = get_public_ip()
#     country = fetch_country_from_ip(ip_address)
#     # Set the location using a placeholder or user's IP address
#     data['location'] = country
#     serializer = InteractionSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     print(serializer.errors)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_interaction(request):
    data = request.data
    
    # Extract user's IP address from the request
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_address:
        ip_address = ip_address.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    # Extracted IP address for debugging purposes
    print(f"Extracted IP address: {ip_address}")
    
    # Fetch country information based on the user's IP address
    country = fetch_country_from_ip(ip_address)
    
    # Set the location using the user's IP address
    data['location'] = country
    
    serializer = InteractionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_contact(request):
    user = request.user
    data = request.data
    data['user'] = user.id
    serializer = ContactSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_contact(request):
    user = request.user
    data = request.data
    data['user'] = user.id
    serializer = ContactSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def interaction_frequency_view(request, period):
    user = request.user

    # Determine the start date and truncation function based on the period
    if period == 'daily':
        start_date = timezone.now() - timedelta(days=7)
        trunc_func = TruncHour
        period_format = '%H'  # Hour format
    elif period == 'weekly':
        start_date = timezone.now() - timedelta(weeks=1)  # Cover the last 7 days
        trunc_func = TruncDay
        period_format = '%A'  # Day of the week
    elif period == 'monthly':
        start_date = timezone.now() - timedelta(days=365)  # Cover the last 12 months
        trunc_func = TruncMonth
        period_format = '%b'  # Abbreviated month format
    else:
        return Response({"error": "Invalid period"}, status=400)

    # Filter interactions based on the user and the start date
    interactions = Interaction.objects.filter(user=user, timestamp__gte=start_date)

    # Annotate interactions with the appropriate period
    data = interactions.annotate(
        period_name=trunc_func('timestamp')
    ).values(
        period=F('period_name')
    ).annotate(
        count=Count('id')
    ).order_by('period')

    # Print raw data for debugging
    print("Raw Data:", list(data))

    # Initialize complete data
    if period == 'daily':
        complete_data = {str(hour): 0 for hour in range(24)}  # 0-23 hours
    elif period == 'weekly':
        complete_data = {day: 0 for day in calendar.day_name}  # Monday to Sunday
    elif period == 'monthly':
        complete_data = {calendar.month_abbr[month]: 0 for month in range(1, 13)}

    # Update the complete list with actual interaction counts
    for item in data:
        period_name = item['period']
        period_name_str = period_name.strftime(period_format)
        if period_name_str in complete_data:
            complete_data[period_name_str] = item['count']

    # Convert the dictionary to a list of dictionaries for the response
    formatted_data = [{'period': period, 'count': count} for period, count in complete_data.items()]

    return Response(formatted_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def peak_interaction_time_view(request, period):
    user = request.user

    if period == 'time_of_day':
        start_date = timezone.now() - timedelta(days=30)  # Last 30 days
        trunc_func = TruncHour
        time_ranges = [f'{i:02d}:00 - {i+3:02d}:59' for i in range(0, 24, 3)]
    elif period == 'day_of_week':
        start_date = timezone.now() - timedelta(weeks=6)  # Last 6 weeks
        trunc_func = TruncDay
        period_format = '%A'
        time_ranges = list(calendar.day_name)
    else:
        return Response({"error": "Invalid period"}, status=400)

    interactions = Interaction.objects.filter(user=user, timestamp__gte=start_date)

    if period == 'time_of_day':
        data = interactions.annotate(
            period_name=trunc_func('timestamp')
        ).values(
            period=F('period_name')
        ).annotate(
            count=Count('id')
        ).order_by('period')

        complete_data = {time_range: 0 for time_range in time_ranges}

        for item in data:
            period_name = item['period']
            period_hour = period_name.hour
            time_range_index = period_hour // 3
            time_range = time_ranges[time_range_index]
            if time_range in complete_data:
                complete_data[time_range] += item['count']

    elif period == 'day_of_week':
        data = interactions.annotate(
            period_name=trunc_func('timestamp')
        ).values(
            period=F('period_name')
        ).annotate(
            count=Count('id')
        ).order_by('period')

        complete_data = {day: 0 for day in calendar.day_name}

        for item in data:
            period_name = item['period']
            period_name_str = period_name.strftime(period_format)
            if period_name_str in complete_data:
                complete_data[period_name_str] += item['count']

    formatted_data = [{'period': period, 'count': count} for period, count in complete_data.items()]

    return Response({'data': formatted_data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def geo_data_view(request):
    user = request.user
    interactions = Interaction.objects.filter(user=user)
    data = interactions.values('location').annotate(count=Count('id')).order_by('-count')

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sharing_networking_view(request):
    user = request.user
    contacts = Contact.objects.filter(user=user)
    new_contacts = contacts.count()
    follow_up = contacts.filter(followed_up=True).count()

    data = {
        "new_contacts": new_contacts,
        "follow_up": follow_up
    }

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def card_distribution_usage_view(request):
    cards = Interaction.objects.values('user').distinct().count()
    active_cards = Interaction.objects.values('user').annotate(count=Count('id')).filter(count__gte=1).count()

    data = {
        "total_cards": cards,
        "active_cards": active_cards,
        "inactive_cards": cards - active_cards
    }

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def engagement_metrics_view(request):
    interactions = Interaction.objects.all()
    total_interactions = interactions.count()
    interactions_by_department = interactions.values('user__profile__department').annotate(count=Count('id')).order_by('-count')

    data = {
        "total_interactions": total_interactions,
        "interactions_by_department": interactions_by_department
    }

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def networking_effectiveness_view(request):
    contacts = Contact.objects.all()
    new_connections = contacts.count()
    follow_up_rates = contacts.filter(followed_up=True).count()

    data = {
        "new_connections": new_connections,
        "follow_up_rates": follow_up_rates
    }

    return Response(data)
