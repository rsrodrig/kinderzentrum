# -*- coding: utf-8 -*-
from django.db import models

class Descripcion(models.Model):
    """ Descripción del problema del paciente """
    LIMITACIONES_OPTIONS = ((1, "SI"), (2, "NO"), (3, "DESCONOCE"))
    DESCUBRIO_MOLESTIAS_OPTIONS = [('papa','Papa'),('mama','Mama'),('abuelos','Abuelos'),('otros','Otros')]
    DIFICULTADES_OPTIONS = [('audicion','Audición'),('vision','Visión'),('lenguaje','Lenguaje'),('seguridad_si_mismo','Seguridad en sí mismo'),('comportamiento','Comportamiento'),('alimentacion','Alimentación'),('suenio','Sueño'),('interaccion_social','Interacción social'),('otro','Otro')]
    
    preocupacion = models.CharField(
        "¿Qué le preocupa de su hijo? Algo especial que le llame la atención",
        max_length=500
    )
    disc_molestias = models.CharField(
        "¿Quién descubrió estas molestias?",
        blank=True,
        max_length=256
    )
    edad_disc_molestia = models.PositiveSmallIntegerField(
        "¿A qué edad notaron estas molestias?"#,
        #blank=True
    )
    tratamiento = models.BooleanField("¿Se encuentra en algún tratamiento?")
    lugar_tratamiento = models.CharField("¿Dónde realiza el tratamiento?",
                                         max_length=256, blank=True)
    limitaciones_movimiento = models.IntegerField(
        "¿Existe alguna limitación con sus movimientos?",
        choices=LIMITACIONES_OPTIONS)

    areas_dificultad = models.CharField("¿Ha presentado su hijo(a) algún tipo de dificultad en éstas áreas?",
                                        max_length=256, blank=True)
    had_convulsion = models.SmallIntegerField("¿Ha sentido convulsiones?",
                                              choices=LIMITACIONES_OPTIONS)
    tipo_crisis = models.CharField("¿Qué tipo de crisis tuvo durante la convulsión?",
                                   max_length=256, blank=True)

    edad_crisis = models.PositiveSmallIntegerField("¿A qué edad fue la primera crisis?", blank=True, null=True)


class Terapia(models.Model):
    """ terapias recibidas por el paciente """
    TERAPIA_CHOICES = ((1, "Rehabilitación Física"),
                       (2, "Estimulación Temprana"),
                       (3, "Ninguna"))
    tipo = models.SmallIntegerField("Tipo de terapia", choices=TERAPIA_CHOICES)   
    tiempo_terapia = models.CharField("¿Cuánto tiempo lleva realizando la terapia", max_length=50)
    descripcion = models.ForeignKey(Descripcion, related_name="terapias")


class Medicamento(models.Model):
    """ Medicamento recetado para convulsiones """
    nombre = models.CharField("nombre del medicamento", max_length=100)
    dosis_diaria = models.IntegerField()
    descripcion = models.ForeignKey(Descripcion, related_name="medicamentos")
