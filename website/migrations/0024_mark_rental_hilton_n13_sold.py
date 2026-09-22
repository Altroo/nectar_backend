from django.db import migrations


HILTON_N13_RENTAL_TITLE = "Appartement Hilton N°13"


def set_rental_hilton_n13_sold(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    Property.objects.filter(
        title=HILTON_N13_RENTAL_TITLE,
        transaction="rent",
        property_type="apartment",
        floor="Etage 10",
    ).update(is_sold=True, is_active=True)


def set_rental_hilton_n13_available(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    Property.objects.filter(
        title=HILTON_N13_RENTAL_TITLE,
        transaction="rent",
        property_type="apartment",
        floor="Etage 10",
    ).update(is_sold=False)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0023_mark_hilton_n13_sold"),
    ]

    operations = [
        migrations.RunPython(
            set_rental_hilton_n13_sold,
            set_rental_hilton_n13_available,
        ),
    ]
