from django.db import migrations, models


RENTED_COMMERCIAL_TITLES = (
    "Local A4 · ERASMUS TOWER",
    "Local A5 · ERASMUS TOWER",
    "Local B6 · ERASMUS TOWER",
)


def mark_commercial_units_rented(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    Property.objects.filter(
        title__in=RENTED_COMMERCIAL_TITLES,
        transaction="rent",
        property_type="commercial",
    ).update(is_rented=True, is_active=True)


def mark_commercial_units_available(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    Property.objects.filter(
        title__in=RENTED_COMMERCIAL_TITLES,
        transaction="rent",
        property_type="commercial",
    ).update(is_rented=False)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0024_mark_rental_hilton_n13_sold"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="is_rented",
            field=models.BooleanField(
                default=False,
                help_text="Cochez pour conserver le bien visible sur le site avec la mention Loue.",
                verbose_name="loue",
            ),
        ),
        migrations.RunPython(
            mark_commercial_units_rented,
            mark_commercial_units_available,
        ),
    ]
