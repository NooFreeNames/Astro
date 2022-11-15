""" 
TODO:
    - Добавить поддержку журналирования пользователей в класс Logged
    - Добавить псевдонимы для космических
    - Узнать про GENERATED ALWAYS AS в django
    - Узнать про индексы в Django
"""

from django.db import models
from .apps import MainConfig
from django.contrib.auth.models import AbstractUser
# from django.conf import settings

MAX_NAME_LENGTH = 35
MAX_DESCRIPTION_LENGTH = 400


class Logged(models.Model):
    class Meta:
        abstract = True

    date_time_added = models.DateTimeField(auto_now_add=True)
    # date_time_change = models.DateTimeField(auto_now=True, null=True, default=None)
    # user_who_added = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    # user_who_change = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)


class Described(Logged):
    class Meta:
        abstract = True

    name = models.CharField(max_length=MAX_NAME_LENGTH, unique=True)
    description = models.TextField(
        max_length=MAX_DESCRIPTION_LENGTH, null=True, default=None)


class Observatory(Described):
    class Meta:
        indexes = [
            models.Index(fields=['name'], name='observatory_name_idx'),
            models.Index(fields=['code_name'],
                         name='observatory_code_name_idx'),
        ]

    code_name = models.CharField(max_length=15, unique=True)


class User(AbstractUser):
    observatory = models.ForeignKey(Observatory, null=True, on_delete=models.SET_NULL)


class PlanetType(Described):
    class Meta:
        db_table = MainConfig.name + '_planet_type'
        indexes = [models.Index(fields=['name'], name='planet_type_name_idx')]


class StarType(Described):
    class Meta:
        db_table = MainConfig.name + '_star_type'
        indexes = [models.Index(fields=['name'], name='star_type_name_idx')]

    name = models.CharField(max_length=1, unique=True)


class AstroObject(Described):
    class Meta:
        abstract = True

    name = models.CharField(max_length=MAX_NAME_LENGTH,
                            unique=True, null=True, default=None)
    date_time_confirmation = models.DateTimeField(null=True, default=None)
    is_confirmed = models.BooleanField()
    mass = models.FloatField(null=True, default=None)
    radius = models.FloatField(null=True, default=None)
    observatory = models.ForeignKey(Observatory, null=True, on_delete=models.SET_NULL)


class Star(AstroObject):
    class Meta:
        indexes = [models.Index(fields=['name'], name='star_name_idx')]

    surface_temperature = models.FloatField(null=True, default=None)
    luminosity = models.FloatField(null=True, default=None)
    type = models.ForeignKey(StarType, null=True, on_delete=models.SET_NULL)


class Planet(AstroObject):
    class Meta:
        indexes = [models.Index(fields=['name'], name='planet_name_idx')]

    orbital_radius = models.FloatField(null=True, default=None)
    orbital_period = models.FloatField(null=True, default=None)
    orbital_eccentricity = models.FloatField(null=True, default=None)
    type = models.ForeignKey(PlanetType, null=True, on_delete=models.SET_NULL)
    star_set = models.ManyToManyField(Star)
