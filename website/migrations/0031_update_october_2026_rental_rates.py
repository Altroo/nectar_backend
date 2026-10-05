from django.db import migrations


RENTAL_RATES = {
    ("Appartement Hilton N°05", "Etage 09"): ("1,400 MAD", 1400, "1 300 DH", 1300),
    ("Appartement Hilton N°11 - Etage 12", "Etage 12"): ("1,100 MAD", 1100, "900 DH", 900),
}
CURRENT_NOTE = "Prix indiqué pour octobre 2026."
PREVIOUS_NOTE = "Prix indiqué pour juillet."


def update_rates(apps, schema_editor, *, reverse=False):
    Property = apps.get_model("website", "Property")
    for (title, floor), (old_price, old_numeric, new_price, new_numeric) in RENTAL_RATES.items():
        Property.objects.using(schema_editor.connection.alias).filter(
            title=title,
            floor=floor,
            transaction="rent",
            property_type="apartment",
        ).update(
            price=old_price if reverse else new_price,
            surface_total=old_numeric if reverse else new_numeric,
            price_note=PREVIOUS_NOTE if reverse else CURRENT_NOTE,
        )


def restore_rates(apps, schema_editor):
    update_rates(apps, schema_editor, reverse=True)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0030_correct_hilton_and_order_sale_apartments"),
    ]

    operations = [
        migrations.RunPython(update_rates, restore_rates),
    ]
