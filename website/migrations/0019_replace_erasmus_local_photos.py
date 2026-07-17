from django.db import migrations


def replace_erasmus_local_photos(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    properties = Property.objects.filter(
        transaction="rent",
        property_type="commercial",
        title__contains="ERASMUS TOWER",
    )

    for property_obj in properties:
        unit_code = property_obj.unit_number or property_obj.title.split(" · ")[0].replace(
            "Local ", ""
        )
        image_path = f"/assets/erasmus/units/{unit_code.upper()}.jpg"

        PropertyPhoto.objects.filter(property=property_obj).delete()
        PropertyPhoto.objects.create(
            property=property_obj,
            title=f"Local {unit_code.upper()}",
            image_path=image_path,
            alt_text=f"Local {unit_code.upper()} · Erasmus Tower",
            sort_order=1,
            is_active=True,
        )

        property_obj.image_path = image_path
        property_obj.image = None
        property_obj.save(update_fields=["image_path", "image"])


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0018_add_erasmus_local_photos"),
    ]

    operations = [
        migrations.RunPython(replace_erasmus_local_photos, migrations.RunPython.noop),
    ]
