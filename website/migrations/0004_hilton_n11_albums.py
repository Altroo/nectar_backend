from django.db import migrations

HILTON_N11_PHOTOS = [
    (
        "Salon",
        "/assets/hilton-n11/hilton-n11-salon.png",
        "Salon de l'appartement Hilton N°11",
    ),
    (
        "Salon 2",
        "/assets/hilton-n11/hilton-n11-salon-2.png",
        "Deuxième vue du salon de l'appartement Hilton N°11",
    ),
    (
        "Meuble TV",
        "/assets/hilton-n11/hilton-n11-meuble-tv.png",
        "Meuble TV de l'appartement Hilton N°11",
    ),
    (
        "Chambre",
        "/assets/hilton-n11/hilton-n11-chambre.png",
        "Chambre de l'appartement Hilton N°11",
    ),
    (
        "Placard",
        "/assets/hilton-n11/hilton-n11-placard.png",
        "Placard de l'appartement Hilton N°11",
    ),
    (
        "Coffre-fort",
        "/assets/hilton-n11/hilton-n11-coffre-fort.png",
        "Coffre-fort de l'appartement Hilton N°11",
    ),
    (
        "Cuisine",
        "/assets/hilton-n11/hilton-n11-cuisine.png",
        "Cuisine de l'appartement Hilton N°11",
    ),
    (
        "Toilette",
        "/assets/hilton-n11/hilton-n11-toilette.png",
        "Toilette de l'appartement Hilton N°11",
    ),
]

HILTON_N11_12TH_PHOTOS = [
    (
        "Salon",
        "/assets/hilton-n11-12th/hilton-n11-12th-salon.png",
        "Salon de l'appartement Hilton N°11 étage 12",
    ),
    (
        "Salle à manger",
        "/assets/hilton-n11-12th/hilton-n11-12th-salle-a-manger.png",
        "Salle à manger de l'appartement Hilton N°11 étage 12",
    ),
    (
        "Chambre",
        "/assets/hilton-n11-12th/hilton-n11-12th-chambre.png",
        "Chambre de l'appartement Hilton N°11 étage 12",
    ),
    (
        "Placard",
        "/assets/hilton-n11-12th/hilton-n11-12th-placard.png",
        "Placard de l'appartement Hilton N°11 étage 12",
    ),
    (
        "Cuisine",
        "/assets/hilton-n11-12th/hilton-n11-12th-cuisine.png",
        "Cuisine de l'appartement Hilton N°11 étage 12",
    ),
    (
        "Toilette",
        "/assets/hilton-n11-12th/hilton-n11-12th-toilette.png",
        "Toilette de l'appartement Hilton N°11 étage 12",
    ),
]

PROPERTY_PHOTO_ALBUMS = {
    "Appartement Hilton N°11": HILTON_N11_PHOTOS,
    "Appartement Hilton N°11 - Etage 12": HILTON_N11_12TH_PHOTOS,
}


def seed_hilton_n11_albums(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    for property_title, photos in PROPERTY_PHOTO_ALBUMS.items():
        property_obj = Property.objects.filter(title=property_title).first()
        if not property_obj:
            continue

        if not property_obj.image_path:
            property_obj.image_path = photos[0][1]
            property_obj.save(update_fields=["image_path"])

        for index, (title, image_path, alt_text) in enumerate(photos, start=1):
            photo, _created = PropertyPhoto.objects.get_or_create(
                property=property_obj,
                title=title,
                defaults={
                    "image_path": image_path,
                    "alt_text": alt_text,
                    "sort_order": index,
                    "is_active": True,
                },
            )
            photo.image_path = image_path
            photo.alt_text = alt_text
            photo.sort_order = index
            photo.is_active = True
            photo.save()


def remove_hilton_n11_albums(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    for property_title, photos in PROPERTY_PHOTO_ALBUMS.items():
        property_obj = Property.objects.filter(title=property_title).first()
        if not property_obj:
            continue
        PropertyPhoto.objects.filter(
            property=property_obj,
            title__in=[title for title, _image_path, _alt_text in photos],
        ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0003_hilton_n05_album"),
    ]

    operations = [
        migrations.RunPython(seed_hilton_n11_albums, remove_hilton_n11_albums),
    ]
