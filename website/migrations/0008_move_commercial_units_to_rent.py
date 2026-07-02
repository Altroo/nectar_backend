from django.db import migrations


def move_commercial_units_to_rent(apps, _schema_editor):
    Property = apps.get_model("website", "Property")

    Property.objects.filter(
        property_type="commercial",
        transaction="rent",
        title="Locaux à louer à Tanger",
    ).delete()

    Property.objects.filter(
        property_type="commercial",
        transaction="sale",
        title__startswith="Local ",
    ).update(
        transaction="rent",
        tag="Malabata · Local commercial à louer",
        cta_label="Demander la disponibilité →",
        is_active=True,
    )


def move_commercial_units_to_sale(apps, _schema_editor):
    Property = apps.get_model("website", "Property")

    Property.objects.filter(
        property_type="commercial",
        transaction="rent",
        title__startswith="Local ",
    ).update(
        transaction="sale",
        tag="Malabata · Local commercial",
        cta_label="Demander le prix →",
        is_active=True,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0007_use_optimized_album_images"),
    ]

    operations = [
        migrations.RunPython(
            move_commercial_units_to_rent,
            move_commercial_units_to_sale,
        ),
    ]
