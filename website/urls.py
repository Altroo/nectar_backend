from django.urls import path

from .views import (
    ContactRequestCreateView,
    NewsletterSignupCreateView,
    PropertyListView,
    PublicSiteView,
    PurplePearlVisitRequestCreateView,
)

urlpatterns = [
    path("content/", PublicSiteView.as_view(), name="public-site"),
    path("properties/", PropertyListView.as_view(), name="properties"),
    path("contact-requests/", ContactRequestCreateView.as_view(), name="contact-requests"),
    path("purple-pearl-visits/", PurplePearlVisitRequestCreateView.as_view(), name="purple-pearl-visits"),
    path("newsletter/", NewsletterSignupCreateView.as_view(), name="newsletter-signups"),
]
