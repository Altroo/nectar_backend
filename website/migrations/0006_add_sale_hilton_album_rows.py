from django.db import migrations

HILTON_N11_PHOTOS = [
    (
        "Salon",
        "/assets/hilton-n11/hilton-n11-salon-large.jpg",
        "Salon de l'appartement Hilton N°11",
    ),
    (
        "Salon 2",
        "/assets/hilton-n11/hilton-n11-salon-2-large.jpg",
        "Deuxième vue du salon de l'appartement Hilton N°11",
    ),
    (
        "Meuble TV",
        "/assets/hilton-n11/hilton-n11-meuble-tv-large.jpg",
        "Meuble TV de l'appartement Hilton N°11",
    ),
    (
        "Chambre",
        "/assets/hilton-n11/hilton-n11-chambre-large.jpg",
        "Chambre de l'appartement Hilton N°11",
    ),
    (
        "Placard",
        "/assets/hilton-n11/hilton-n11-placard-large.jpg",
        "Placard de l'appartement Hilton N°11",
    ),
    (
        "Coffre-fort",
        "/assets/hilton-n11/hilton-n11-coffre-fort-large.jpg",
        "Coffre-fort de l'appartement Hilton N°11",
    ),
    (
        "Cuisine",
        "/assets/hilton-n11/hilton-n11-cuisine-large.jpg",
        "Cuisine de l'appartement Hilton N°11",
    ),
    (
        "Toilette",
        "/assets/hilton-n11/hilton-n11-toilette-large.jpg",
        "Toilette de l'appartement Hilton N°11",
    ),
]

HILTON_N13_PHOTOS = [
    (
        "Salon",
        "/assets/hilton-n13/hilton-n13-salon-large.jpg",
        "Salon de l'appartement Hilton N°13",
    ),
    (
        "Chambre 1",
        "/assets/hilton-n13/hilton-n13-chambre-1-large.jpg",
        "Chambre 1 de l'appartement Hilton N°13",
    ),
    (
        "Chambre 2",
        "/assets/hilton-n13/hilton-n13-chambre-2-large.jpg",
        "Chambre 2 de l'appartement Hilton N°13",
    ),
    (
        "Coffre-fort",
        "/assets/hilton-n13/hilton-n13-coffre-fort-large.jpg",
        "Coffre-fort de l'appartement Hilton N°13",
    ),
    (
        "Cuisine",
        "/assets/hilton-n13/hilton-n13-cuisine-large.jpg",
        "Cuisine de l'appartement Hilton N°13",
    ),
    (
        "Toilette 1",
        "/assets/hilton-n13/hilton-n13-toilette-1-large.jpg",
        "Toilette 1 de l'appartement Hilton N°13",
    ),
    (
        "Toilette 2",
        "/assets/hilton-n13/hilton-n13-toilette-2-large.jpg",
        "Toilette 2 de l'appartement Hilton N°13",
    ),
]

PROPERTY_PHOTO_ALBUMS = {
    "HILTON · N°11": HILTON_N11_PHOTOS,
    "HILTON · N°13": HILTON_N13_PHOTOS,
}


def seed_sale_hilton_albums(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    for property_title, photos in PROPERTY_PHOTO_ALBUMS.items():
        property_obj = Property.objects.filter(
            title=property_title,
            transaction="sale",
        ).first()
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


def remove_sale_hilton_albums(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    for property_title in PROPERTY_PHOTO_ALBUMS:
        property_obj = Property.objects.filter(
            title=property_title,
            transaction="sale",
        ).first()
        if property_obj:
            PropertyPhoto.objects.filter(property=property_obj).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0005_refresh_hilton_n05_and_add_n13_album"),
    ]

    operations = [
        migrations.RunPython(seed_sale_hilton_albums, remove_sale_hilton_albums),
    ]
