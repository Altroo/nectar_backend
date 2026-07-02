from django.db import migrations, models
import django.db.models.deletion


CITY_CENTER_PHOTOS = [
    (
        "Salon",
        "/assets/city-center/city-center-salon.png",
        "Salon de l'appartement City Center",
    ),
    (
        "Séjour",
        "/assets/city-center/city-center-sejour.png",
        "Séjour de l'appartement City Center",
    ),
    (
        "Chambre 1",
        "/assets/city-center/city-center-chambre-1.png",
        "Chambre 1 de l'appartement City Center",
    ),
    (
        "Chambre 2",
        "/assets/city-center/city-center-chambre-2.png",
        "Chambre 2 de l'appartement City Center",
    ),
    (
        "Chambre 3",
        "/assets/city-center/city-center-chambre-3.png",
        "Chambre 3 de l'appartement City Center",
    ),
    (
        "Chambre 4",
        "/assets/city-center/city-center-chambre-4.png",
        "Chambre 4 de l'appartement City Center",
    ),
    (
        "Cuisine",
        "/assets/city-center/city-center-cuisine.png",
        "Cuisine de l'appartement City Center",
    ),
    (
        "Toilette 1",
        "/assets/city-center/city-center-toilette-1.png",
        "Toilette de l'appartement City Center",
    ),
    (
        "Toilette 2",
        "/assets/city-center/city-center-toilette-2.png",
        "Deuxième toilette de l'appartement City Center",
    ),
]


def seed_city_center_album(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")

    city_center = (
        Property.objects.filter(title="Appartement City Center Ra1 N°B").first()
        or Property.objects.filter(title__icontains="City Center", unit_number="N°B").first()
    )
    if not city_center:
        return

    if not city_center.image_path:
        city_center.image_path = CITY_CENTER_PHOTOS[0][1]
        city_center.save(update_fields=["image_path"])

    for index, (title, image_path, alt_text) in enumerate(CITY_CENTER_PHOTOS, start=1):
        photo, _created = PropertyPhoto.objects.get_or_create(
            property=city_center,
            title=title,
            defaults={
                "image_path": image_path,
                "alt_text": alt_text,
                "sort_order": index,
                "is_active": True,
            },
        )
        photo.image_path = image_path
        photo.alt_text = alt_text
        photo.sort_order = index
        photo.is_active = True
        photo.save()


def remove_city_center_album(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    PropertyPhoto = apps.get_model("website", "PropertyPhoto")
    city_center = Property.objects.filter(title="Appartement City Center Ra1 N°B").first()
    if city_center:
        PropertyPhoto.objects.filter(property=city_center).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PropertyPhoto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="date d'ajout",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name="derniere modification",
                    ),
                ),
                (
                    "sort_order",
                    models.PositiveIntegerField(
                        default=0,
                        help_text=(
                            "Plus le nombre est petit, plus l'element apparait haut "
                            "dans la page."
                        ),
                        verbose_name="ordre d'affichage",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Decochez pour cacher cet element sans le supprimer.",
                        verbose_name="visible sur le site",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text=(
                            "Chargez une nouvelle image si vous voulez remplacer le "
                            "visuel actuel."
                        ),
                        null=True,
                        upload_to="site/images/",
                        verbose_name="nouvelle image",
                    ),
                ),
                (
                    "image_path",
                    models.CharField(
                        blank=True,
                        help_text=(
                            "Exemple: /assets/nectar-bureau.png. Laissez vide si "
                            "vous chargez une nouvelle image."
                        ),
                        max_length=500,
                        verbose_name="image deja dans le site",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=160,
                        verbose_name="nom affiche dans l'album",
                    ),
                ),
                (
                    "alt_text",
                    models.CharField(
                        blank=True,
                        help_text="Texte court utile si l'image ne se charge pas.",
                        max_length=220,
                        verbose_name="description de la photo",
                    ),
                ),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photos",
                        to="website.property",
                        verbose_name="bien concerne",
                    ),
                ),
            ],
            options={
                "verbose_name": "photo du bien",
                "verbose_name_plural": "photos des biens",
                "ordering": ("property", "sort_order", "id"),
            },
        ),
        migrations.RunPython(seed_city_center_album, remove_city_center_album),
    ]
