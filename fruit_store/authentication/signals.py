import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse
from allauth.socialaccount.signals import social_account_updated
from django.dispatch import receiver
from .models import User
import logging

logger = logging.getLogger(__name__)

@receiver(social_account_updated)
def save_profile_image(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    provider = sociallogin.account.provider
    logger.info(f"Social account updated for user {user}. Provider: {provider}")
    if provider == 'google':
        picture_url = sociallogin.account.extra_data.get('picture')
        logger.info(f"Picture URL: {picture_url}")
        if picture_url:
            response = requests.get(picture_url)
            logger.info(f"Response status code: {response.status_code}")
            if response.status_code == 200:
                img_content = ContentFile(response.content)
                img_name = urlparse(picture_url).path.split('/')[-1]
                user.profile_img.save(img_name, img_content, save=True)
                logger.info(f"Saved profile image for user {user}.")
