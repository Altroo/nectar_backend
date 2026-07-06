import logging

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    ContactRequest,
    EventIdea,
    GuidePlace,
    NewsletterSignup,
    Property,
    PurplePearlPlan,
    PurplePearlVisitRequest,
    SiteContact,
    Testimonial,
)
from .serializers import (
    ContactRequestSerializer,
    EventIdeaSerializer,
    GuidePlaceSerializer,
    NewsletterSignupSerializer,
    PropertySerializer,
    PurplePearlPlanSerializer,
    PurplePearlVisitRequestSerializer,
    SiteContactSerializer,
    TestimonialSerializer,
)

logger = logging.getLogger(__name__)


def _recipient_list(value):
    if isinstance(value, (list, tuple)):
        return [email for email in value if email]
    return [email.strip() for email in str(value or "").split(",") if email.strip()]


def _display(value):
    if value is None or value == "":
        return "-"
    return str(value)


def _display_date(value):
    if not value:
        return "-"
    return value.strftime("%d/%m/%Y")


def _send_site_notification(subject, lines, recipient_setting):
    recipients = _recipient_list(getattr(settings, recipient_setting, ""))
    if not recipients:
        return
    try:
        send_mail(
            subject=subject,
            message="\n".join(lines),
            from_email=settings.DEFAULT_FROM_EMAIL or settings.SERVER_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
    except Exception:
        logger.exception("Failed to send site notification: %s", subject)


def _notify_contact_request(contact_request):
    _send_site_notification(
        "Nouvelle demande de contact - Nectar",
        [
            "Une nouvelle demande a ete envoyee depuis le site Nectar.",
            "",
            f"Nom complet : {_display(contact_request.full_name)}",
            f"Telephone : {_display(contact_request.phone)}",
            f"Email : {_display(contact_request.email)}",
            f"Projet : {_display(contact_request.project)}",
            f"Type de bien : {_display(contact_request.property_type)}",
            f"Budget : {_display(contact_request.budget)}",
            f"Date souhaitee : {_display_date(contact_request.preferred_date)}",
            f"Heure souhaitee : {_display(contact_request.preferred_time)}",
            f"Mode de rendez-vous : {_display(contact_request.appointment_mode)}",
            "",
            "Message :",
            _display(contact_request.message),
        ],
        "CONTACT_NOTIFICATION_EMAILS",
    )


def _notify_purple_pearl_visit(visit_request):
    _send_site_notification(
        "Nouvelle demande de visite - Purple Pearl",
        [
            "Une nouvelle demande de visite Purple Pearl a ete envoyee depuis le site.",
            "",
            f"Type de visite : {_display(visit_request.visit_type)}",
            f"Date souhaitee : {_display_date(visit_request.preferred_date)}",
            f"Heure souhaitee : {_display(visit_request.preferred_time)}",
            f"Nom complet : {_display(visit_request.full_name)}",
            f"Telephone : {_display(visit_request.phone)}",
            f"Email : {_display(visit_request.email)}",
            f"Consentement : {'oui' if visit_request.consent else 'non'}",
            "",
            "Message :",
            _display(visit_request.message),
        ],
        "PURPLE_PEARL_VISIT_NOTIFICATION_EMAILS",
    )


def _notify_newsletter_signup(signup):
    _send_site_notification(
        "Nouvelle inscription newsletter - Nectar",
        [
            "Une nouvelle inscription newsletter a ete envoyee depuis le site Nectar.",
            "",
            f"Email : {_display(signup.email)}",
            f"Origine : {_display(signup.source)}",
        ],
        "NEWSLETTER_NOTIFICATION_EMAILS",
    )


class PublicMixin:
    authentication_classes = ()
    permission_classes = (AllowAny,)


class PublicSiteView(PublicMixin, APIView):
    def get(self, request):
        context = {"request": request}
        contact = SiteContact.objects.filter(is_active=True).order_by("sort_order", "id").first()
        contact_data = (
            SiteContactSerializer(contact, context=context).data
            if contact
            else {
                "address": "Tanger, Maroc",
                "phone_display": getattr(settings, "SITE_PHONE_DISPLAY", ""),
                "whatsapp_number": getattr(settings, "SITE_PHONE", ""),
                "email_display": getattr(settings, "SITE_EMAIL_DISPLAY", ""),
            }
        )
        return Response(
            {
                "defaultLang": getattr(settings, "SITE_DEFAULT_LANG", "fr"),
                "contact": contact_data,
                "properties": PropertySerializer(
                    Property.objects.filter(is_active=True)
                    .prefetch_related("photos")
                    .order_by("sort_order", "title"),
                    many=True,
                    context=context,
                ).data,
                "guidePlaces": GuidePlaceSerializer(
                    GuidePlace.objects.filter(is_active=True).order_by("section", "sort_order", "title"),
                    many=True,
                    context=context,
                ).data,
                "eventIdeas": EventIdeaSerializer(
                    EventIdea.objects.filter(is_active=True).order_by("sort_order", "title"),
                    many=True,
                    context=context,
                ).data,
                "purplePearlPlans": PurplePearlPlanSerializer(
                    PurplePearlPlan.objects.filter(is_active=True).order_by("sort_order", "title"),
                    many=True,
                    context=context,
                ).data,
                "testimonials": TestimonialSerializer(
                    Testimonial.objects.filter(is_active=True).order_by("sort_order", "client_name"),
                    many=True,
                ).data,
            }
        )


class PropertyListView(PublicMixin, generics.ListAPIView):
    serializer_class = PropertySerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Property.objects.filter(is_active=True).prefetch_related("photos").order_by("sort_order", "title")
        transaction = self.request.query_params.get("transaction")
        property_type = self.request.query_params.get("property_type")
        if transaction:
            queryset = queryset.filter(transaction=transaction)
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        return queryset


class ContactRequestCreateView(PublicMixin, generics.CreateAPIView):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer

    def perform_create(self, serializer):
        contact_request = serializer.save()
        _notify_contact_request(contact_request)


class PurplePearlVisitRequestCreateView(PublicMixin, generics.CreateAPIView):
    queryset = PurplePearlVisitRequest.objects.all()
    serializer_class = PurplePearlVisitRequestSerializer

    def perform_create(self, serializer):
        visit_request = serializer.save()
        _notify_purple_pearl_visit(visit_request)


class NewsletterSignupCreateView(PublicMixin, generics.CreateAPIView):
    queryset = NewsletterSignup.objects.all()
    serializer_class = NewsletterSignupSerializer

    def perform_create(self, serializer):
        signup = serializer.save()
        _notify_newsletter_signup(signup)
