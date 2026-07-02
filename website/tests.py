from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ContactRequest, NewsletterSignup, Property, PropertyPhoto


class PublicSiteApiTests(TestCase):
    def test_site_payload_exposes_dynamic_properties(self):
        property_obj = Property.objects.create(
            transaction=Property.SALE,
            property_type=Property.APARTMENT,
            title="Appartement test",
            residence="Hilton",
            bedrooms=2,
            surface_total=74,
        )
        PropertyPhoto.objects.create(
            property=property_obj,
            title="Salon",
            image_path="/assets/city-center/city-center-salon.png",
            alt_text="Salon de l'appartement test",
            sort_order=1,
        )

        response = self.client.get(reverse("public-site"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["properties"][0]["title"], "Appartement test")
        self.assertEqual(payload["properties"][0]["surface_total"], 74.0)
        self.assertEqual(payload["properties"][0]["photos"][0]["title"], "Salon")
        self.assertEqual(
            payload["properties"][0]["photos"][0]["image"],
            "/assets/city-center/city-center-salon.png",
        )

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


class AdminEmailLoginTests(TestCase):
    def test_admin_login_uses_email(self):
        get_user_model().objects.create_superuser(
            email="admin@nectar.test",
            password="secure-admin-password",
        )

        response = self.client.post(
            reverse("admin:login"),
            {
                "username": "admin@nectar.test",
                "password": "secure-admin-password",
                "next": reverse("admin:index"),
            },
            follow=True,
        )

        self.assertTrue(response.context["user"].is_authenticated)
