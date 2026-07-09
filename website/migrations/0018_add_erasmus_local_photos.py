from django.db import migrations


ERASMUS_LOCAL_PHOTOS = [
    (
        "Pharmacie",
        "/assets/erasmus/erasmus-pharmacie-large.jpg",
        "Local Erasmus Tower amenage en pharmacie",
    ),
    (
        "Salon de coiffure",
        "/assets/erasmus/erasmus-salon-coiffure-large.jpg",
        "Local Erasmus Tower amenage en salon de coiffure",
    ),
    (
        "Opticien",
        "/assets/erasmus/erasmus-opticien-large.jpg",
        "Local Erasmus Tower amenage en opticien",
    ),
    (
        "Chocolaterie",
        "/assets/erasmus/erasmus-chocolaterie-large.jpg",
        "Local Erasmus Tower amenage en chocolaterie",
    ),
    (
        "Patisserie",
        "/assets/erasmus/erasmus-patisserie-large.jpg",
        "Local Erasmus Tower amenage en patisserie",
    ),
    (
        "Mini market",
        "/assets/erasmus/erasmus-mini-market-large.jpg",
        "Local Erasmus Tower amenage en mini market",
    ),
]

ERASMUS_PHOTO_STARTS = (0, 3, 1, 5, 2, 4, 3, 0, 5, 1, 4, 2, 0)


def erasmus_album_for(index):
    start = ERASMUS_PHOTO_STARTS[index % len(ERASMUS_PHOTO_STARTS)]
    return [
        ERASMUS_LOCAL_PHOTOS[(start + offset) % len(ERASMUS_LOCAL_PHOTOS)]
        for offset in range(len(ERASMUS_LOCAL_PHOTOS))
    ]


def add_erasmus_local_photos(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    properties = list(
        Property.objects.filter(
            transaction="rent",
            property_type="commercial",
            title__contains="ERASMUS TOWER",
        ).order_by("sort_order", "title", "id")
    )

    for property_index, property_obj in enumerate(properties):
        photos = erasmus_album_for(property_index)
        PropertyPhoto.objects.filter(
            property=property_obj,
            image_path__startswith="/assets/erasmus/",
        ).delete()

        property_obj.image_path = photos[0][1]
        property_obj.save(update_fields=["image_path"])

        for sort_order, (title, image_path, alt_text) in enumerate(photos, start=1):
            PropertyPhoto.objects.create(
                property=property_obj,
                title=title,
                image_path=image_path,
                alt_text=alt_text,
                sort_order=sort_order,
                is_active=True,
            )


def remove_erasmus_local_photos(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    properties = Property.objects.filter(
        transaction="rent",
        property_type="commercial",
        title__contains="ERASMUS TOWER",
    )
    PropertyPhoto.objects.filter(
        property__in=properties,
        image_path__startswith="/assets/erasmus/",
    ).delete()
    properties.filter(image_path__startswith="/assets/erasmus/").update(image_path="")


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0017_reorder_sale_apartments"),
    ]

    operations = [
        migrations.RunPython(add_erasmus_local_photos, remove_erasmus_local_photos),
    ]
