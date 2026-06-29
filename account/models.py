from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _("adresse email"),
        unique=True,
        help_text=_("Adresse email utilisee pour se connecter a l'administration."),
    )
    first_name = models.CharField(_("prenom"), max_length=150, blank=True)
    last_name = models.CharField(_("nom"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _("acces a l'administration"),
        default=False,
        help_text=_(
            "Cochez pour autoriser l'utilisateur a ouvrir le panneau d'administration."
        ),
    )
    is_active = models.BooleanField(
        _("compte actif"),
        default=True,
        help_text=_("Decochez pour bloquer ce compte sans le supprimer."),
    )
    date_joined = models.DateTimeField(_("date de creation"), default=timezone.now)
    date_updated = models.DateTimeField(_("derniere modification"), auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("utilisateur")
        verbose_name_plural = _("utilisateurs")
        ordering = ("-date_joined",)

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email
