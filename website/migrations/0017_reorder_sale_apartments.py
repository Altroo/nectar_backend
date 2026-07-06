from django.db import migrations


SALE_APARTMENT_ORDER = {
    "HILTON · N°03": 1,
    "HILTON · N°11": 2,
    "HILTON · N°13": 3,
    "MANDELSON BLOC A · N°47": 4,
    "MARINA BLOC B · N°302": 5,
    "MARINA BLOC B · N°303": 6,
    "MARINA BLOC B · N°306": 7,
}


def reorder_sale_apartments(apps, schema_editor):
    Property = apps.get_model("website", "Property")
    for title, sort_order in SALE_APARTMENT_ORDER.items():
        Property.objects.filter(
            title=title,
            transaction="sale",
            property_type="apartment",
        ).update(sort_order=sort_order)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0016_alter_sitecontact_email_display"),
    ]

    operations = [
        migrations.RunPython(reorder_sale_apartments, migrations.RunPython.noop),
    ]
