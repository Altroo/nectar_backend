from django.test import TestCase
from django.urls import reverse

from .models import ContactRequest, NewsletterSignup, Property


class PublicSiteApiTests(TestCase):
    def test_site_payload_exposes_dynamic_properties(self):
        Property.objects.create(
            transaction=Property.SALE,
            property_type=Property.APARTMENT,
            title="Appartement test",
            residence="Hilton",
            bedrooms=2,
            surface_total=74,
        )

        response = self.client.get(reverse("public-site"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["properties"][0]["title"], "Appartement test")
        self.assertEqual(payload["properties"][0]["surface_total"], 74.0)

    def test_contact_and_newsletter_forms_create_admin_entries(self):
        contact_response = self.client.post(
            reverse("contact-requests"),
            {
                "full_name": "Client Test",
                "phone": "0600000000",
                "email": "client@example.com",
                "project": "Achat",
                "property_type": "Appartement",
            },
            content_type="application/json",
        )
        newsletter_response = self.client.post(
            reverse("newsletter-signups"),
            {"email": "client@example.com", "source": "home"},
            content_type="application/json",
        )

        self.assertEqual(contact_response.status_code, 201)
        self.assertEqual(newsletter_response.status_code, 201)
        self.assertEqual(ContactRequest.objects.count(), 1)
        self.assertEqual(NewsletterSignup.objects.count(), 1)
