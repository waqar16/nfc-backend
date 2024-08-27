from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Event
from individual.models import UserProfile
from company.models import Company, Employee
from nfc_backend.settings import EMAIL_HOST_USER


@receiver(post_save, sender=Event)
def send_event_email(sender, instance, created, **kwargs):
    if created:
        # Get all subscribed users
        subscribers_individual = UserProfile.objects.filter(receive_marketing_emails=True)
        subscribers_employee = Employee.objects.filter(receive_marketing_emails=True)
        subscribers_company = Company.objects.filter(receive_marketing_emails=True)

        # Combine all subscribers
        subscribers = list(subscribers_individual) + list(subscribers_employee) + list(subscribers_company)
        
        # Collect their email addresses
        emails = [subscriber.email for subscriber in subscribers]

        if emails:
            # Create the email subject
            subject = f"New Event: {instance.event_name}"
            
            # Render the HTML template with context
            html_content = render_to_string('emails/event_notification.html', {
                'event_name': instance.event_name,
                'event_date': instance.event_date,
                'event_time': instance.event_time,
                'event_location': instance.event_location,
                'event_description': instance.event_description,
            })
            
            # Fallback plain text content
            text_content = strip_tags(html_content)

            # Create the email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,  # Fallback for clients that don't support HTML
                from_email=EMAIL_HOST_USER,
                to=emails,
            )
            # Attach the HTML version
            email.attach_alternative(html_content, "text/html")
            
            # Send the email
            email.send(fail_silently=False)
