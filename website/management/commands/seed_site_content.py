from django.core.management.base import BaseCommand

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
    ("Salon", "/assets/city-center/city-center-salon.png", "Salon de l'appartement City Center"),
    ("Séjour", "/assets/city-center/city-center-sejour.png", "Séjour de l'appartement City Center"),
    ("Chambre 1", "/assets/city-center/city-center-chambre-1.png", "Chambre 1 de l'appartement City Center"),
    ("Chambre 2", "/assets/city-center/city-center-chambre-2.png", "Chambre 2 de l'appartement City Center"),
    ("Chambre 3", "/assets/city-center/city-center-chambre-3.png", "Chambre 3 de l'appartement City Center"),
    ("Chambre 4", "/assets/city-center/city-center-chambre-4.png", "Chambre 4 de l'appartement City Center"),
    ("Cuisine", "/assets/city-center/city-center-cuisine.png", "Cuisine de l'appartement City Center"),
    ("Toilette 1", "/assets/city-center/city-center-toilette-1.png", "Toilette de l'appartement City Center"),
    ("Toilette 2", "/assets/city-center/city-center-toilette-2.png", "Deuxième toilette de l'appartement City Center"),
]


class Command(BaseCommand):
    help = "Ajoute le contenu de depart editable dans l'administration Nectar."

    def handle(self, *args, **options):
        SiteContact.objects.get_or_create(
            defaults={
                "address": "Tanger, Maroc",
                "phone_display": "06 75 59 92 56 / 07 73 86 35 85",
                "whatsapp_number": "212675599256",
                "email_display": "info@nectar.ma / contact@nectar.ma",
            }
        )
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
            ("HILTON · N°03", "HILTON", "Centre-ville", "ETAGE 10", "N°03", 1, 53, "53 m²"),
            ("HILTON · N°11", "HILTON", "Centre-ville", "ETAGE 10", "N°11", 1, 55, "55 m²"),
            ("HILTON · N°13", "HILTON", "Centre-ville", "ETAGE 10", "N°13", 2, 74, "74 m²"),
            ("MARINA BLOC B · N°302", "MARINA BLOC B", "Marina", "ETAGE 03", "N°302", 1, 84, "84 m²"),
            ("MARINA BLOC B · N°303", "MARINA BLOC B", "Marina", "ETAGE 03", "N°303", 1, 89, "89 m²"),
            ("MARINA BLOC B · N°306", "MARINA BLOC B", "Marina", "ETAGE 03", "N°306", 3, 341, "261 m² vendu"),
            ("MANDELSON BLOC A · N°47", "MANDELSON BLOC A", "Iberia", "ETAGE 06", "N°47", 3, 102, "102 m²"),
        ]
        for index, item in enumerate(sale_apartments, start=1):
            title, residence, district, floor, unit_number, bedrooms, surface, sold = item
            address = "Place du Maghreb Arabe, 90000 Tanger, Maroc" if residence == "HILTON" else "Blvd. Mohamed VI, Tanger" if residence.startswith("MARINA") else "Place Mozart, Tanger"
            self.upsert(
                Property,
                {"title": title, "transaction": Property.SALE, "property_type": Property.APARTMENT},
                {
                    "tag": f"{district} · Appartement à vendre",
                    "residence": residence,
                    "district": district,
                    "address": address,
                    "description": f"{address}. Un appartement clair et bien situé pour résidence principale, investissement ou pied-à-terre à Tanger.",
                    "floor": floor,
                    "unit_number": unit_number,
                    "bedrooms": bedrooms,
                    "surface_total": surface,
                    "surface_sold": sold,
                    "cta_label": "Demander le prix →",
                    "sort_order": index,
                    "is_active": True,
                },
            )

        rent_apartments = [
            ("Appartement Hilton N°05", "Hilton", "Etage 09", "N°05", 2, "1,400 MAD", 1400),
            ("Appartement Hilton N°11", "Hilton", "Etage 10", "N°11", 1, "1,100 MAD", 1100),
            ("Appartement Hilton N°13", "Hilton", "Etage 10", "N°13", 2, "1,400 MAD", 1400),
            ("Appartement Hilton N°11 - Etage 12", "Hilton", "Etage 12", "N°11", 1, "1,100 MAD", 1100),
            ("Appartement City Center Ra1 N°B", "City Center Ra1", "Etage 05", "N°B", 4, "1,500 MAD", 1500),
        ]
        for index, item in enumerate(rent_apartments, start=101):
            title, residence, floor, unit_number, bedrooms, price, numeric_price = item
            address = "Place du Maghreb Arabe, Tanger" if residence == "Hilton" else "City Center Ra1, Tanger"
            property_obj = self.upsert(
                Property,
                {"title": title, "transaction": Property.RENT, "property_type": Property.APARTMENT},
                {
                    "tag": f"{residence} · {floor} · {unit_number}",
                    "residence": residence,
                    "district": "Centre-ville",
                    "address": address,
                    "description": f"{address}. Appartement disponible à la location, sélectionné pour un séjour confortable à Tanger.",
                    "floor": floor,
                    "unit_number": unit_number,
                    "bedrooms": bedrooms,
                    "price": price,
                    "price_note": "Prix indiqué pour juin.",
                    "cta_label": "Demander la disponibilité →",
                    "sort_order": index,
                    "is_active": True,
                    "surface_total": numeric_price,
                },
            )
            if "City Center" in title and not property_obj.image_path:
                property_obj.image_path = CITY_CENTER_PHOTOS[0][1]
                property_obj.save(update_fields=["image_path"])
        self.seed_city_center_photos()

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
                {"title": title, "transaction": Property.SALE, "property_type": Property.COMMERCIAL},
                {
                    "tag": "Malabata · Local commercial",
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
                    "cta_label": "Demander le prix →",
                    "sort_order": index,
                    "is_active": True,
                },
            )

        self.upsert(
            Property,
            {"title": "Locaux à louer à Tanger", "transaction": Property.RENT, "property_type": Property.COMMERCIAL},
            {
                "tag": "Location · Local",
                "district": "Malabata, Centre-ville",
                "description": "Une page dédiée aux demandes de locaux à louer : boutiques, bureaux, showrooms ou espaces commerciaux.",
                "project_label": "Commerce / bureau",
                "cta_label": "Faire une demande →",
                "sort_order": 301,
                "is_active": True,
            },
        )

    def seed_city_center_photos(self):
        city_center = Property.objects.filter(title="Appartement City Center Ra1 N°B").first()
        if not city_center:
            return
        if not city_center.image_path:
            city_center.image_path = CITY_CENTER_PHOTOS[0][1]
            city_center.save(update_fields=["image_path"])
        for index, (title, image_path, alt_text) in enumerate(CITY_CENTER_PHOTOS, start=1):
            self.upsert(
                PropertyPhoto,
                {"property": city_center, "title": title},
                {
                    "image_path": image_path,
                    "alt_text": alt_text,
                    "sort_order": index,
                    "is_active": True,
                },
            )

    def seed_guide(self):
        places = [
            ("monuments", "La Kasbah de Tanger", "Ancien quartier fortifié en hauteur, connu pour ses ruelles, ses portes anciennes et ses vues sur la médina et le détroit.", "/guide-photos/kasbah-fortifications.png"),
            ("monuments", "La Médina de Tanger", "Le cœur ancien de la ville : souks, ruelles, maisons traditionnelles et atmosphère culturelle unique.", "/guide-photos/medina-ruelle.png"),
            ("monuments", "Grand Socco — Place du 9 Avril 1947", "Place emblématique entre la ville moderne et la médina, souvent considérée comme l’entrée du vieux Tanger.", "/guide-photos/grand-socco.png"),
            ("monuments", "Le Petit Socco", "Petite place historique au cœur de la médina, autrefois fréquentée par artistes, écrivains et voyageurs.", "/guide-photos/petit-socco.png"),
            ("monuments", "Palais de la Kasbah / Dar El Makhzen", "Ancien palais du sultan, aujourd’hui lié au patrimoine culturel et architectural de Tanger.", "/guide-photos/dar-el-makhzen.png"),
            ("monuments", "Cap Spartel et son phare", "Site naturel et historique à l’entrée du détroit de Gibraltar, symbole du patrimoine maritime tangérois.", "/guide-photos/kasbah-view.png"),
            ("monuments", "Les Grottes d’Hercule", "Site mythique près du Cap Spartel, célèbre pour son ouverture naturelle donnant sur l’océan.", "/guide-photos/kasbah-rooftops.png"),
            ("monuments", "Borj Dar El Baroud / Fortifications", "Ancien ouvrage défensif lié à l’histoire militaire de Tanger et à ses fortifications.", "/guide-photos/kasbah-fortifications.png"),
            ("musees", "Musée la Kasbah des cultures méditerranéennes", "Musée patrimonial présentant des collections archéologiques et ethnographiques liées à l’identité méditerranéenne de Tanger.", "/guide-photos/dar-el-makhzen.png"),
            ("musees", "Musée de la Kasbah — Espace d’art contemporain", "Espace culturel dédié aux expositions temporaires, rencontres artistiques et création contemporaine.", "/guide-photos/terrace-photo.png"),
            ("musees", "Dar Niaba — Musée des artistes voyageurs", "Musée autour de l’histoire diplomatique de Tanger et des artistes voyageurs inspirés par le Maroc.", "/guide-photos/petit-socco.png"),
            ("musees", "Musée de la Légation américaine de Tanger", "Ancienne légation américaine devenue musée, centre de recherche et lieu culturel maroco-américain.", "/guide-photos/medina-collage.png"),
            ("musees", "Centre d’interprétation des fortifications", "Un lieu pour comprendre l’histoire défensive de Tanger et ses anciens systèmes de protection.", "/guide-photos/kasbah-fortifications.png"),
        ]
        for index, (section, title, description, image_path) in enumerate(places, start=1):
            self.upsert(GuidePlace, {"title": title}, {"section": section, "description": description, "image_path": image_path, "sort_order": index, "is_active": True})

    def seed_events(self):
        ideas = [
            ("Anniversaire", "Birthday apartment setup", "Une décoration chaleureuse avec ballons, gâteau, bougies, message personnalisé et coin photo.", "Ballons premium et arche légère\nTable surprise avec gâteau\nMessage personnalisé au prénom", "/event-photos/anniversaire.jpg"),
            ("Amoureux", "Romantic night", "Une ambiance douce pour couples : pétales, bougies LED, lumière tamisée et détails raffinés.", "Chemin de pétales et bougies\nPlateau gourmand ou fleurs\nOption demande / surprise", "/event-photos/amoureux.jpg"),
            ("Bride to be", "Bridal suite decor", "Une mise en scène chic pour bride to be, photos entre amies et préparation avant mariage.", "Ballons blancs, dorés ou rose gold\nLettrage Bride to Be\nCoin photo élégant", "/event-photos/bride-to-be.jpg"),
            ("Dîner privé", "Private dinner", "Une table intime dans l’appartement avec décoration florale, lumière chaude et service sur demande.", "Dressage de table premium\nFleurs et ambiance lumineuse\nOption chef / pâtisserie locale", "/event-photos/diner-prive.jpg"),
        ]
        for index, (category, title, description, bullet_points, image_path) in enumerate(ideas, start=1):
            self.upsert(EventIdea, {"title": title}, {"category": category, "description": description, "bullet_points": bullet_points, "image_path": image_path, "sort_order": index, "is_active": True})

    def seed_purple_pearl(self):
        plans = [
            ("1. Plan sous-sol", "1. Plan sous-sol", "Plan du sous-sol / parking du projet Purple Pearl.", "/assets/purple-pearl-plan-general.jpg"),
            ("2. Plan RDC - Locaux commerciaux", "2. Plan RDC - Locaux commerciaux", "Plan du rez-de-chaussée dédié aux locaux commerciaux.", "/assets/purple-pearl-plan-etage-courant.jpg"),
            ("3. Plan RDC haut - Locaux commerciaux", "3. Plan RDC haut - Locaux commerciaux", "Plan RDC haut avec les locaux commerciaux.", "/assets/purple-pearl-plan-etage-courant.jpg"),
            ("3.1. Plan RDC haut - Appartements avec cour", "3.1. Plan RDC haut - Appartements avec cour", "Appartements avec cour au RDC haut.", "/assets/purple-pearl-plan-etage-courant.jpg"),
            ("Plans des 1er, 2e, 3e et 4e étages (Appartement type 1 - 2 - 3 - 4 - 5)", "Plans des 1er, 2e, 3e et 4e étages", "Appartement type 1 - 2 - 3 - 4 - 5.", "/assets/purple-pearl-plan-etage-courant.jpg"),
            ("5. Plan 1er retrait (Appartement 1 - 2 - 3 - 4)", "5. Plan 1er retrait", "Appartement 1 - 2 - 3 - 4.", "/assets/purple-pearl-plan-1er-retrait.jpg"),
            ("6. Plan 2e retrait (Appartement type 1 - 2 - 3 - 4)", "6. Plan 2e retrait", "Appartement type 1 - 2 - 3 - 4.", "/assets/purple-pearl-plan-2eme-retrait.jpg"),
            ("Façades & situation", "Façades & situation", "Façades, situation du projet et images de synthèse du bâtiment.", "/assets/purple-pearl-plan-facades-situation.jpg"),
        ]
        for index, (button_label, title, description, image_path) in enumerate(plans, start=1):
            self.upsert(PurplePearlPlan, {"button_label": button_label}, {"title": title, "description": description, "image_path": image_path, "alt_text": title, "sort_order": index, "is_active": True})

    def seed_testimonials(self):
        testimonials = [
            ("Korkanc", "Turquie — Appartement Hilton 1 Chambre — 2 nuits, juillet 2025 — Couple", "Ceux qui souhaitent faire une réservation doivent le faire immédiatement s’ils trouvent une place.", False),
            ("Mohamed", "Pays-Bas — Appartement Hilton 1 Chambre — 2 nuits, novembre 2023 — Couple", "Emplacement de premier choix. La vue était magnifique.", False),
            ("Shéhérazade", "France — Appartement Hilton 1 Chambre — 2 nuits, novembre 2023 — Famille", "Très bel appartement décoré avec soin, la vue est exceptionnelle et la localisation idéale.", False),
            ("Elamrani", "Maroc — Appartement Hilton 2 Chambres — 3 nuits, décembre 2024 — Groupe", "Un appartement magnifique, propre et bien équipé, avec une vue superbe et un emplacement magnifique avec facilité d’accès.", False),
            ("Régine", "France — Appartement Hilton 2 Chambres — 3 nuits, août 2025 — Famille", "Très bon séjour, je recommande à 100% l’appartement. Tout était bien : propreté, accueil, je le conseille.", False),
            ("Saber", "Royaume-Uni — Appartement Hilton 1 Chambre — 5 nuits, juillet 2024 — Famille", "Great place! Great location, very clean.", False),
            ("Audrey", "États-Unis — Appartement Hilton 1 Chambre — 7 nuits, janvier 2026 — Couple", "Exceptionnel. I stayed for 7 days, it was worth the price, great place and stuff. Loved it and will return whenever I’m back in Tangier.", False),
            ("Khadija", "France — Apartment in City Center Tangier — 4 nuits, février 2024 — Famille", "Exceptionnel.", True),
            ("Ibrahim", "Arabie Saoudite — Apartment in City Center Tangier — 4 nuits, novembre 2023 — Groupe", "L’appartement est absolument magnifique, l’emplacement est superbe et proche de tous les services, et le service de Mme Hajar était extrêmement poli et courtois.", True),
        ]
        for index, (client_name, details, quote, city_center) in enumerate(testimonials, start=1):
            self.upsert(Testimonial, {"client_name": client_name, "details": details}, {"rating": "10/10", "quote": quote, "highlight_city_center": city_center, "sort_order": index, "is_active": True})
