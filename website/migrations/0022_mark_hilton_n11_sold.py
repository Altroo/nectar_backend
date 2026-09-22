from django.db import migrations


HILTON_N11_PROPERTIES = (
    ("HILTON · N°11", "sale", "ETAGE 10"),
    ("Appartement Hilton N°11", "rent", "Etage 10"),
)


def set_hilton_n11_sold(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    for title, transaction, floor in HILTON_N11_PROPERTIES:
        Property.objects.filter(
            title=title,
            transaction=transaction,
            property_type="apartment",
            floor=floor,
        ).update(is_sold=True, is_active=True)


def set_hilton_n11_available(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    for title, transaction, floor in HILTON_N11_PROPERTIES:
        Property.objects.filter(
            title=title,
            transaction=transaction,
            property_type="apartment",
            floor=floor,
        ).update(is_sold=False)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0021_property_is_sold"),
    ]

    operations = [
        migrations.RunPython(set_hilton_n11_sold, set_hilton_n11_available),
    ]
