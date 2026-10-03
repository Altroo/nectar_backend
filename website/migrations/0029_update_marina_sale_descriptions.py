from django.db import migrations


MARINA_SALE_DESCRIPTIONS = {
    "MARINA BLOC B · N°302": "Offrez-vous une adresse privilégiée à Tanger Marina Bay. Spacieux et baigné de lumière, cet appartement bénéficie d’une superbe vue sur la Méditerranée. Une belle occasion de concrétiser votre projet immobilier, pour y vivre, investir ou séjourner à Tanger.",
    "MARINA BLOC B · N°303": "À Tanger Marina Bay, cet appartement séduit par ses beaux volumes, sa luminosité et sa magnifique vue sur la Méditerranée. Un cadre idéal pour s’installer à Tanger ou profiter d’une résidence secondaire face à la mer.",
    "MARINA BLOC B · N°306": "Découvrez cet appartement spacieux et lumineux situé à Tanger Marina Bay. Sa vue exceptionnelle sur la Méditerranée et son emplacement privilégié en font une belle opportunité pour une résidence principale, un investissement ou un pied-à-terre à Tanger.",
}

PREVIOUS_DESCRIPTION = (
    "Blvd. Mohamed VI, Tanger. Un appartement clair et bien situé pour résidence "
    "principale, investissement ou pied-à-terre à Tanger."
)


def update_marina_descriptions(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    for title, description in MARINA_SALE_DESCRIPTIONS.items():
        Property.objects.filter(
            title=title,
            transaction="sale",
            property_type="apartment",
        ).update(description=description)


def restore_marina_descriptions(apps, _schema_editor):
    Property = apps.get_model("website", "Property")
    for title, description in MARINA_SALE_DESCRIPTIONS.items():
        Property.objects.filter(
            title=title,
            transaction="sale",
            property_type="apartment",
            description=description,
        ).update(description=PREVIOUS_DESCRIPTION)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0028_publish_hilton_137m2_sale"),
    ]

    operations = [
        migrations.RunPython(update_marina_descriptions, restore_marina_descriptions),
    ]
