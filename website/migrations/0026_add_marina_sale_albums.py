from django.db import migrations


MARINA_N302_PHOTOS = [
    ("Vue", "/assets/marina-n302/marina-n302-vue-large.jpg", "Vue depuis l'appartement Marina N°302"),
    ("Porte N°302", "/assets/marina-n302/marina-n302-porte-large.jpg", "Porte N°302 de l'appartement Marina N°302"),
    ("Salon", "/assets/marina-n302/marina-n302-salon-large.jpg", "Salon de l'appartement Marina N°302"),
    ("Hall de la résidence", "/assets/marina-n302/marina-n302-hall-large.jpg", "Hall de la résidence Marina"),
    ("Cuisine", "/assets/marina-n302/marina-n302-cuisine-large.jpg", "Cuisine de l'appartement Marina N°302"),
    ("Chambre", "/assets/marina-n302/marina-n302-chambre-large.jpg", "Chambre de l'appartement Marina N°302"),
    ("Placard", "/assets/marina-n302/marina-n302-placard-large.jpg", "Placard de l'appartement Marina N°302"),
    ("Balcon", "/assets/marina-n302/marina-n302-balcon-large.jpg", "Balcon de l'appartement Marina N°302"),
    ("Salle de bain", "/assets/marina-n302/marina-n302-salle-de-bain-large.jpg", "Salle de bain de l'appartement Marina N°302"),
    ("WC", "/assets/marina-n302/marina-n302-wc-large.jpg", "WC de l'appartement Marina N°302"),
]

MARINA_N303_PHOTOS = [
    ("Vue", "/assets/marina-n303/marina-n303-vue-large.jpg", "Vue depuis l'appartement Marina N°303"),
    ("Porte N°303", "/assets/marina-n303/marina-n303-porte-large.jpg", "Porte N°303 de l'appartement Marina N°303"),
    ("Salon", "/assets/marina-n303/marina-n303-salon-large.jpg", "Salon de l'appartement Marina N°303"),
    ("Hall de la résidence", "/assets/marina-n303/marina-n303-hall-large.jpg", "Hall de la résidence Marina"),
    ("Cuisine", "/assets/marina-n303/marina-n303-cuisine-large.jpg", "Cuisine de l'appartement Marina N°303"),
    ("Chambre", "/assets/marina-n303/marina-n303-chambre-large.jpg", "Chambre de l'appartement Marina N°303"),
    ("Placard", "/assets/marina-n303/marina-n303-placard-large.jpg", "Placard de l'appartement Marina N°303"),
    ("Toilette", "/assets/marina-n303/marina-n303-toilette-large.jpg", "Toilette de l'appartement Marina N°303"),
    ("WC", "/assets/marina-n303/marina-n303-wc-large.jpg", "WC de l'appartement Marina N°303"),
]

MARINA_N306_PHOTOS = [
    ("Vue", "/assets/marina-n306/marina-n306-vue-large.jpg", "Vue depuis l'appartement Marina N°306"),
    ("Porte N°306", "/assets/marina-n306/marina-n306-porte-large.jpg", "Porte N°306 de l'appartement Marina N°306"),
    ("Séjour", "/assets/marina-n306/marina-n306-sejour-large.jpg", "Séjour de l'appartement Marina N°306"),
    ("Salon", "/assets/marina-n306/marina-n306-salon-large.jpg", "Salon de l'appartement Marina N°306"),
    ("Hall de la résidence", "/assets/marina-n306/marina-n306-hall-large.jpg", "Hall de la résidence Marina"),
    ("Terrasse", "/assets/marina-n306/marina-n306-terrasse-large.jpg", "Terrasse de l'appartement Marina N°306"),
    ("Cuisine", "/assets/marina-n306/marina-n306-cuisine-large.jpg", "Cuisine de l'appartement Marina N°306"),
    ("Balcon cuisine", "/assets/marina-n306/marina-n306-balcon-cuisine-large.jpg", "Balcon cuisine de l'appartement Marina N°306"),
    ("Chambre parentale", "/assets/marina-n306/marina-n306-chambre-parentale-large.jpg", "Chambre parentale de l'appartement Marina N°306"),
    ("Chambre 1", "/assets/marina-n306/marina-n306-chambre-1-large.jpg", "Chambre 1 de l'appartement Marina N°306"),
    ("Chambre 2", "/assets/marina-n306/marina-n306-chambre-2-large.jpg", "Chambre 2 de l'appartement Marina N°306"),
    ("Toilette parentale", "/assets/marina-n306/marina-n306-toilette-parentale-large.jpg", "Toilette parentale de l'appartement Marina N°306"),
    ("WC 1", "/assets/marina-n306/marina-n306-wc-1-large.jpg", "WC 1 de l'appartement Marina N°306"),
    ("WC 2", "/assets/marina-n306/marina-n306-wc-2-large.jpg", "WC 2 de l'appartement Marina N°306"),
    ("WC 3", "/assets/marina-n306/marina-n306-wc-3-large.jpg", "WC 3 de l'appartement Marina N°306"),
    ("WC", "/assets/marina-n306/marina-n306-wc-large.jpg", "WC de l'appartement Marina N°306"),
]


MARINA_PHOTO_ALBUMS = {
    "MARINA BLOC B · N°302": MARINA_N302_PHOTOS,
    "MARINA BLOC B · N°303": MARINA_N303_PHOTOS,
    "MARINA BLOC B · N°306": MARINA_N306_PHOTOS,
}


def add_marina_sale_albums(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    for property_title, photos in MARINA_PHOTO_ALBUMS.items():
        property_obj = Property.objects.filter(
            title=property_title,
            transaction="sale",
            property_type="apartment",
        ).first()
        if not property_obj:
            continue

        for sort_order, (title, image_path, alt_text) in enumerate(photos, start=1):
            PropertyPhoto.objects.update_or_create(
                property=property_obj,
                title=title,
                defaults={
                    "image": None,
                    "image_path": image_path,
                    "alt_text": alt_text,
                    "sort_order": sort_order,
                    "is_active": True,
                },
            )

        property_obj.image = None
        property_obj.image_path = photos[0][1]
        property_obj.save(update_fields=["image", "image_path"])


def remove_marina_sale_albums(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    for property_title, photos in MARINA_PHOTO_ALBUMS.items():
        property_obj = Property.objects.filter(
            title=property_title,
            transaction="sale",
            property_type="apartment",
        ).first()
        if not property_obj:
            continue

        PropertyPhoto.objects.filter(
            property=property_obj,
            image_path__in=[image_path for _title, image_path, _alt_text in photos],
        ).delete()
        if property_obj.image_path == photos[0][1]:
            property_obj.image_path = ""
            property_obj.save(update_fields=["image_path"])


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0025_property_is_rented"),
    ]

    operations = [
        migrations.RunPython(add_marina_sale_albums, remove_marina_sale_albums),
    ]
