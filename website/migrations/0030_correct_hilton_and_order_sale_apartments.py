from django.db import migrations


SALE_ORDER = [
    "MARINA BLOC B · N°302",
    "MARINA BLOC B · N°303",
    "MARINA BLOC B · N°306",
    "HILTON · N°03",
    "HILTON N° 1",
    "HILTON · N°11",
    "HILTON · N°13",
    "MANDELSON BLOC A · N°47",
]
PREVIOUS_ORDER = [
    "HILTON · N°03",
    "HILTON · N°11",
    "HILTON · N°13",
    "MANDELSON BLOC A · N°47",
    "MARINA BLOC B · N°302",
    "MARINA BLOC B · N°303",
    "MARINA BLOC B · N°306",
    "HILTON · 137 m²",
]


def update_listings(apps, schema_editor, *, reverse=False):
    database = schema_editor.connection.alias
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")
    sales = Property.objects.using(database).filter(
        transaction="sale", property_type="apartment"
    )
    old_title, new_title = "HILTON · 137 m²", "HILTON N° 1"
    old_alt, new_alt = "Hilton de 137 m²", "Hilton N° 1"
    if reverse:
        old_title, new_title = new_title, old_title
        old_alt, new_alt = new_alt, old_alt

    for property_obj in sales.filter(title=old_title):
        sales.filter(pk=property_obj.pk).update(
            title=new_title,
            surface_total=137 if reverse else 131,
            surface_sold="137 m²" if reverse else "131 m²",
            unit_number="" if reverse else "N° 1",
        )
        photos = PropertyPhoto.objects.using(database).filter(
            property_id=property_obj.pk, alt_text__contains=old_alt
        )
        for photo in photos:
            photos.filter(pk=photo.pk).update(
                alt_text=photo.alt_text.replace(old_alt, new_alt)
            )

    for sort_order, title in enumerate(
        PREVIOUS_ORDER if reverse else SALE_ORDER, start=1
    ):
        sales.filter(title=title).update(sort_order=sort_order)


def restore_listings(apps, schema_editor):
    update_listings(apps, schema_editor, reverse=True)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0029_update_marina_sale_descriptions"),
    ]

    operations = [
        migrations.RunPython(update_listings, restore_listings),
    ]
