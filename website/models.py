from django.db import models
from django.utils.text import slugify


class VisibleOrderedModel(models.Model):
    created_at = models.DateTimeField("date d'ajout", auto_now_add=True)
    updated_at = models.DateTimeField("derniere modification", auto_now=True)
    sort_order = models.PositiveIntegerField(
        "ordre d'affichage",
        default=0,
        help_text="Plus le nombre est petit, plus l'element apparait haut dans la page.",
    )
    is_active = models.BooleanField(
        "visible sur le site",
        default=True,
        help_text="Decochez pour cacher cet element sans le supprimer.",
    )

    class Meta:
        abstract = True


class ImageSourceModel(models.Model):
    image = models.ImageField(
        "nouvelle image",
        upload_to="site/images/",
        blank=True,
        null=True,
        help_text="Chargez une nouvelle image si vous voulez remplacer le visuel actuel.",
    )
    image_path = models.CharField(
        "image deja dans le site",
        max_length=500,
        blank=True,
        help_text="Exemple: /assets/nectar-bureau.png. Laissez vide si vous chargez une nouvelle image.",
    )

    class Meta:
        abstract = True


class SiteContact(VisibleOrderedModel):
    address = models.CharField("adresse affichee", max_length=200, default="Tanger, Maroc")
    phone_display = models.CharField(
        "telephones affiches",
        max_length=200,
        default="06 75 59 92 56 / 07 73 86 35 85",
    )
    whatsapp_number = models.CharField(
        "numero WhatsApp",
        max_length=30,
        default="212675599256",
        help_text="Format international sans +, par exemple 212675599256.",
    )
    email_display = models.CharField(
        "emails affiches",
        max_length=200,
        default="info@nectar.ma / contact@nectar.ma",
    )

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "coordonnees du site"
        verbose_name_plural = "coordonnees du site"

    def __str__(self):
        return "Coordonnees Nectar"


class Property(VisibleOrderedModel, ImageSourceModel):
    SALE = "sale"
    RENT = "rent"
    APARTMENT = "apartment"
    COMMERCIAL = "commercial"

    TRANSACTION_CHOICES = (
        (SALE, "Vente"),
        (RENT, "Location"),
    )
    PROPERTY_TYPE_CHOICES = (
        (APARTMENT, "Appartement"),
        (COMMERCIAL, "Local commercial"),
    )

    transaction = models.CharField("vente ou location", max_length=12, choices=TRANSACTION_CHOICES)
    property_type = models.CharField("type de bien", max_length=20, choices=PROPERTY_TYPE_CHOICES)
    title = models.CharField("titre de l'annonce", max_length=200)
    tag = models.CharField("petite ligne au-dessus du titre", max_length=200, blank=True)
    residence = models.CharField("residence", max_length=160, blank=True)
    district = models.CharField("quartier", max_length=160, blank=True)
    address = models.TextField("adresse ou emplacement", blank=True)
    description = models.TextField("description courte", blank=True)
    floor = models.CharField("etage", max_length=80, blank=True)
    unit_number = models.CharField("numero appartement/local", max_length=80, blank=True)
    bedrooms = models.PositiveSmallIntegerField("nombre de chambres", blank=True, null=True)
    surface_total = models.DecimalField("surface globale en m2", max_digits=8, decimal_places=2, blank=True, null=True)
    surface_sold = models.CharField("surface vendue", max_length=120, blank=True)
    mezzanine = models.CharField("mezzanine", max_length=120, blank=True)
    project_label = models.CharField("projet client", max_length=160, blank=True)
    price = models.CharField("prix affiche", max_length=120, blank=True)
    price_note = models.CharField("note sous le prix", max_length=160, blank=True)
    cta_label = models.CharField("texte du bouton", max_length=120, blank=True)

    class Meta:
        ordering = ("sort_order", "title")
        verbose_name = "bien immobilier"
        verbose_name_plural = "biens immobiliers"

    def __str__(self):
        return self.title


class PropertyPhoto(VisibleOrderedModel, ImageSourceModel):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="bien concerne",
    )
    title = models.CharField("nom affiche dans l'album", max_length=160)
    alt_text = models.CharField(
        "description de la photo",
        max_length=220,
        blank=True,
        help_text="Texte court utile si l'image ne se charge pas.",
    )

    class Meta:
        ordering = ("property", "sort_order", "id")
        verbose_name = "photo du bien"
        verbose_name_plural = "photos des biens"

    def __str__(self):
        return f"{self.property} - {self.title}"


class GuidePlace(VisibleOrderedModel, ImageSourceModel):
    MONUMENTS = "monuments"
    MUSEUMS = "musees"
    SECTION_CHOICES = (
        (MONUMENTS, "Monuments historiques"),
        (MUSEUMS, "Musees"),
    )
    section = models.CharField("rubrique du guide", max_length=20, choices=SECTION_CHOICES)
    title = models.CharField("nom du lieu", max_length=220)
    description = models.TextField("description courte")

    class Meta:
        ordering = ("section", "sort_order", "title")
        verbose_name = "lieu du guide de Tanger"
        verbose_name_plural = "lieux du guide de Tanger"

    def __str__(self):
        return self.title


class EventIdea(VisibleOrderedModel, ImageSourceModel):
    category = models.CharField("categorie", max_length=120)
    title = models.CharField("titre", max_length=180)
    description = models.TextField("description courte")
    bullet_points = models.TextField(
        "details affiches",
        blank=True,
        help_text="Un detail par ligne.",
    )

    class Meta:
        ordering = ("sort_order", "title")
        verbose_name = "idee evenement"
        verbose_name_plural = "idees evenement"

    def __str__(self):
        return self.title


class PurplePearlPlan(VisibleOrderedModel, ImageSourceModel):
    key = models.SlugField("reference du plan", max_length=120, unique=True, editable=False)
    button_label = models.CharField("titre du bouton", max_length=240)
    title = models.CharField("titre sous l'image", max_length=240, blank=True)
    description = models.CharField("description sous l'image", max_length=300, blank=True)
    alt_text = models.CharField("description du plan architectural", max_length=240, blank=True)
    image_3d = models.ImageField(
        "nouveau plan 3D",
        upload_to="site/images/",
        blank=True,
        null=True,
        help_text="Chargez une nouvelle image si vous voulez remplacer le plan 3D actuel.",
    )
    image_3d_title = models.CharField("titre du premier visuel 3D", max_length=120, default="Plan 3D")
    image_3d_path = models.CharField(
        "plan 3D deja dans le site",
        max_length=500,
        blank=True,
        help_text="Exemple: /assets/purple-pearl/plans/plan-sous-sol-3d.jpg. Laissez vide si vous chargez une nouvelle image.",
    )
    image_3d_alt_text = models.CharField("description du plan 3D", max_length=240, blank=True)
    image_3d_secondary = models.ImageField(
        "nouveau deuxieme visuel 3D",
        upload_to="site/images/",
        blank=True,
        null=True,
        help_text="Chargez une nouvelle image si vous voulez ajouter un deuxieme visuel 3D.",
    )
    image_3d_secondary_title = models.CharField("titre du deuxieme visuel 3D", max_length=120, blank=True)
    image_3d_secondary_path = models.CharField(
        "deuxieme visuel 3D deja dans le site",
        max_length=500,
        blank=True,
        help_text="Exemple: /assets/purple-pearl/plans/facade-3d-nuit.jpg. Laissez vide si vous chargez une nouvelle image.",
    )
    image_3d_secondary_alt_text = models.CharField("description du deuxieme visuel 3D", max_length=240, blank=True)

    class Meta:
        ordering = ("sort_order", "title")
        verbose_name = "plan Purple Pearl"
        verbose_name_plural = "plans Purple Pearl"

    def save(self, *args, **kwargs):
        if not self.key:
            base = slugify(self.button_label or self.title)[:90] or "plan"
            key = base
            index = 2
            while PurplePearlPlan.objects.filter(key=key).exclude(pk=self.pk).exists():
                key = f"{base}-{index}"
                index += 1
            self.key = key
        super().save(*args, **kwargs)

    def __str__(self):
        return self.button_label


class Testimonial(VisibleOrderedModel):
    rating = models.CharField("note affichee", max_length=40, default="10/10")
    quote = models.TextField("avis client")
    client_name = models.CharField("nom du client", max_length=160)
    details = models.CharField("details du sejour", max_length=260)
    highlight_city_center = models.BooleanField(
        "mentionner City Center",
        default=False,
        help_text="Cochez pour ajouter la mention City Center comme sur la maquette.",
    )

    class Meta:
        ordering = ("sort_order", "client_name")
        verbose_name = "recommandation client"
        verbose_name_plural = "recommandations clients"

    def __str__(self):
        return self.client_name


class ContactRequest(models.Model):
    NEW = "new"
    READ = "read"
    DONE = "done"
    STATUS_CHOICES = (
        (NEW, "Nouvelle demande"),
        (READ, "Vue"),
        (DONE, "Traitee"),
    )

    created_at = models.DateTimeField("date de reception", auto_now_add=True)
    status = models.CharField("statut", max_length=12, choices=STATUS_CHOICES, default=NEW)
    full_name = models.CharField("nom complet", max_length=180)
    phone = models.CharField("telephone", max_length=80)
    email = models.EmailField("email", blank=True)
    project = models.CharField("projet", max_length=120, blank=True)
    property_type = models.CharField("type de bien", max_length=120, blank=True)
    budget = models.CharField("budget", max_length=120, blank=True)
    preferred_date = models.DateField("date souhaitee", blank=True, null=True)
    preferred_time = models.CharField("heure souhaitee", max_length=40, blank=True)
    appointment_mode = models.CharField("mode de rendez-vous", max_length=120, blank=True)
    message = models.TextField("message", blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "demande de contact"
        verbose_name_plural = "demandes de contact"

    def __str__(self):
        return f"{self.full_name} - {self.project or 'Demande'}"


class PurplePearlVisitRequest(models.Model):
    NEW = "new"
    READ = "read"
    DONE = "done"
    STATUS_CHOICES = (
        (NEW, "Nouvelle demande"),
        (READ, "Vue"),
        (DONE, "Traitee"),
    )

    created_at = models.DateTimeField("date de reception", auto_now_add=True)
    status = models.CharField("statut", max_length=12, choices=STATUS_CHOICES, default=NEW)
    visit_type = models.CharField("type de visite", max_length=120)
    preferred_date = models.DateField("date souhaitee", blank=True, null=True)
    preferred_time = models.CharField("heure souhaitee", max_length=40, blank=True)
    full_name = models.CharField("nom complet", max_length=180)
    phone = models.CharField("telephone", max_length=80)
    email = models.EmailField("email", blank=True)
    message = models.TextField("message", blank=True)
    consent = models.BooleanField("accepte d'etre contacte", default=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "demande de visite Purple Pearl"
        verbose_name_plural = "demandes de visite Purple Pearl"

    def __str__(self):
        return f"{self.full_name} - {self.visit_type}"


class NewsletterSignup(models.Model):
    created_at = models.DateTimeField("date d'inscription", auto_now_add=True)
    email = models.EmailField("email")
    source = models.CharField("origine", max_length=120, blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "inscription newsletter"
        verbose_name_plural = "inscriptions newsletter"

    def __str__(self):
        return self.email
