from django.db import migrations, models


MANDELSON_TITLE = "MANDELSON BLOC A · N°47"


def mark_mandelson_sold(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    Property.objects.filter(
        title=MANDELSON_TITLE,
        transaction="sale",
        property_type="apartment",
    ).update(is_sold=True, is_active=True)


def mark_mandelson_available(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    Property.objects.filter(
        title=MANDELSON_TITLE,
        transaction="sale",
        property_type="apartment",
    ).update(is_sold=False)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0020_publish_hilton_n03_sale"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="is_sold",
            field=models.BooleanField(
                default=False,
                help_text="Cochez pour conserver le bien visible sur le site avec la mention Vendu.",
                verbose_name="vendu",
            ),
        ),
        migrations.RunPython(mark_mandelson_sold, mark_mandelson_available),
    ]
