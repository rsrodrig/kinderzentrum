# -*- coding: utf-8 -*-

from django.db import models


class PrimerosDias(models.Model):
    "Primeros días de vida del niño(a)"
    SITUACIONES_COLICO = "Cólicos"
    SITUACIONES_INFECCION = "Infección"
    SITUACIONES_RESPIRACION = "Dificultades Respiratorias"
    SITUACIONES_RESPIRADOR_ARTIFICIAL = "Respirador Artificial"
    SITUACIONES_OTRO = "Otro"
    SITUACIONES_CHOICES = (
        (SITUACIONES_COLICO, SITUACIONES_COLICO),
        (SITUACIONES_INFECCION, SITUACIONES_INFECCION),
        (SITUACIONES_RESPIRACION, SITUACIONES_RESPIRACION),
        (SITUACIONES_RESPIRADOR_ARTIFICIAL, SITUACIONES_RESPIRADOR_ARTIFICIAL),
        (SITUACIONES_OTRO, "Otra enfermedad")
    )
    EXAMENES_PRUEBA_TALON = "Prueba de talón"
    EXAMENES_LECHE_MATERNA = "Examen para determinar leche materna"
    EXAMENES_OTRO = "Otro"
    
    EXAMENES_CHOICES = (
        (EXAMENES_PRUEBA_TALON, EXAMENES_PRUEBA_TALON),
        (EXAMENES_LECHE_MATERNA, EXAMENES_LECHE_MATERNA),
        (EXAMENES_OTRO, "Otro (Especifique)")
    )

    LUGAR_DORMIR_PROPIO_CUARTO = 0
    LUGAR_DORMIR_CUNA = 1
    LUGAR_DORMIR_CON_MAMA = 2
    LUGAR_DORMIR_CON_PADRES = 3
    LUGAR_DORMIR_CHOICES = (
        (LUGAR_DORMIR_PROPIO_CUARTO, "En su propio cuarto"),
        (LUGAR_DORMIR_CUNA, "En un moisés o cuna al lado de mamá"),
        (LUGAR_DORMIR_CON_MAMA, "En la cama con mamá"),
        (LUGAR_DORMIR_CON_PADRES, "En la cama con mamá y papá")
    )
    clinica_permanencia = models.CharField("¿Cuál fue la clínica u hospital en la que permaneció el niño(a)?", max_length=100, blank=True)
    dias_permanencia = models.PositiveIntegerField("Indique los días de permanencia", blank=True, null=True)
    situaciones_despues_nacimiento = models.CharField("¿Presentó su bebé alguna de éstas situaciones después del nacimiento?", max_length=256, blank=True)
    icteria = models.NullBooleanField("¿Hubo algún tratamiento por icteria")
    tratamiento_icteria = models.CharField("¿Cuál fue el tratamiento por icteria?", max_length=256, blank=True)
    examenes = models.CharField("¿Le realizaron al recién nacido algún tipo de exámen?", max_length=100, blank=True)
    veces_despertar_noche = models.PositiveSmallIntegerField("¿Cuántas veces se despertaba el recién nacido?", default=0)
    lugar_dormir = models.PositiveSmallIntegerField("¿Dónde dormía el bebé?")
    descripcion_bebe = models.CharField("Describa a su bebé los 3 primeros meses de vida", max_length=256)
    descripcion_madre = models.CharField("¿Cómo se sentía usted esos 3 primeros meses?", max_length=256)
    
