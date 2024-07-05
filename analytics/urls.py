from django.urls import path
from .views import (
    interaction_frequency_view,
    peak_interaction_time_view,
    geo_data_view,
    sharing_networking_view,
    card_distribution_usage_view,
    engagement_metrics_view,
    networking_effectiveness_view,
    create_interaction,
    create_contact
)

urlpatterns = [
    path('interactions/', create_interaction, name='create_interaction'),
    path('contacts/', create_contact, name='create_contact'),
    path('interaction-frequency/<str:period>/', interaction_frequency_view, name='interaction-frequency'),
    path('peak-interaction-time/', peak_interaction_time_view, name='peak-interaction-time'),
    path('geo-data/', geo_data_view, name='geo-data'),
    path('sharing-networking/', sharing_networking_view, name='sharing-networking'),
    path('card-distribution-usage/', card_distribution_usage_view, name='card-distribution-usage'),
    path('engagement-metrics/', engagement_metrics_view, name='engagement-metrics'),
    path('networking-effectiveness/', networking_effectiveness_view, name='networking-effectiveness'),
]
