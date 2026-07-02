from django.db import migrations

ALBUM_ASSET_PREFIXES = (
    "/assets/city-center/",
    "/assets/hilton-n05/",
    "/assets/hilton-n11/",
    "/assets/hilton-n11-12th/",
    "/assets/hilton-n13/",
)


def is_album_asset(image_path):
    return any(image_path.startswith(prefix) for prefix in ALBUM_ASSET_PREFIXES)


def to_large_image(image_path):
    if is_album_asset(image_path) and image_path.endswith(".png"):
        return f"{image_path[:-4]}-large.jpg"
    return image_path


def to_original_png(image_path):
    if is_album_asset(image_path) and image_path.endswith("-large.jpg"):
        return f"{image_path[:-10]}.png"
    return image_path


def update_image_paths(apps, converter):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    for model in (Property, PropertyPhoto):
        for obj in model.objects.exclude(image_path="").iterator():
            next_image_path = converter(obj.image_path)
            if next_image_path != obj.image_path:
                obj.image_path = next_image_path
                obj.save(update_fields=["image_path"])


def use_optimized_album_images(apps, _schema_editor):
    update_image_paths(apps, to_large_image)


def restore_original_album_images(apps, _schema_editor):
    update_image_paths(apps, to_original_png)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0006_add_sale_hilton_album_rows"),
    ]

    operations = [
        migrations.RunPython(use_optimized_album_images, restore_original_album_images),
    ]
