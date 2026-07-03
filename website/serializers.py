from rest_framework import serializers

from .models import (
    ContactRequest,
    EventIdea,
    GuidePlace,
    NewsletterSignup,
    Property,
    PropertyPhoto,
    PurplePearlPlan,
    PurplePearlVisitRequest,
    SiteContact,
    Testimonial,
)


def image_url(request, obj, image_field="image", path_field="image_path"):
    image = getattr(obj, image_field)
    if image:
        try:
            url = image.url
        except ValueError:
            url = ""
        if url:
            return request.build_absolute_uri(url) if request else url
    return getattr(obj, path_field)


class SiteContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContact
        fields = (
            "address",
            "phone_display",
            "whatsapp_number",
            "email_display",
        )


class PropertyPhotoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PropertyPhoto
        fields = ("id", "title", "alt_text", "image", "sort_order")

    def get_image(self, obj):
        return image_url(self.context.get("request"), obj)


class PropertySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    surface_total = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            "id",
            "transaction",
            "property_type",
            "title",
            "tag",
            "residence",
            "district",
            "address",
            "description",
            "floor",
            "unit_number",
            "bedrooms",
            "surface_total",
            "surface_sold",
            "mezzanine",
            "project_label",
            "price",
            "price_note",
            "cta_label",
            "image",
            "photos",
            "sort_order",
        )

    def get_image(self, obj):
        return image_url(self.context.get("request"), obj)

    def get_photos(self, obj):
        return PropertyPhotoSerializer(
            obj.photos.filter(is_active=True).order_by("sort_order", "id"),
            many=True,
            context=self.context,
        ).data

    def get_surface_total(self, obj):
        if obj.surface_total is None:
            return None
        return float(obj.surface_total)


class GuidePlaceSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = GuidePlace
        fields = ("id", "section", "title", "description", "image", "sort_order")

    def get_image(self, obj):
        return image_url(self.context.get("request"), obj)


class EventIdeaSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    bullet_points = serializers.SerializerMethodField()

    class Meta:
        model = EventIdea
        fields = ("id", "category", "title", "description", "bullet_points", "image", "sort_order")

    def get_image(self, obj):
        return image_url(self.context.get("request"), obj)

    def get_bullet_points(self, obj):
        return [line.strip() for line in obj.bullet_points.splitlines() if line.strip()]


class PurplePearlPlanSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_3d = serializers.SerializerMethodField()
    image_3d_secondary = serializers.SerializerMethodField()

    class Meta:
        model = PurplePearlPlan
        fields = (
            "id",
            "key",
            "button_label",
            "title",
            "description",
            "alt_text",
            "image",
            "image_3d_title",
            "image_3d",
            "image_3d_alt_text",
            "image_3d_secondary_title",
            "image_3d_secondary",
            "image_3d_secondary_alt_text",
            "sort_order",
        )

    def get_image(self, obj):
        return image_url(self.context.get("request"), obj)

    def get_image_3d(self, obj):
        return image_url(self.context.get("request"), obj, "image_3d", "image_3d_path")

    def get_image_3d_secondary(self, obj):
        return image_url(
            self.context.get("request"),
            obj,
            "image_3d_secondary",
            "image_3d_secondary_path",
        )


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ("id", "rating", "quote", "client_name", "details", "highlight_city_center", "sort_order")


class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = (
            "id",
            "created_at",
            "full_name",
            "phone",
            "email",
            "project",
            "property_type",
            "budget",
            "preferred_date",
            "preferred_time",
            "appointment_mode",
            "message",
        )
        read_only_fields = ("id", "created_at")


class PurplePearlVisitRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurplePearlVisitRequest
        fields = (
            "id",
            "created_at",
            "visit_type",
            "preferred_date",
            "preferred_time",
            "full_name",
            "phone",
            "email",
            "message",
            "consent",
        )
        read_only_fields = ("id", "created_at")


class NewsletterSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSignup
        fields = ("id", "created_at", "email", "source")
        read_only_fields = ("id", "created_at")
