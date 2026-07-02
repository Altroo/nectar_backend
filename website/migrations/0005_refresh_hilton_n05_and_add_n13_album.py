from django.db import migrations

HILTON_N05_PHOTOS = [
    (
        "Salon",
        "/assets/hilton-n05/hilton-n05-salon.png",
        "Salon de l'appartement Hilton N°05",
    ),
    (
        "Chambre 1",
        "/assets/hilton-n05/hilton-n05-chambre-1.png",
        "Chambre 1 de l'appartement Hilton N°05",
    ),
    (
        "Chambre 2",
        "/assets/hilton-n05/hilton-n05-chambre-2.png",
        "Chambre 2 de l'appartement Hilton N°05",
    ),
    (
        "Coffre-fort",
        "/assets/hilton-n05/hilton-n05-coffre-fort.png",
        "Coffre-fort de l'appartement Hilton N°05",
    ),
    (
        "Cuisine",
        "/assets/hilton-n05/hilton-n05-cuisine.png",
        "Cuisine de l'appartement Hilton N°05",
    ),
    (
        "Toilette 1",
        "/assets/hilton-n05/hilton-n05-toilette-1.png",
        "Toilette 1 de l'appartement Hilton N°05",
    ),
    (
        "Toilette 2",
        "/assets/hilton-n05/hilton-n05-toilette-2.png",
        "Toilette 2 de l'appartement Hilton N°05",
    ),
]

HILTON_N13_PHOTOS = [
    (
        "Salon",
        "/assets/hilton-n13/hilton-n13-salon.png",
        "Salon de l'appartement Hilton N°13",
    ),
    (
        "Chambre 1",
        "/assets/hilton-n13/hilton-n13-chambre-1.png",
        "Chambre 1 de l'appartement Hilton N°13",
    ),
    (
        "Chambre 2",
        "/assets/hilton-n13/hilton-n13-chambre-2.png",
        "Chambre 2 de l'appartement Hilton N°13",
    ),
    (
        "Coffre-fort",
        "/assets/hilton-n13/hilton-n13-coffre-fort.png",
        "Coffre-fort de l'appartement Hilton N°13",
    ),
    (
        "Cuisine",
        "/assets/hilton-n13/hilton-n13-cuisine.png",
        "Cuisine de l'appartement Hilton N°13",
    ),
    (
        "Toilette 1",
        "/assets/hilton-n13/hilton-n13-toilette-1.png",
        "Toilette 1 de l'appartement Hilton N°13",
    ),
    (
        "Toilette 2",
        "/assets/hilton-n13/hilton-n13-toilette-2.png",
        "Toilette 2 de l'appartement Hilton N°13",
    ),
]

PROPERTY_PHOTO_ALBUMS = {
    "Appartement Hilton N°05": HILTON_N05_PHOTOS,
    "Appartement Hilton N°13": HILTON_N13_PHOTOS,
}


def seed_refreshed_albums(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    for property_title, photos in PROPERTY_PHOTO_ALBUMS.items():
        property_obj = Property.objects.filter(title=property_title).first()
        if not property_obj:
            continue

        PropertyPhoto.objects.filter(property=property_obj).delete()
        property_obj.image_path = photos[0][1]
        property_obj.save(update_fields=["image_path"])

        for index, (title, image_path, alt_text) in enumerate(photos, start=1):
            PropertyPhoto.objects.create(
                property=property_obj,
                title=title,
                image_path=image_path,
                alt_text=alt_text,
                sort_order=index,
                is_active=True,
            )


def remove_refreshed_albums(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    for property_title in PROPERTY_PHOTO_ALBUMS:
        property_obj = Property.objects.filter(title=property_title).first()
        if property_obj:
            PropertyPhoto.objects.filter(property=property_obj).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0004_hilton_n11_albums"),
    ]

    operations = [
        migrations.RunPython(seed_refreshed_albums, remove_refreshed_albums),
    ]
