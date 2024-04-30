from django.contrib.auth.models import Group
from social_core.exceptions import AuthForbidden
from wagtail.core.models import Site

from home.models import SiteSettings


def set_permissions(user, is_new, request, *args, **kwargs):
    if user and is_new:
        # Restrict new users to the site they logged in on
        site = Site.find_for_request(request)
        group = Group.objects.filter(name__iexact=f"{site.site_name} Editors").first()

        if not group:
            group = Group.objects.get(name="Editors")
        user.groups.add(group)
        user.save()


def auth_allowed(user, backend, details, response, request, *args, **kwargs):
    # Allow users with the Administrator role to always login from any site
    if user and user.is_superuser:
        return

    # Check if this Google email is in the whitelist for the site
    site = Site.find_for_request(request)
    site_settings = SiteSettings.for_site(site)

    allowed_emails = [
        str(email).lower() for email in site_settings.allowed_emails.__iter__()
    ]
    email = details.get("email")

    allowed = False
    if email and allowed_emails:
        email = email.lower()
        allowed = email in allowed_emails
    if not allowed:
        raise AuthForbidden(backend)
