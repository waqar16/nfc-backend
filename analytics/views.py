from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Interaction, Contact
from .serializers import InteractionSerializer, ContactSerializer
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from rest_framework import status


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_interaction(request):
    user = request.user
    data = request.data
    data['user'] = user.id
    serializer = InteractionSerializer(data=data)
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

    if period == 'daily':
        start_date = timezone.now() - timedelta(days=1)
    elif period == 'weekly':
        start_date = timezone.now() - timedelta(days=7)
    elif period == 'monthly':
        start_date = timezone.now() - timedelta(days=30)
    else:
        return Response({"error": "Invalid period"}, status=400)

    interactions = Interaction.objects.filter(user=user, timestamp__gte=start_date)
    data = interactions.values('timestamp__date').annotate(count=Count('id')).order_by('timestamp__date')

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def peak_interaction_time_view(request):
    user = request.user
    interactions = Interaction.objects.filter(user=user)
    data = interactions.values('timestamp__hour').annotate(count=Count('id')).order_by('timestamp__hour')

    return Response(data)


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
