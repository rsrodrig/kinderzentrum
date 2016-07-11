# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from .descripcion_models import *
from .medico_model import Medico
from .historial_madre_models import *
from .nacimiento_models import *
from .familiars_models import DatosFamiliaresOtros
from .recien_nacido_model import RecienNacido
from .alimentacion_models import AlimentacionCostumbres
from .primeros_dias_model import PrimerosDias


class Paciente(models.Model):
    """Modelo que representa a un paciente de la clinica"""
    GRUPO_SANGUINEO_CHOICES = (
        ("A+", "A+"),
        ("A-", "A-"),
        ("O+", "O+"),
        ("O-", "O-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"), 
        ("AB-", "AB-")       
    )

    SEXO_CHOICES = (
        ("M", "Masculino"),
        ("F", "Femenino")
    )
    nombres = models.CharField(max_length=256)
    apellidos = models.CharField(max_length=256)
    lugar_nacimiento = models.CharField("lugar de nacimiento", max_length=30)
    fecha_nacimiento = models.DateField("fecha de nacimiento")
    fecha_registro = models.DateField("fecha de registro",
                                      auto_now_add=True) #Autoregistro con la fecha de creacion
    nacionalidad = models.CharField(max_length=30)
    grupo_sanguineo = models.CharField("grupo sanguineo",
                                       choices=GRUPO_SANGUINEO_CHOICES,
                                       max_length=4, blank=False, default='O+')
    sexo = models.CharField(choices=SEXO_CHOICES, max_length=1, blank=False, default="--")

    #medico = models.OneToOneField(Medico)
    descripcion = models.OneToOneField(Descripcion)
    historial_madre = models.OneToOneField(HistorialMadre)
    gestacion = models.OneToOneField(Gestacion)
    nacimiento = models.OneToOneField(Nacimiento)
    recien_nacido = models.OneToOneField(RecienNacido)
    primeros_dias = models.OneToOneField(PrimerosDias)
    alimentacion = models.OneToOneField(AlimentacionCostumbres)
    datos_familiares = models.OneToOneField(DatosFamiliaresOtros)

    def __unicode__(self):
        return self.apellidos + " " + self.nombres

    def delete(self, *args, **kwargs):
        if self.descripcion:
            self.descripcion.delete()
        if self.historial_madre:
            self.historial_madre.delete()
        if self.gestacion:
            self.gestacion.delete()
        if self.nacimiento:
            self.nacimiento.delete()
        if self.recien_nacido:
            self.recien_nacido.delete()
        if self.primeros_dias:
            self.primeros_dias.delete()
        if self.alimentacion:
            self.alimentacion.delete()
        if self.datos_familiares:
            self.datos_familiares.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


