from django.db import migrations


HILTON_N03_DESCRIPTION = (
    "À vendre, superbe appartement situé au 10ᵉ étage de la résidence Hilton, "
    "l’une des adresses les plus prestigieuses de Tanger. Offrant une vue "
    "panoramique exceptionnelle sur la Méditerranée, ce bien bénéficie d’un "
    "environnement sécurisé et d’un cadre élégant. Il constitue une excellente "
    "opportunité pour y vivre ou réaliser un investissement immobilier de qualité."
)

HILTON_N03_PHOTOS = [
    (
        "Salon",
        "/assets/hilton-n03/hilton-n03-salon-large.jpg",
        "Salon de l'appartement Hilton N°03",
    ),
    (
        "Meuble TV",
        "/assets/hilton-n03/hilton-n03-meuble-tv-large.jpg",
        "Meuble TV de l'appartement Hilton N°03",
    ),
    (
        "Chambre",
        "/assets/hilton-n03/hilton-n03-chambre-large.jpg",
        "Chambre de l'appartement Hilton N°03",
    ),
    (
        "Placard",
        "/assets/hilton-n03/hilton-n03-placard-large.jpg",
        "Placard de l'appartement Hilton N°03",
    ),
    (
        "Coffre-fort",
        "/assets/hilton-n03/hilton-n03-coffre-fort-large.jpg",
        "Coffre-fort de l'appartement Hilton N°03",
    ),
    (
        "Cuisine",
        "/assets/hilton-n03/hilton-n03-cuisine-large.jpg",
        "Cuisine de l'appartement Hilton N°03",
    ),
    (
        "Toilette",
        "/assets/hilton-n03/hilton-n03-toilette-large.jpg",
        "Toilette de l'appartement Hilton N°03",
    ),
    (
        "Vue",
        "/assets/hilton-n03/hilton-n03-vue-large.jpg",
        "Vue sur la Méditerranée depuis l'appartement Hilton N°03",
    ),
]


def publish_hilton_n03(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    property_obj = Property.objects.filter(
        title="HILTON · N°03",
        transaction="sale",
        property_type="apartment",
    ).first()
    if not property_obj:
        return

    PropertyPhoto.objects.filter(property=property_obj).delete()
    for sort_order, (title, image_path, alt_text) in enumerate(
        HILTON_N03_PHOTOS, start=1
    ):
        PropertyPhoto.objects.create(
            property=property_obj,
            title=title,
            image_path=image_path,
            alt_text=alt_text,
            sort_order=sort_order,
            is_active=True,
        )

    property_obj.description = HILTON_N03_DESCRIPTION
    property_obj.image = None
    property_obj.image_path = HILTON_N03_PHOTOS[0][1]
    property_obj.is_active = True
    property_obj.save(
        update_fields=["description", "image", "image_path", "is_active"]
    )


def hide_hilton_n03(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    property_obj = Property.objects.filter(
        title="HILTON · N°03",
        transaction="sale",
        property_type="apartment",
    ).first()
    if not property_obj:
        return

    PropertyPhoto.objects.filter(property=property_obj).delete()
    property_obj.image_path = ""
    property_obj.is_active = False
    property_obj.save(update_fields=["image_path", "is_active"])


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0019_replace_erasmus_local_photos"),
    ]

    operations = [
        migrations.RunPython(publish_hilton_n03, hide_hilton_n03),
    ]
