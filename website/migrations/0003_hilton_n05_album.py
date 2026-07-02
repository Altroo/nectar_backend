from django.db import migrations


HILTON_N05_PHOTOS = [
    ("Salon", "/assets/hilton-n05/hilton-n05-salon.png", "Salon de l'appartement Hilton N°05"),
    ("Chambre 1", "/assets/hilton-n05/hilton-n05-chambre-1.png", "Chambre 1 de l'appartement Hilton N°05"),
    ("Chambre 2", "/assets/hilton-n05/hilton-n05-chambre-2.png", "Chambre 2 de l'appartement Hilton N°05"),
    ("Cuisine", "/assets/hilton-n05/hilton-n05-cuisine.png", "Cuisine de l'appartement Hilton N°05"),
    ("Toilette", "/assets/hilton-n05/hilton-n05-toilette.png", "Toilette de l'appartement Hilton N°05"),
]


def seed_hilton_n05_album(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    hilton_n05 = (
        Property.objects.filter(title="Appartement Hilton N°05").first()
        or Property.objects.filter(title__icontains="Hilton", unit_number="N°05").first()
    )
    if not hilton_n05:
        return

    if not hilton_n05.image_path:
        hilton_n05.image_path = HILTON_N05_PHOTOS[0][1]
        hilton_n05.save(update_fields=["image_path"])

    for index, (title, image_path, alt_text) in enumerate(HILTON_N05_PHOTOS, start=1):
        photo, _created = PropertyPhoto.objects.get_or_create(
            property=hilton_n05,
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


def remove_hilton_n05_album(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")
    hilton_n05 = Property.objects.filter(title="Appartement Hilton N°05").first()
    if hilton_n05:
        PropertyPhoto.objects.filter(
            property=hilton_n05,
            title__in=[title for title, _image_path, _alt_text in HILTON_N05_PHOTOS],
        ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0002_propertyphoto_city_center_album"),
    ]

    operations = [
        migrations.RunPython(seed_hilton_n05_album, remove_hilton_n05_album),
    ]
