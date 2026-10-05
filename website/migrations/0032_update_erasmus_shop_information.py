from django.db import migrations, models


# Erasmus tower updates.xlsx, Feuil1!A2:G14.
ERASMUS_UPDATES = [
    {
        "title": "Local A1 · ERASMUS TOWER",
        "before": {
            "surface_total": 235,
            "surface_sold": "188 m²",
            "project_label": "RDC 141 m²",
            "mezzanine": "94 m²",
        },
        "after": {
            "surface_total": 235,
            "surface_sold": "185,5 m²",
            "project_label": "RDC 136 m²",
            "mezzanine": "99 m²",
            "surface_category": "small",
            "rental_category": "A",
        },
    },
    {
        "title": "Local A2 · ERASMUS TOWER",
        "before": {
            "surface_total": 239,
            "surface_sold": "160 m²",
            "project_label": "RDC 81 m²",
            "mezzanine": "158 m²",
        },
        "after": {
            "surface_total": 210,
            "surface_sold": "166 m²",
            "project_label": "RDC 122 m²",
            "mezzanine": "88 m²",
            "surface_category": "small",
            "rental_category": "A",
        },
    },
    {
        "title": "Local A3 · ERASMUS TOWER",
        "before": {
            "surface_total": 314,
            "surface_sold": "231 m²",
            "project_label": "RDC 148 m²",
            "mezzanine": "166 m²",
        },
        "after": {
            "surface_total": 287,
            "surface_sold": "232,5 m²",
            "project_label": "RDC 178 m²",
            "mezzanine": "109 m²",
            "surface_category": "medium",
            "rental_category": "A",
        },
    },
    {
        "title": "Local A4 · ERASMUS TOWER",
        "before": {
            "surface_total": 292,
            "surface_sold": "237 m²",
            "project_label": "RDC 181 m²",
            "mezzanine": "111 m²",
        },
        "after": {
            "surface_total": 282,
            "surface_sold": "228,5 m²",
            "project_label": "RDC 175 m²",
            "mezzanine": "107 m²",
            "surface_category": "medium",
            "rental_category": "A",
        },
    },
    {
        "title": "Local A5 · ERASMUS TOWER",
        "before": {
            "surface_total": 292,
            "surface_sold": "238 m²",
            "project_label": "RDC 183 m²",
            "mezzanine": "109 m²",
        },
        "after": {
            "surface_total": 305,
            "surface_sold": "224 m²",
            "project_label": "RDC 143 m²",
            "mezzanine": "162 m²",
            "surface_category": "medium",
            "rental_category": "B",
        },
    },
    {
        "title": "Local A6 · ERASMUS TOWER",
        "before": {
            "surface_total": 213,
            "surface_sold": "170 m²",
            "project_label": "RDC 126 m²",
            "mezzanine": "87 m²",
        },
        "after": {
            "surface_total": 227,
            "surface_sold": "151,5 m²",
            "project_label": "RDC 76 m²",
            "mezzanine": "151 m²",
            "surface_category": "small",
            "rental_category": "B",
        },
    },
    {
        "title": "Local B1 · ERASMUS TOWER",
        "before": {
            "surface_total": 211,
            "surface_sold": "160 m²",
            "project_label": "RDC 108 m²",
            "mezzanine": "103 m²",
        },
        "after": {
            "surface_total": 203,
            "surface_sold": "154 m²",
            "project_label": "RDC 105 m²",
            "mezzanine": "98 m²",
            "surface_category": "small",
            "rental_category": "A",
        },
    },
    {
        "title": "Local B2 · ERASMUS TOWER",
        "before": {
            "surface_total": 270,
            "surface_sold": "219 m²",
            "project_label": "RDC 168 m²",
            "mezzanine": "102 m²",
        },
        "after": {
            "surface_total": 267,
            "surface_sold": "214 m²",
            "project_label": "RDC 161 m²",
            "mezzanine": "106 m²",
            "surface_category": "medium",
            "rental_category": "A",
        },
    },
    {
        "title": "Local B3 · ERASMUS TOWER",
        "before": {
            "surface_total": 505,
            "surface_sold": "410 m²",
            "project_label": "RDC 314 m²",
            "mezzanine": "191 m²",
        },
        "after": {
            "surface_total": 498,
            "surface_sold": "403,5 m²",
            "project_label": "RDC 309 m²",
            "mezzanine": "189 m²",
            "surface_category": "large",
            "rental_category": "A",
        },
    },
    {
        "title": "Local B4 · ERASMUS TOWER",
        "before": {
            "surface_total": 388,
            "surface_sold": "291 m²",
            "project_label": "RDC 194 m²",
            "mezzanine": "194 m²",
        },
        "after": {
            "surface_total": 379,
            "surface_sold": "284,5 m²",
            "project_label": "RDC 190 m²",
            "mezzanine": "189 m²",
            "surface_category": "large",
            "rental_category": "B",
        },
    },
    {
        "title": "Local B5 · ERASMUS TOWER",
        "before": {
            "surface_total": 262,
            "surface_sold": "199 m²",
            "project_label": "RDC 136 m²",
            "mezzanine": "126 m²",
        },
        "after": {
            "surface_total": 244,
            "surface_sold": "187,5 m²",
            "project_label": "RDC 131 m²",
            "mezzanine": "113 m²",
            "surface_category": "small",
            "rental_category": "B",
        },
    },
    {
        "title": "Local B6 · ERASMUS TOWER",
        "before": {
            "surface_total": 277,
            "surface_sold": "215 m²",
            "project_label": "RDC 152 m²",
            "mezzanine": "125 m²",
        },
        "after": {
            "surface_total": 270,
            "surface_sold": "208,5 m²",
            "project_label": "RDC 147 m²",
            "mezzanine": "123 m²",
            "surface_category": "medium",
            "rental_category": "B",
        },
    },
    {
        "title": "Local B7 · ERASMUS TOWER",
        "before": {
            "surface_total": 401,
            "surface_sold": "285 m²",
            "project_label": "RDC 168 m²",
            "mezzanine": "233 m²",
        },
        "after": {
            "surface_total": 351,
            "surface_sold": "257 m²",
            "project_label": "RDC 163 m²",
            "mezzanine": "188 m²",
            "surface_category": "large",
            "rental_category": "B",
        },
    },
]


def update_shops(apps, schema_editor, *, reverse=False):
    Property = apps.get_model("website", "Property")
    properties = Property.objects.using(schema_editor.connection.alias).filter(
        transaction="rent", property_type="commercial"
    )
    for entry in ERASMUS_UPDATES:
        values = dict(entry["before"] if reverse else entry["after"])
        if reverse:
            values.update(surface_category="", rental_category="")
        properties.filter(title=entry["title"]).update(**values)


def restore_shops(apps, schema_editor):
    update_shops(apps, schema_editor, reverse=True)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0031_update_october_2026_rental_rates"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="surface_category",
            field=models.CharField(
                blank=True,
                choices=[("small", "Petite"), ("medium", "Moyenne"), ("large", "Grande")],
                default="",
                max_length=6,
                verbose_name="categorie de surface",
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="rental_category",
            field=models.CharField(
                blank=True,
                choices=[("A", "A"), ("B", "B")],
                default="",
                max_length=1,
                verbose_name="categorie locative",
            ),
        ),
        migrations.RunPython(update_shops, restore_shops),
    ]
