from django.db import migrations


HILTON_137M2_SALE_DESCRIPTION = (
    "Découvrez cet appartement d’exception situé à Hilton Résidence à Tanger. "
    "Offrant une vue imprenable sur la Méditerranée, un cadre sécurisé et une ambiance calme et luxueuse, ce bien représente une opportunité idéale pour un investissement de qualité ou une résidence élégante au cœur de la ville. "
    "Le parking est inclus dans le prix de vente."
)

HILTON_137M2_PHOTOS = [
    ("Salon", "/assets/hilton-137m2/hilton-137m2-01-large.jpg", "Salon de l'appartement Hilton de 137 m²"),
    ("Séjour", "/assets/hilton-137m2/hilton-137m2-02-large.jpg", "Séjour de l'appartement Hilton de 137 m²"),
    ("Cuisine", "/assets/hilton-137m2/hilton-137m2-03-large.jpg", "Cuisine de l'appartement Hilton de 137 m²"),
    ("Chambre 1", "/assets/hilton-137m2/hilton-137m2-04-large.jpg", "Chambre 1 de l'appartement Hilton de 137 m²"),
    ("Chambre 2", "/assets/hilton-137m2/hilton-137m2-05-large.jpg", "Chambre 2 de l'appartement Hilton de 137 m²"),
    ("Chambre 3", "/assets/hilton-137m2/hilton-137m2-06-large.jpg", "Chambre 3 de l'appartement Hilton de 137 m²"),
    ("Toilette", "/assets/hilton-137m2/hilton-137m2-07-large.jpg", "Toilette de l'appartement Hilton de 137 m²"),
]


def publish_hilton_137m2(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")
    property_obj, _created = Property.objects.update_or_create(
        title="HILTON · 137 m²",
        transaction="sale",
        property_type="apartment",
        defaults={
            "residence": "HILTON",
            "district": "Centre-ville",
            "tag": "Centre-ville · Appartement à vendre",
            "address": "Place du Maghreb Arabe, 90000 Tanger, Maroc",
            "description": HILTON_137M2_SALE_DESCRIPTION,
            "floor": "ETAGE 09",
            "unit_number": "",
            "bedrooms": 3,
            "surface_total": 137,
            "surface_sold": "137 m²",
            "cta_label": "Demander le prix →",
            "image": None,
            "image_path": HILTON_137M2_PHOTOS[0][1],
            "sort_order": 8,
            "is_active": True,
            "is_sold": False,
            "is_rented": False,
        },
    )
    for sort_order, (photo_title, image_path, alt_text) in enumerate(
        HILTON_137M2_PHOTOS, start=1
    ):
        PropertyPhoto.objects.update_or_create(
            property=property_obj,
            title=photo_title,
            defaults={
                "image": None,
                "image_path": image_path,
                "alt_text": alt_text,
                "sort_order": sort_order,
                "is_active": True,
            },
        )


def remove_hilton_137m2(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    Property.objects.filter(
        title="HILTON · 137 m²",
        transaction="sale",
        property_type="apartment",
        image_path=HILTON_137M2_PHOTOS[0][1],
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0027_move_marina_hall_after_view"),
    ]

    operations = [
        migrations.RunPython(publish_hilton_137m2, remove_hilton_137m2),
    ]
