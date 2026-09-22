from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactRequest, NewsletterSignup, Property, PropertyPhoto, PurplePearlVisitRequest


class PublicSiteApiTests(TestCase):
    def test_site_payload_exposes_dynamic_properties(self):
        property_obj = Property.objects.create(
            transaction=Property.SALE,
            property_type=Property.APARTMENT,
            is_sold=True,
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
        self.assertIs(payload["properties"][0]["is_sold"], True)
        self.assertEqual(payload["properties"][0]["surface_total"], 74.0)
        self.assertEqual(payload["properties"][0]["photos"][0]["title"], "Salon")
        self.assertEqual(
            payload["properties"][0]["photos"][0]["image"],
            "/assets/city-center/city-center-salon.png",
        )

    @override_settings(
        CONTACT_NOTIFICATION_EMAILS=["contact@nectar.ma"],
        DEFAULT_FROM_EMAIL="website@nectar.ma",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        NEWSLETTER_NOTIFICATION_EMAILS=["info@nectar.ma"],
        PURPLE_PEARL_VISIT_NOTIFICATION_EMAILS=["contact@nectar.ma"],
    )
    def test_contact_newsletter_and_visit_forms_create_admin_entries_and_notify(self):
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
        visit_response = self.client.post(
            reverse("purple-pearl-visits"),
            {
                "visit_type": "Visite projet",
                "preferred_date": "2026-07-22",
                "preferred_time": "10:00",
                "full_name": "Client Purple",
                "phone": "0700000000",
                "email": "purple@example.com",
                "message": "Je souhaite visiter le projet.",
                "consent": True,
            },
            content_type="application/json",
        )
        newsletter_response = self.client.post(
            reverse("newsletter-signups"),
            {"email": "client@example.com", "source": "home"},
            content_type="application/json",
        )

        self.assertEqual(contact_response.status_code, 201)
        self.assertEqual(visit_response.status_code, 201)
        self.assertEqual(newsletter_response.status_code, 201)
        self.assertEqual(ContactRequest.objects.count(), 1)
        self.assertEqual(PurplePearlVisitRequest.objects.count(), 1)
        self.assertEqual(NewsletterSignup.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 3)
        self.assertEqual(mail.outbox[0].to, ["contact@nectar.ma"])
        self.assertIn("Nouvelle demande de contact", mail.outbox[0].subject)
        self.assertIn("Client Test", mail.outbox[0].body)
        self.assertEqual(mail.outbox[1].to, ["contact@nectar.ma"])
        self.assertIn("Nouvelle demande de visite", mail.outbox[1].subject)
        self.assertIn("Client Purple", mail.outbox[1].body)
        self.assertEqual(mail.outbox[2].to, ["info@nectar.ma"])
        self.assertIn("Nouvelle inscription newsletter", mail.outbox[2].subject)


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
