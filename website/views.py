from django.conf import settings
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
                    Property.objects.filter(is_active=True).order_by("sort_order", "title"),
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
        queryset = Property.objects.filter(is_active=True).order_by("sort_order", "title")
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


class PurplePearlVisitRequestCreateView(PublicMixin, generics.CreateAPIView):
    queryset = PurplePearlVisitRequest.objects.all()
    serializer_class = PurplePearlVisitRequestSerializer


class NewsletterSignupCreateView(PublicMixin, generics.CreateAPIView):
    queryset = NewsletterSignup.objects.all()
    serializer_class = NewsletterSignupSerializer
