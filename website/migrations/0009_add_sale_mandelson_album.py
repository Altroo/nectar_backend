from django.db import migrations

MANDELSON_N47_PHOTOS = [
    (
        "Salon",
        "/assets/mandelson-n47/mandelson-n47-salon-large.jpg",
        "Salon de l'appartement Mandelson N°47",
    ),
    (
        "Salle à manger",
        "/assets/mandelson-n47/mandelson-n47-salle-a-manger-large.jpg",
        "Salle à manger de l'appartement Mandelson N°47",
    ),
    (
        "Chambre 1",
        "/assets/mandelson-n47/mandelson-n47-chambre-1-large.jpg",
        "Chambre 1 de l'appartement Mandelson N°47",
    ),
    (
        "Chambre 2",
        "/assets/mandelson-n47/mandelson-n47-chambre-2-large.jpg",
        "Chambre 2 de l'appartement Mandelson N°47",
    ),
    (
        "Balcon chambre 2",
        "/assets/mandelson-n47/mandelson-n47-balcon-chambre-2-large.jpg",
        "Balcon de la chambre 2 de l'appartement Mandelson N°47",
    ),
    (
        "Cuisine",
        "/assets/mandelson-n47/mandelson-n47-cuisine-large.jpg",
        "Cuisine de l'appartement Mandelson N°47",
    ),
    (
        "Balcon cuisine",
        "/assets/mandelson-n47/mandelson-n47-balcon-cuisine-large.jpg",
        "Balcon de la cuisine de l'appartement Mandelson N°47",
    ),
    (
        "Toilette 1",
        "/assets/mandelson-n47/mandelson-n47-toilette-1-large.jpg",
        "Toilette 1 de l'appartement Mandelson N°47",
    ),
    (
        "Toilette 2",
        "/assets/mandelson-n47/mandelson-n47-toilette-2-large.jpg",
        "Toilette 2 de l'appartement Mandelson N°47",
    ),
]

PROPERTY_PHOTO_ALBUMS = {
    "MANDELSON BLOC A · N°47": MANDELSON_N47_PHOTOS,
}


def seed_sale_mandelson_album(apps, _schema_editor):
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


def remove_sale_mandelson_album(apps, _schema_editor):
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
        ("website", "0008_move_commercial_units_to_rent"),
    ]

    operations = [
        migrations.RunPython(seed_sale_mandelson_album, remove_sale_mandelson_album),
    ]
