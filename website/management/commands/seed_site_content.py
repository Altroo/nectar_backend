from django.core.management.base import BaseCommand
from django.db.models import Q

from website.models import (
    EventIdea,
    GuidePlace,
    Property,
    PropertyPhoto,
    PurplePearlPlan,
    SiteContact,
    Testimonial,
)

CITY_CENTER_PHOTOS = [
    (
        "Salon",
        "/assets/city-center/city-center-salon-large.jpg",
        "Salon de l'appartement City Center",
    ),
    (
        "Séjour",
        "/assets/city-center/city-center-sejour-large.jpg",
        "Séjour de l'appartement City Center",
    ),
    (
        "Chambre 1",
        "/assets/city-center/city-center-chambre-1-large.jpg",
        "Chambre 1 de l'appartement City Center",
    ),
    (
        "Chambre 2",
        "/assets/city-center/city-center-chambre-2-large.jpg",
        "Chambre 2 de l'appartement City Center",
    ),
    (
        "Chambre 3",
        "/assets/city-center/city-center-chambre-3-large.jpg",
        "Chambre 3 de l'appartement City Center",
    ),
    (
        "Chambre 4",
        "/assets/city-center/city-center-chambre-4-large.jpg",
        "Chambre 4 de l'appartement City Center",
    ),
    (
        "Cuisine",
        "/assets/city-center/city-center-cuisine-large.jpg",
        "Cuisine de l'appartement City Center",
    ),
    (
        "Toilette 1",
        "/assets/city-center/city-center-toilette-1-large.jpg",
        "Toilette de l'appartement City Center",
    ),
    (
        "Toilette 2",
        "/assets/city-center/city-center-toilette-2-large.jpg",
        "Deuxième toilette de l'appartement City Center",
    ),
]

HILTON_N05_PHOTOS = [
    (
        "Salon",
        "/assets/hilton-n05/hilton-n05-salon-large.jpg",
        "Salon de l'appartement Hilton N°05",
    ),
    (
        "Chambre 1",
        "/assets/hilton-n05/hilton-n05-chambre-1-large.jpg",
        "Chambre 1 de l'appartement Hilton N°05",
    ),
    (
        "Chambre 2",
        "/assets/hilton-n05/hilton-n05-chambre-2-large.jpg",
        "Chambre 2 de l'appartement Hilton N°05",
    ),
    (
        "Coffre-fort",
        "/assets/hilton-n05/hilton-n05-coffre-fort-large.jpg",
        "Coffre-fort de l'appartement Hilton N°05",
    ),
    (
        "Cuisine",
        "/assets/hilton-n05/hilton-n05-cuisine-large.jpg",
        "Cuisine de l'appartement Hilton N°05",
    ),
    (
        "Toilette 1",
        "/assets/hilton-n05/hilton-n05-toilette-1-large.jpg",
        "Toilette 1 de l'appartement Hilton N°05",
    ),
    (
        "Toilette 2",
        "/assets/hilton-n05/hilton-n05-toilette-2-large.jpg",
        "Toilette 2 de l'appartement Hilton N°05",
    ),
]

HILTON_N13_PHOTOS = [
    (
        "Salon",
        "/assets/hilton-n13/hilton-n13-salon-large.jpg",
        "Salon de l'appartement Hilton N°13",
    ),
    (
        "Chambre 1",
        "/assets/hilton-n13/hilton-n13-chambre-1-large.jpg",
        "Chambre 1 de l'appartement Hilton N°13",
    ),
    (
        "Chambre 2",
        "/assets/hilton-n13/hilton-n13-chambre-2-large.jpg",
        "Chambre 2 de l'appartement Hilton N°13",
    ),
    (
        "Coffre-fort",
        "/assets/hilton-n13/hilton-n13-coffre-fort-large.jpg",
        "Coffre-fort de l'appartement Hilton N°13",
    ),
    (
        "Cuisine",
        "/assets/hilton-n13/hilton-n13-cuisine-large.jpg",
        "Cuisine de l'appartement Hilton N°13",
    ),
    (
        "Toilette 1",
        "/assets/hilton-n13/hilton-n13-toilette-1-large.jpg",
        "Toilette 1 de l'appartement Hilton N°13",
    ),
    (
        "Toilette 2",
        "/assets/hilton-n13/hilton-n13-toilette-2-large.jpg",
        "Toilette 2 de l'appartement Hilton N°13",
    ),
]

HILTON_N11_PHOTOS = [
    (
        "Salon",
        "/assets/hilton-n11/hilton-n11-salon-large.jpg",
        "Salon de l'appartement Hilton N°11",
    ),
    (
        "Meuble TV",
        "/assets/hilton-n11/hilton-n11-meuble-tv-large.jpg",
        "Meuble TV de l'appartement Hilton N°11",
    ),
    (
        "Chambre",
        "/assets/hilton-n11/hilton-n11-chambre-large.jpg",
        "Chambre de l'appartement Hilton N°11",
    ),
    (
        "Placard",
        "/assets/hilton-n11/hilton-n11-placard-large.jpg",
        "Placard de l'appartement Hilton N°11",
    ),
    (
        "Coffre-fort",
        "/assets/hilton-n11/hilton-n11-coffre-fort-large.jpg",
        "Coffre-fort de l'appartement Hilton N°11",
    ),
    (
        "Cuisine",
        "/assets/hilton-n11/hilton-n11-cuisine-large.jpg",
        "Cuisine de l'appartement Hilton N°11",
    ),
    (
        "Toilette",
        "/assets/hilton-n11/hilton-n11-toilette-large.jpg",
        "Toilette de l'appartement Hilton N°11",
    ),
]

HILTON_N11_12TH_PHOTOS = [
    (
        "Salon",
        "/assets/hilton-n11-12th/hilton-n11-12th-salon-large.jpg",
        "Salon de l'appartement Hilton N°11 étage 12",
    ),
    (
        "Salle à manger",
        "/assets/hilton-n11-12th/hilton-n11-12th-salle-a-manger-large.jpg",
        "Salle à manger de l'appartement Hilton N°11 étage 12",
    ),
    (
        "Chambre",
        "/assets/hilton-n11-12th/hilton-n11-12th-chambre-large.jpg",
        "Chambre de l'appartement Hilton N°11 étage 12",
    ),
    (
        "Placard",
        "/assets/hilton-n11-12th/hilton-n11-12th-placard-large.jpg",
        "Placard de l'appartement Hilton N°11 étage 12",
    ),
    (
        "Cuisine",
        "/assets/hilton-n11-12th/hilton-n11-12th-cuisine-large.jpg",
        "Cuisine de l'appartement Hilton N°11 étage 12",
    ),
    (
        "Toilette",
        "/assets/hilton-n11-12th/hilton-n11-12th-toilette-large.jpg",
        "Toilette de l'appartement Hilton N°11 étage 12",
    ),
]

MANDELSON_N47_PHOTOS = [
    (
        "Salon",
        "/assets/mandelson-n47/mandelson-n47-salon-large.jpg",
        "Salon de l'appartement Mandelson N°47",
    ),
    (
        "Salle à manger",
        "/assets/mandelson-n47/mandelson-n47-salle-a-manger-large.jpg",
        "Salle à manger de l'appartement Mandelson N°47",
    ),
    (
        "Chambre 1",
        "/assets/mandelson-n47/mandelson-n47-chambre-1-large.jpg",
        "Chambre 1 de l'appartement Mandelson N°47",
    ),
    (
        "Chambre 2",
        "/assets/mandelson-n47/mandelson-n47-chambre-2-large.jpg",
        "Chambre 2 de l'appartement Mandelson N°47",
    ),
    (
        "Balcon chambre 2",
        "/assets/mandelson-n47/mandelson-n47-balcon-chambre-2-large.jpg",
        "Balcon de la chambre 2 de l'appartement Mandelson N°47",
    ),
    (
        "Cuisine",
        "/assets/mandelson-n47/mandelson-n47-cuisine-large.jpg",
        "Cuisine de l'appartement Mandelson N°47",
    ),
    (
        "Balcon cuisine",
        "/assets/mandelson-n47/mandelson-n47-balcon-cuisine-large.jpg",
        "Balcon de la cuisine de l'appartement Mandelson N°47",
    ),
    (
        "Toilette 1",
        "/assets/mandelson-n47/mandelson-n47-toilette-1-large.jpg",
        "Toilette 1 de l'appartement Mandelson N°47",
    ),
    (
        "Toilette 2",
        "/assets/mandelson-n47/mandelson-n47-toilette-2-large.jpg",
        "Toilette 2 de l'appartement Mandelson N°47",
    ),
]

PROPERTY_PHOTO_ALBUMS = {
    "Appartement City Center Ra1 N°B": CITY_CENTER_PHOTOS,
    "Appartement Hilton N°05": HILTON_N05_PHOTOS,
    "Appartement Hilton N°11": HILTON_N11_PHOTOS,
    "Appartement Hilton N°13": HILTON_N13_PHOTOS,
    "Appartement Hilton N°11 - Etage 12": HILTON_N11_12TH_PHOTOS,
    "HILTON · N°11": HILTON_N11_PHOTOS,
    "HILTON · N°13": HILTON_N13_PHOTOS,
    "MANDELSON BLOC A · N°47": MANDELSON_N47_PHOTOS,
}

HILTON_N05_DESCRIPTION = (
    "Profitez d’un séjour élégant dans cet appartement situé au sein de l’hôtel "
    "Hilton à Tanger. Avec sa vue imprenable sur la Méditerranée, son cadre "
    "sécurisé et son ambiance calme et luxueuse, il offre l’endroit idéal pour se "
    "détendre et vivre pleinement vos vacances."
)

HILTON_N11_RENT_DESCRIPTION = (
    "Profitez d’un séjour raffiné dans cet appartement situé au sein de l’hôtel "
    "Hilton à Tanger. Offrant une vue exceptionnelle sur la Méditerranée, un "
    "cadre sécurisé et une atmosphère calme et élégante, il réunit toutes les "
    "conditions pour des vacances reposantes et mémorables."
)

HILTON_N13_RENT_DESCRIPTION = (
    "Séjournez dans un appartement élégant au cœur de l’hôtel Hilton à Tanger, "
    "où confort, sécurité et tranquillité se rencontrent. Sa vue imprenable sur "
    "la Méditerranée et son ambiance luxueuse en font l’adresse idéale pour "
    "profiter pleinement de votre séjour."
)

HILTON_N11_12TH_RENT_DESCRIPTION = (
    "Vivez une expérience unique dans cet appartement situé au sein de l’hôtel "
    "Hilton à Tanger. Entre vue panoramique sur la Méditerranée, environnement "
    "sécurisé et ambiance paisible, ce lieu vous invite à la détente dans un "
    "cadre chic et confortable."
)

HILTON_N11_SALE_DESCRIPTION = (
    "Découvrez cet appartement d’exception situé au sein de l’hôtel Hilton à "
    "Tanger. Offrant une vue imprenable sur la Méditerranée, un cadre sécurisé "
    "et une ambiance calme et luxueuse, ce bien représente une opportunité "
    "idéale pour un investissement de qualité ou une résidence élégante au cœur "
    "de la ville."
)

HILTON_N13_SALE_DESCRIPTION = (
    "À vendre, superbe appartement situé dans l’une des adresses les plus "
    "prestigieuses de Tanger, au sein de l’hôtel Hilton. Avec sa vue panoramique "
    "sur la Méditerranée, son environnement sécurisé et son cadre raffiné, ce "
    "bien allie confort, élégance et fort potentiel d’investissement."
)

CITY_CENTER_RA1_DESCRIPTION = (
    "Situé en plein centre-ville de Tanger, à proximité de la gare TGV, cet "
    "appartement offre une vue sur la ville et un cadre confortable, idéal pour "
    "un séjour pratique et agréable."
)


class Command(BaseCommand):
    help = "Ajoute le contenu de depart editable dans l'administration Nectar."

    def handle(self, *args, **options):
        contact_values = {
            "address": "Tanger, Maroc",
            "phone_display": "06 75 59 92 56 / 07 73 86 35 85",
            "whatsapp_number": "212675599256",
            "email_display": "contact@nectar.ma",
        }
        contact = SiteContact.objects.order_by("sort_order", "id").first()
        if contact:
            for key, value in contact_values.items():
                setattr(contact, key, value)
            contact.save()
        else:
            SiteContact.objects.create(**contact_values)
        self.seed_properties()
        self.seed_guide()
        self.seed_events()
        self.seed_purple_pearl()
        self.seed_testimonials()
        self.stdout.write(self.style.SUCCESS("Contenu Nectar ajoute."))

    def upsert(self, model, lookup, values):
        obj, created = model.objects.get_or_create(**lookup, defaults=values)
        if not created:
            for key, value in values.items():
                setattr(obj, key, value)
            obj.save()
        return obj

    def seed_properties(self):
        sale_apartments = [
            (
                "HILTON · N°03",
                "HILTON",
                "Centre-ville",
                "ETAGE 10",
                "N°03",
                1,
                53,
                "53 m²",
            ),
            (
                "HILTON · N°11",
                "HILTON",
                "Centre-ville",
                "ETAGE 10",
                "N°11",
                1,
                55,
                "55 m²",
            ),
            (
                "HILTON · N°13",
                "HILTON",
                "Centre-ville",
                "ETAGE 10",
                "N°13",
                2,
                74,
                "74 m²",
            ),
            (
                "MANDELSON BLOC A · N°47",
                "MANDELSON BLOC A",
                "Iberia",
                "ETAGE 06",
                "N°47",
                3,
                102,
                "102 m²",
            ),
            (
                "MARINA BLOC B · N°302",
                "MARINA BLOC B",
                "Marina",
                "ETAGE 03",
                "N°302",
                1,
                84,
                "84 m²",
            ),
            (
                "MARINA BLOC B · N°303",
                "MARINA BLOC B",
                "Marina",
                "ETAGE 03",
                "N°303",
                1,
                89,
                "89 m²",
            ),
            (
                "MARINA BLOC B · N°306",
                "MARINA BLOC B",
                "Marina",
                "ETAGE 03",
                "N°306",
                3,
                341,
                "261 m² vendu",
            ),
        ]
        hidden_sale_titles = {"HILTON · N°03"}
        sale_descriptions = {
            "HILTON · N°11": HILTON_N11_SALE_DESCRIPTION,
            "HILTON · N°13": HILTON_N13_SALE_DESCRIPTION,
        }
        for index, item in enumerate(sale_apartments, start=1):
            title, residence, district, floor, unit_number, bedrooms, surface, sold = (
                item
            )
            address = (
                "Place du Maghreb Arabe, 90000 Tanger, Maroc"
                if residence == "HILTON"
                else (
                    "Blvd. Mohamed VI, Tanger"
                    if residence.startswith("MARINA")
                    else "Place Mozart, Tanger"
                )
            )
            self.upsert(
                Property,
                {
                    "title": title,
                    "transaction": Property.SALE,
                    "property_type": Property.APARTMENT,
                },
                {
                    "tag": f"{district} · Appartement à vendre",
                    "residence": residence,
                    "district": district,
                    "address": address,
                    "description": sale_descriptions.get(
                        title,
                        f"{address}. Un appartement clair et bien situé pour résidence principale, investissement ou pied-à-terre à Tanger.",
                    ),
                    "floor": floor,
                    "unit_number": unit_number,
                    "bedrooms": bedrooms,
                    "surface_total": surface,
                    "surface_sold": sold,
                    "cta_label": "Demander le prix →",
                    "sort_order": index,
                    "is_active": title not in hidden_sale_titles,
                },
            )

        rent_apartments = [
            (
                "Appartement Hilton N°05",
                "Hilton",
                "Etage 09",
                "N°05",
                2,
                "1,400 MAD",
                1400,
            ),
            (
                "Appartement Hilton N°11",
                "Hilton",
                "Etage 10",
                "N°11",
                1,
                "1,100 MAD",
                1100,
            ),
            (
                "Appartement Hilton N°13",
                "Hilton",
                "Etage 10",
                "N°13",
                2,
                "1,400 MAD",
                1400,
            ),
            (
                "Appartement Hilton N°11 - Etage 12",
                "Hilton",
                "Etage 12",
                "N°11",
                1,
                "1,100 MAD",
                1100,
            ),
            (
                "Appartement City Center Ra1 N°B",
                "City Center Ra1",
                "Etage 05",
                "N°B",
                4,
                "1,500 MAD",
                1500,
            ),
        ]
        rent_descriptions = {
            "Appartement Hilton N°05": HILTON_N05_DESCRIPTION,
            "Appartement Hilton N°11": HILTON_N11_RENT_DESCRIPTION,
            "Appartement Hilton N°13": HILTON_N13_RENT_DESCRIPTION,
            "Appartement Hilton N°11 - Etage 12": HILTON_N11_12TH_RENT_DESCRIPTION,
            "Appartement City Center Ra1 N°B": CITY_CENTER_RA1_DESCRIPTION,
        }
        for index, item in enumerate(rent_apartments, start=101):
            title, residence, floor, unit_number, bedrooms, price, numeric_price = item
            address = (
                "Place du Maghreb Arabe, Tanger"
                if residence == "Hilton"
                else "City Center Ra1, Tanger"
            )
            property_obj = self.upsert(
                Property,
                {
                    "title": title,
                    "transaction": Property.RENT,
                    "property_type": Property.APARTMENT,
                },
                {
                    "tag": f"{residence} · {floor} · {unit_number}",
                    "residence": residence,
                    "district": "Centre-ville",
                    "address": address,
                    "description": rent_descriptions.get(
                        title,
                        f"{address}. Appartement disponible à la location, sélectionné pour un séjour confortable à Tanger.",
                    ),
                    "floor": floor,
                    "unit_number": unit_number,
                    "bedrooms": bedrooms,
                    "price": price,
                    "price_note": "Prix indiqué pour juillet.",
                    "cta_label": "Demander la disponibilité →",
                    "sort_order": index,
                    "is_active": True,
                    "surface_total": numeric_price,
                },
            )
            album_photos = PROPERTY_PHOTO_ALBUMS.get(title)
            if album_photos and not property_obj.image_path:
                property_obj.image_path = album_photos[0][1]
                property_obj.save(update_fields=["image_path"])
        self.seed_property_photo_albums()

        commercial_units = [
            ("Local A1 · ERASMUS TOWER", "A", 235, "141 m²", "94 m²", "188 m²"),
            ("Local A2 · ERASMUS TOWER", "A", 239, "81 m²", "158 m²", "160 m²"),
            ("Local A3 · ERASMUS TOWER", "A", 314, "148 m²", "166 m²", "231 m²"),
            ("Local A4 · ERASMUS TOWER", "A", 292, "181 m²", "111 m²", "237 m²"),
            ("Local A5 · ERASMUS TOWER", "A", 292, "183 m²", "109 m²", "238 m²"),
            ("Local A6 · ERASMUS TOWER", "A", 213, "126 m²", "87 m²", "170 m²"),
            ("Local B1 · ERASMUS TOWER", "B", 211, "108 m²", "103 m²", "160 m²"),
            ("Local B2 · ERASMUS TOWER", "B", 270, "168 m²", "102 m²", "219 m²"),
            ("Local B3 · ERASMUS TOWER", "B", 505, "314 m²", "191 m²", "410 m²"),
            ("Local B4 · ERASMUS TOWER", "B", 388, "194 m²", "194 m²", "291 m²"),
            ("Local B5 · ERASMUS TOWER", "B", 262, "136 m²", "126 m²", "199 m²"),
            ("Local B6 · ERASMUS TOWER", "B", 277, "152 m²", "125 m²", "215 m²"),
            ("Local B7 · ERASMUS TOWER", "B", 401, "168 m²", "233 m²", "285 m²"),
        ]
        for index, item in enumerate(commercial_units, start=201):
            title, unit_type, surface, rdc, mezzanine, total_sold = item
            self.upsert(
                Property,
                {
                    "title": title,
                    "transaction": Property.RENT,
                    "property_type": Property.COMMERCIAL,
                },
                {
                    "tag": "Malabata · Local commercial à louer",
                    "residence": "Erasmus Tower",
                    "district": "Malabata",
                    "address": "RTE MALABATA RESD ERASMUS",
                    "description": "RTE MALABATA RESD ERASMUS. Local visible et modulable, adapté showroom, commerce premium, cabinet ou activité de service.",
                    "unit_number": title.split(" · ")[0].replace("Local ", ""),
                    "bedrooms": 0,
                    "surface_total": surface,
                    "surface_sold": total_sold,
                    "mezzanine": mezzanine,
                    "project_label": f"RDC {rdc}",
                    "price_note": unit_type,
                    "cta_label": "Demander la disponibilité →",
                    "sort_order": index,
                    "is_active": True,
                },
            )

    def seed_property_photo_albums(self):
        for property_title, photos in PROPERTY_PHOTO_ALBUMS.items():
            property_obj = Property.objects.filter(title=property_title).first()
            if not property_obj:
                continue
            if not property_obj.image_path:
                property_obj.image_path = photos[0][1]
                property_obj.save(update_fields=["image_path"])
            for index, (title, image_path, alt_text) in enumerate(photos, start=1):
                self.upsert(
                    PropertyPhoto,
                    {"property": property_obj, "title": title},
                    {
                        "image_path": image_path,
                        "alt_text": alt_text,
                        "sort_order": index,
                        "is_active": True,
                    },
                )

    def seed_guide(self):
        places = [
            (
                "monuments",
                "La Kasbah de Tanger",
                "Ancien quartier fortifié en hauteur, connu pour ses ruelles, ses portes anciennes et ses vues sur la médina et le détroit.",
                "/guide-photos/monuments/la-kasbah-de-tanger.jpg",
            ),
            (
                "monuments",
                "La Médina de Tanger",
                "Le cœur ancien de la ville : souks, ruelles, maisons traditionnelles et atmosphère culturelle unique.",
                "/guide-photos/monuments/la-medina-de-tanger.jpg",
            ),
            (
                "monuments",
                "Grand Socco — Place du 9 Avril 1947",
                "Place emblématique entre la ville moderne et la médina, souvent considérée comme l’entrée du vieux Tanger.",
                "/guide-photos/monuments/grand-socco-place-9-avril-1947.jpg",
            ),
            (
                "monuments",
                "Palais de la Kasbah — Dar El Makhzen",
                "Ancien palais du sultan, aujourd’hui lié au patrimoine culturel et architectural de Tanger.",
                "/guide-photos/monuments/palais-kasbah-dar-el-makhzen.jpg",
            ),
            (
                "monuments",
                "Cap Spartel et son phare",
                "Site naturel et historique à l’entrée du détroit de Gibraltar, symbole du patrimoine maritime tangérois.",
                "/guide-photos/monuments/cap-spartel-et-son-phare.jpg",
            ),
            (
                "monuments",
                "Les Grottes d’Hercule",
                "Site mythique près du Cap Spartel, célèbre pour son ouverture naturelle donnant sur l’océan.",
                "/guide-photos/monuments/les-grottes-d-hercule.jpg",
            ),
            (
                "monuments",
                "Borj Dar El Baroud — Fortifications",
                "Ancien ouvrage défensif lié à l’histoire militaire de Tanger et à ses fortifications.",
                "/guide-photos/monuments/borj-dar-el-baroud-fortifications.jpg",
            ),
            (
                "musees",
                "Musée de la Légation américaine",
                "La Légation américaine abrite un petit musée historique qui mérite une visite, notamment pour les personnes intéressées par les relations entre le Maroc et les États-Unis à travers les siècles. Située à proximité de la médina, elle se découvre facilement lors d’un détour pendant votre visite.",
                "/guide-photos/musees/musee-legation-americaine.jpg",
            ),
            (
                "musees",
                "Musée Dar Niaba",
                "Dar Niaba est un musée historique situé dans la médina de Tanger. Il retrace une partie de l’histoire diplomatique du Maroc et met en valeur le rôle de Tanger comme lieu d’échanges entre différentes cultures.",
                "/guide-photos/musees/musee-dar-niaba.jpg",
            ),
            (
                "musees",
                "Musée de la Kasbah — Espace d’art contemporain",
                "Espace culturel dédié aux expositions temporaires, rencontres artistiques et à la création contemporaine.",
                "/guide-photos/musees/musee-kasbah-espace-art-contemporain.jpg",
            ),
            (
                "musees",
                "Musée Villa Harris",
                "Situé dans une élégante villa historique de Tanger, le Musée Villa Harris met en valeur l’art et le patrimoine culturel de la ville. Entouré d’un beau jardin, ce lieu offre aux visiteurs une expérience unique entre architecture, histoire et collections artistiques.",
                "/guide-photos/musees/musee-villa-harris.jpg",
            ),
            (
                "musees",
                "Villa Perdicaris",
                "Située au cœur du parc Perdicaris, la Villa Perdicaris est un lieu emblématique de Tanger, entouré d’une nature luxuriante et d’une atmosphère paisible. Ce site historique offre un cadre unique entre patrimoine, architecture et paysages verdoyants, idéal pour découvrir une autre facette de la ville.",
                "/guide-photos/musees/villa-perdicaris.jpg",
            ),
        ]
        for index, (section, title, description, image_path) in enumerate(
            places, start=1
        ):
            self.upsert(
                GuidePlace,
                {"title": title},
                {
                    "section": section,
                    "description": description,
                    "image_path": image_path,
                    "sort_order": index,
                    "is_active": True,
                },
            )

    def seed_events(self):
        ideas = [
            (
                "Anniversaire",
                "Birthday apartment setup",
                "Une décoration chaleureuse avec ballons, gâteau, bougies, message personnalisé et coin photo.",
                "Ballons premium et arche légère\nTable surprise avec gâteau\nMessage personnalisé au prénom",
                "/event-photos/anniversaire.jpg",
            ),
            (
                "Amoureux",
                "Romantic night",
                "Une ambiance douce pour couples : pétales, bougies LED, lumière tamisée et détails raffinés.",
                "Chemin de pétales et bougies\nPlateau gourmand ou fleurs\nOption demande / surprise",
                "/event-photos/amoureux.jpg",
            ),
            (
                "Bride to be",
                "Bridal suite decor",
                "Une mise en scène chic pour bride to be, photos entre amies et préparation avant mariage.",
                "Ballons blancs, dorés ou rose gold\nLettrage Bride to Be\nCoin photo élégant",
                "/event-photos/bride-to-be.jpg",
            ),
            (
                "Dîner privé",
                "Private dinner",
                "Une table intime dans l’appartement avec décoration florale, lumière chaude et service sur demande.",
                "Dressage de table premium\nFleurs et ambiance lumineuse\nOption chef / pâtisserie locale",
                "/event-photos/diner-prive.jpg",
            ),
        ]
        for index, (
            category,
            title,
            description,
            bullet_points,
            image_path,
        ) in enumerate(ideas, start=1):
            self.upsert(
                EventIdea,
                {"title": title},
                {
                    "category": category,
                    "description": description,
                    "bullet_points": bullet_points,
                    "image_path": image_path,
                    "sort_order": index,
                    "is_active": True,
                },
            )

    def seed_purple_pearl(self):
        old_plan_keys = [
            "general",
            "etage1",
            "etage2",
            "etage3",
            "etage4",
            "etage5",
            "etage6",
            "facades",
        ]
        old_plan_labels = [
            "1. Plan sous-sol",
            "2. Plan RDC - Locaux commerciaux",
            "3. Plan RDC haut - Locaux commerciaux",
            "3.1. Plan RDC haut - Appartements avec cour",
            "Plans des 1er, 2e, 3e et 4e étages (Appartement type 1 - 2 - 3 - 4 - 5)",
            "5. Plan 1er retrait (Appartement 1 - 2 - 3 - 4)",
            "6. Plan 2e retrait (Appartement type 1 - 2 - 3 - 4)",
            "Façades & situation",
        ]
        plans = [
            {
                "key": "facade",
                "button_label": "Façade",
                "title": "",
                "description": "",
                "image_path": "",
                "image_3d_title": "Visuel 3D",
                "image_3d_path": "/assets/purple-pearl/plans/facade-3d-jour.jpg",
                "image_3d_alt_text": "Visuel 3D",
                "image_3d_secondary_title": "Visuel 3D",
                "image_3d_secondary_path": "/assets/purple-pearl/plans/facade-3d-nuit.jpg",
                "image_3d_secondary_alt_text": "Visuel 3D",
            },
            {
                "key": "plan-coupe",
                "button_label": "Plan coupe",
                "title": "Plan coupe",
                "description": "Coupe architecturale du projet Purple Pearl.",
                "image_path": "/assets/purple-pearl/plans/plan-coupe-architectural.jpg",
                "image_3d_title": "Plan 3D",
                "image_3d_path": "/assets/purple-pearl/plans/plan-coupe-3d.jpg",
                "image_3d_secondary_title": "",
                "image_3d_secondary_path": "",
            },
            {
                "key": "plan-sous-sol",
                "button_label": "Plan sous-sol",
                "title": "Plan sous-sol",
                "description": "Plan du sous-sol du projet Purple Pearl.",
                "image_path": "/assets/purple-pearl/plans/plan-sous-sol-architectural.jpg",
                "image_3d_title": "Plan 3D",
                "image_3d_path": "/assets/purple-pearl/plans/plan-sous-sol-3d.jpg",
                "image_3d_secondary_title": "",
                "image_3d_secondary_path": "",
            },
            {
                "key": "plan-rdc-bas-magasins",
                "button_label": "RDC bas + magasins",
                "title": "RDC bas + magasins",
                "description": "Plan du RDC bas avec magasins.",
                "image_path": "/assets/purple-pearl/plans/plan-rdc-bas-magasins-architectural.jpg",
                "image_3d_title": "Plan 3D",
                "image_3d_path": "/assets/purple-pearl/plans/plan-rdc-bas-magasins-3d.jpg",
                "image_3d_secondary_title": "",
                "image_3d_secondary_path": "",
            },
            {
                "key": "plan-rdc-haut-app-mezzanine",
                "button_label": "RDC haut : Appartement + mezzanine",
                "title": "RDC haut : Appartement + mezzanine",
                "description": "Plan du RDC haut : appartement + mezzanine.",
                "image_path": "/assets/purple-pearl/plans/plan-rdc-haut-app-mezzanine-architectural.jpg",
                "image_3d_title": "Plan 3D",
                "image_3d_path": "/assets/purple-pearl/plans/plan-rdc-haut-app-mezzanine-3d.jpg",
                "image_3d_secondary_title": "",
                "image_3d_secondary_path": "",
            },
            {
                "key": "plans-etages-1-2-3-4",
                "button_label": "Étages 1, 2, 3 et 4",
                "title": "Étages 1, 2, 3 et 4",
                "description": "Plans des étages 1, 2, 3 et 4.",
                "image_path": "/assets/purple-pearl/plans/plans-etages-1-4-architectural.jpg",
                "image_3d_title": "Plan 3D",
                "image_3d_path": "/assets/purple-pearl/plans/plans-etages-1-4-3d.jpg",
                "image_3d_secondary_title": "",
                "image_3d_secondary_path": "",
            },
            {
                "key": "plan-1er-retrait",
                "button_label": "1er retrait",
                "title": "1er retrait",
                "description": "Plan du 1er retrait.",
                "image_path": "/assets/purple-pearl/plans/plan-1er-retrait-architectural.jpg",
                "image_3d_title": "Plan 3D",
                "image_3d_path": "/assets/purple-pearl/plans/plan-1er-retrait-3d.jpg",
                "image_3d_secondary_title": "",
                "image_3d_secondary_path": "",
            },
            {
                "key": "plan-2eme-retrait",
                "button_label": "2e retrait",
                "title": "2e retrait",
                "description": "Plan du 2e retrait.",
                "image_path": "/assets/purple-pearl/plans/plan-2eme-retrait-architectural.jpg",
                "image_3d_title": "Plan 3D",
                "image_3d_path": "/assets/purple-pearl/plans/plan-2eme-retrait-3d.jpg",
                "image_3d_secondary_title": "",
                "image_3d_secondary_path": "",
            },
        ]
        PurplePearlPlan.objects.filter(
            Q(key__in=old_plan_keys) | Q(button_label__in=old_plan_labels)
        ).delete()
        for index, plan in enumerate(plans, start=1):
            self.upsert(
                PurplePearlPlan,
                {"key": plan["key"]},
                {
                    "button_label": plan["button_label"],
                    "title": plan["title"],
                    "description": plan["description"],
                    "image_path": plan["image_path"],
                    "alt_text": plan["title"],
                    "image_3d_title": plan["image_3d_title"],
                    "image_3d_path": plan["image_3d_path"],
                    "image_3d_alt_text": plan.get("image_3d_alt_text", f"{plan['title']} - Plan 3D"),
                    "image_3d_secondary_title": plan["image_3d_secondary_title"],
                    "image_3d_secondary_path": plan["image_3d_secondary_path"],
                    "image_3d_secondary_alt_text": plan.get("image_3d_secondary_alt_text", plan["image_3d_secondary_title"]),
                    "sort_order": index,
                    "is_active": True,
                },
            )

    def seed_testimonials(self):
        testimonials = [
            (
                "Korkanc",
                "Turquie — Appartement Hilton 1 Chambre — 2 nuits, juillet 2025 — Couple",
                "Ceux qui souhaitent faire une réservation doivent le faire immédiatement s’ils trouvent une place.",
                False,
            ),
            (
                "Mohamed",
                "Pays-Bas — Appartement Hilton 1 Chambre — 2 nuits, novembre 2023 — Couple",
                "Emplacement de premier choix. La vue était magnifique.",
                False,
            ),
            (
                "Shéhérazade",
                "France — Appartement Hilton 1 Chambre — 2 nuits, novembre 2023 — Famille",
                "Très bel appartement décoré avec soin, la vue est exceptionnelle et la localisation idéale.",
                False,
            ),
            (
                "Elamrani",
                "Maroc — Appartement Hilton 2 Chambres — 3 nuits, décembre 2024 — Groupe",
                "Un appartement magnifique, propre et bien équipé, avec une vue superbe et un emplacement magnifique avec facilité d’accès.",
                False,
            ),
            (
                "Régine",
                "France — Appartement Hilton 2 Chambres — 3 nuits, août 2025 — Famille",
                "Très bon séjour, je recommande à 100% l’appartement. Tout était bien : propreté, accueil, je le conseille.",
                False,
            ),
            (
                "Saber",
                "Royaume-Uni — Appartement Hilton 1 Chambre — 5 nuits, juillet 2024 — Famille",
                "Great place! Great location, very clean.",
                False,
            ),
            (
                "Audrey",
                "États-Unis — Appartement Hilton 1 Chambre — 7 nuits, janvier 2026 — Couple",
                "Exceptionnel. I stayed for 7 days, it was worth the price, great place and stuff. Loved it and will return whenever I’m back in Tangier.",
                False,
            ),
            (
                "Khadija",
                "France — Apartment in City Center Tangier — 4 nuits, février 2024 — Famille",
                "Exceptionnel.",
                True,
            ),
            (
                "Ibrahim",
                "Arabie Saoudite — Apartment in City Center Tangier — 4 nuits, novembre 2023 — Groupe",
                "L’appartement est absolument magnifique, l’emplacement est superbe et proche de tous les services, et le service de Mme Hajar était extrêmement poli et courtois.",
                True,
            ),
        ]
        for index, (client_name, details, quote, city_center) in enumerate(
            testimonials, start=1
        ):
            self.upsert(
                Testimonial,
                {"client_name": client_name, "details": details},
                {
                    "rating": "10/10",
                    "quote": quote,
                    "highlight_city_center": city_center,
                    "sort_order": index,
                    "is_active": True,
                },
            )
