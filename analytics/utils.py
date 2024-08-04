from django.conf import settings
import requests


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        data = response.json()
        return data.get('ip', 'Unknown')
    except requests.RequestException:
        return 'Unknown'


def fetch_country_from_ip(ip_address):
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json")
        response.raise_for_status()
        data = response.json()
        return data.get("country", "Unknown")
    except requests.RequestException:
        return "Unknown"

# def fetch_country_from_ip(ip_address):
#     try:
#         response = requests.get(f"https://ipinfo.io/{ip_address}/json", headers={"Authorization": f"Bearer {settings.IPINFO_TOKEN}"})
#         response.raise_for_status()
#         data = response.json()
#         return data.get("country", "Unknown")
#     except requests.RequestException:
#         return "Unknown"
