from django.contrib import admin

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


admin.site.site_header = "Administration Nectar"
admin.site.site_title = "Nectar"
admin.site.index_title = "Gestion du site"


class VisibleOrderedAdmin(admin.ModelAdmin):
    list_filter = ("is_active",)
    ordering = ("sort_order",)


@admin.register(SiteContact)
class SiteContactAdmin(VisibleOrderedAdmin):
    list_display = ("address", "phone_display", "email_display", "is_active")
    fieldsets = (
        (
            "Coordonnees affichees sur le site",
            {
                "description": "Modifiez ici l'adresse, les telephones et les emails visibles par les visiteurs.",
                "fields": (
                    "address",
                    "phone_display",
                    "whatsapp_number",
                    "email_display",
                    "sort_order",
                    "is_active",
                ),
            },
        ),
    )


class PropertyPhotoInline(admin.TabularInline):
    model = PropertyPhoto
    extra = 0
    fields = (
        "title",
        "image",
        "image_path",
        "alt_text",
        "sort_order",
        "is_active",
    )
    ordering = ("sort_order", "id")
    verbose_name = "photo de l'album"
    verbose_name_plural = "album photo"


@admin.register(Property)
class PropertyAdmin(VisibleOrderedAdmin):
    list_display = (
        "title",
        "transaction",
        "property_type",
        "residence",
        "district",
        "price",
        "is_active",
    )
    list_filter = ("transaction", "property_type", "residence", "district", "is_active")
    search_fields = ("title", "tag", "residence", "district", "address", "description", "unit_number")
    inlines = (PropertyPhotoInline,)
    fieldsets = (
        (
            "Ou apparait ce bien",
            {
                "fields": (
                    "transaction",
                    "property_type",
                    "sort_order",
                    "is_active",
                )
            },
        ),
        (
            "Texte de l'annonce",
            {
                "fields": (
                    "title",
                    "tag",
                    "description",
                    "cta_label",
                    "image",
                    "image_path",
                )
            },
        ),
        (
            "Informations du bien",
            {
                "fields": (
                    "residence",
                    "district",
                    "address",
                    "floor",
                    "unit_number",
                    "bedrooms",
                    "surface_total",
                    "surface_sold",
                    "mezzanine",
                    "project_label",
                    "price",
                    "price_note",
                )
            },
        ),
    )


@admin.register(PropertyPhoto)
class PropertyPhotoAdmin(VisibleOrderedAdmin):
    list_display = ("title", "property", "sort_order", "is_active")
    list_filter = ("is_active", "property__residence")
    search_fields = ("title", "property__title", "property__residence")
    autocomplete_fields = ("property",)
    fieldsets = (
        (
            "Photo affichee dans l'album du bien",
            {
                "description": "Ajoutez les photos dans l'ordre souhaite: salon, chambres, cuisine, toilette.",
                "fields": (
                    "property",
                    "title",
                    "image",
                    "image_path",
                    "alt_text",
                    "sort_order",
                    "is_active",
                ),
            },
        ),
    )


@admin.register(GuidePlace)
class GuidePlaceAdmin(VisibleOrderedAdmin):
    list_display = ("title", "section", "sort_order", "is_active")
    list_filter = ("section", "is_active")
    search_fields = ("title", "description")
    fieldsets = (
        (
            "Lieu affiche dans le guide",
            {
                "fields": (
                    "section",
                    "title",
                    "description",
                    "image",
                    "image_path",
                    "sort_order",
                    "is_active",
                )
            },
        ),
    )


@admin.register(EventIdea)
class EventIdeaAdmin(VisibleOrderedAdmin):
    list_display = ("title", "category", "sort_order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title", "category", "description", "bullet_points")
    fieldsets = (
        (
            "Idee affichee dans la page Evenement",
            {
                "description": "Les details s'affichent en liste. Mettez un detail par ligne.",
                "fields": (
                    "category",
                    "title",
                    "description",
                    "bullet_points",
                    "image",
                    "image_path",
                    "sort_order",
                    "is_active",
                ),
            },
        ),
    )


@admin.register(PurplePearlPlan)
class PurplePearlPlanAdmin(VisibleOrderedAdmin):
    list_display = ("button_label", "title", "sort_order", "is_active")
    search_fields = ("button_label", "title", "description")
    readonly_fields = ("key",)
    fieldsets = (
        (
            "Plan affiche dans Purple Pearl",
            {
                "description": "Ces plans alimentent les boutons et l'image affichee dans la section Plans.",
                "fields": (
                    "button_label",
                    "title",
                    "description",
                    "image",
                    "image_path",
                    "alt_text",
                    "sort_order",
                    "is_active",
                    "key",
                ),
            },
        ),
    )


@admin.register(Testimonial)
class TestimonialAdmin(VisibleOrderedAdmin):
    list_display = ("client_name", "rating", "details", "sort_order", "is_active")
    list_filter = ("highlight_city_center", "is_active")
    search_fields = ("client_name", "quote", "details")
    fieldsets = (
        (
            "Recommandation client",
            {
                "fields": (
                    "rating",
                    "quote",
                    "client_name",
                    "details",
                    "highlight_city_center",
                    "sort_order",
                    "is_active",
                )
            },
        ),
    )


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "project", "property_type", "created_at", "status")
    list_filter = ("status", "project", "property_type", "appointment_mode", "created_at")
    search_fields = ("full_name", "phone", "email", "message", "budget")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Suivi de la demande",
            {"fields": ("status", "created_at")},
        ),
        (
            "Coordonnees client",
            {"fields": ("full_name", "phone", "email")},
        ),
        (
            "Projet immobilier",
            {"fields": ("project", "property_type", "budget", "message")},
        ),
        (
            "Rendez-vous souhaite",
            {"fields": ("preferred_date", "preferred_time", "appointment_mode")},
        ),
    )


@admin.register(PurplePearlVisitRequest)
class PurplePearlVisitRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "visit_type", "preferred_date", "preferred_time", "created_at", "status")
    list_filter = ("status", "visit_type", "preferred_date", "created_at")
    search_fields = ("full_name", "phone", "email", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Suivi de la demande",
            {"fields": ("status", "created_at")},
        ),
        (
            "Coordonnees client",
            {"fields": ("full_name", "phone", "email", "consent")},
        ),
        (
            "Visite souhaitee",
            {"fields": ("visit_type", "preferred_date", "preferred_time", "message")},
        ),
    )


@admin.register(NewsletterSignup)
class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ("email", "source", "created_at")
    search_fields = ("email", "source")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
