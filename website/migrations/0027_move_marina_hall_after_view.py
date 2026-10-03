from django.db import migrations


MARINA_PREVIOUS_HALL_POSITIONS = {
    "MARINA BLOC B · N°302": 4,
    "MARINA BLOC B · N°303": 4,
    "MARINA BLOC B · N°306": 5,
}


def reorder_hall_photos(apps, positions):
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")
    for property_title, position in positions.items():
        photos = list(
            PropertyPhoto.objects.filter(
                property__title=property_title,
                property__transaction="sale",
                property__property_type="apartment",
            ).order_by("sort_order", "id")
        )
        view = next((photo for photo in photos if photo.title == "Vue"), None)
        hall = next(
            (photo for photo in photos if photo.title == "Hall de la résidence"),
            None,
        )
        if view is None or hall is None:
            continue

        ordered = [view] + [photo for photo in photos if photo not in (view, hall)]
        ordered.insert(position - 1, hall)
        for sort_order, photo in enumerate(ordered, start=1):
            photo.sort_order = sort_order
        PropertyPhoto.objects.bulk_update(ordered, ["sort_order"])


def move_marina_hall_after_view(apps, _schema_editor):
    reorder_hall_photos(
        apps, {title: 2 for title in MARINA_PREVIOUS_HALL_POSITIONS}
    )


def restore_marina_hall_positions(apps, _schema_editor):
    reorder_hall_photos(apps, MARINA_PREVIOUS_HALL_POSITIONS)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0026_add_marina_sale_albums"),
    ]

    operations = [
        migrations.RunPython(
            move_marina_hall_after_view, restore_marina_hall_positions
        ),
    ]
