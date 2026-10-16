from django.db import migrations


PREVIOUS_SURFACE = "261 m² vendu"
CORRECTED_SURFACE = "261 m²"


def correct_surface(apps, schema_editor, *, reverse=False):
    Property = apps.get_model("website", "Property")
    Property.objects.using(schema_editor.connection.alias).filter(
        title="MARINA BLOC B · N°306",
        transaction="sale",
        property_type="apartment",
        surface_sold=CORRECTED_SURFACE if reverse else PREVIOUS_SURFACE,
    ).update(surface_sold=PREVIOUS_SURFACE if reverse else CORRECTED_SURFACE)


def restore_surface(apps, schema_editor):
    correct_surface(apps, schema_editor, reverse=True)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0034_correct_b2_b6_rental_statuses"),
    ]

    operations = [
        migrations.RunPython(correct_surface, restore_surface),
    ]
