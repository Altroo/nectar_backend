from django.db import migrations


RENTAL_STATUSES = {
    "Local B2 · ERASMUS TOWER": False,
    "Local B6 · ERASMUS TOWER": True,
}


def update_rental_statuses(apps, schema_editor, *, reverse=False):
    Property = apps.get_model("website", "Property")
    properties = Property.objects.using(schema_editor.connection.alias).filter(
        transaction="rent", property_type="commercial"
    )
    for title, is_rented in RENTAL_STATUSES.items():
        properties.filter(title=title).update(
            is_rented=not is_rented if reverse else is_rented,
        )


def restore_rental_statuses(apps, schema_editor):
    update_rental_statuses(apps, schema_editor, reverse=True)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0033_update_erasmus_rental_statuses"),
    ]

    operations = [
        migrations.RunPython(update_rental_statuses, restore_rental_statuses),
    ]
