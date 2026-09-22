from django.db import migrations


HILTON_N13_TITLE = "HILTON · N°13"


def set_hilton_n13_sold(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    Property.objects.filter(
        title=HILTON_N13_TITLE,
        transaction="sale",
        property_type="apartment",
        floor="ETAGE 10",
    ).update(is_sold=True, is_active=True)


def set_hilton_n13_available(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    Property.objects.filter(
        title=HILTON_N13_TITLE,
        transaction="sale",
        property_type="apartment",
        floor="ETAGE 10",
    ).update(is_sold=False)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0022_mark_hilton_n11_sold"),
    ]

    operations = [
        migrations.RunPython(set_hilton_n13_sold, set_hilton_n13_available),
    ]
