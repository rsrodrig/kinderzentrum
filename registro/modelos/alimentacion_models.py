# -*- coding: utf-8 -*-

from django.db import models


class AlimentacionCostumbres(models.Model):
    """Alimentación y Costumbres"""
    TIEMPO_LACTANCIA_MESES_1_4 = 0
    TIEMPO_LACTANCIA_MESES_5_6 = 1
    TIEMPO_LACTANCIA_MESES_7_8 = 2
    TIEMPO_LACTANCIA_MESES_9_12 = 3
    TIEMPO_LACTANCIA_MESES_13_18 = 4
    TIEMPO_LACTANCIA_MESES_19_24 = 5
    TIEMPO_LACTANCIA_CHOICES = (
        (TIEMPO_LACTANCIA_MESES_1_4, "1 - 4 Meses"),
        (TIEMPO_LACTANCIA_MESES_5_6, "5 - 6 Meses"),
        (TIEMPO_LACTANCIA_MESES_7_8, "7 - 8 Meses"),
        (TIEMPO_LACTANCIA_MESES_9_12, "9 - 12 Meses"),
        (TIEMPO_LACTANCIA_MESES_13_18, "13 - 18 Meses"),
        (TIEMPO_LACTANCIA_MESES_19_24, "19 - 24 Meses")
    )

    tiempo_leche_materna = models.PositiveSmallIntegerField(blank=True, null=True)

    MOTIVO_SUSPENSION_RECHAZO = "Rechazo del niño"
    MOTIVO_SUSPENSION_TRABAJO = "Vinculación laboral"
    MOTIVO_SUSPENSION_NO_LECHE = "No producía leche"
    MOTIVO_SUSPENSION_PERSONAL = "Decisión Personal"
    MOTIVO_SUSPENSION_ENFERMEDAD_MADRE = "Enfermedad de la madre"
    MOTIVO_SUSPENSION_OTRO = "Otro"
    MOTIVO_SUSPENSION_CHOICES = (
        (MOTIVO_SUSPENSION_RECHAZO, "Rechazo del niño"),
        (MOTIVO_SUSPENSION_TRABAJO, "Vinculación laboral"),
        (MOTIVO_SUSPENSION_NO_LECHE, "No producía leche"),
        (MOTIVO_SUSPENSION_PERSONAL, "Decisión Personal"),
        (MOTIVO_SUSPENSION_ENFERMEDAD_MADRE, "Enfermedad de la madre"),
        (MOTIVO_SUSPENSION_OTRO, "Otro(Especifique)")
    )
    motivo_suspencion_lactancia = models.CharField(max_length=100, blank=True, null=True)

    AFECCIONES_ESTRENIMIENTO = "Estreñimiento"
    AFECCIONES_DEPOSICIONES = "Deposiciones Líquidas"
    AFECCIONES_OTROS = "Otros"
    AFECCIONES_CHOICES  = (
        (AFECCIONES_ESTRENIMIENTO, AFECCIONES_ESTRENIMIENTO),
        (AFECCIONES_DEPOSICIONES, AFECCIONES_DEPOSICIONES),
        (AFECCIONES_OTROS, "Otros(Especifique)")
    )
    afecciones = models.CharField(max_length=100, blank=True)

    ENFERMEDADES_BRONQUITIS = "Infección a las vías aéreas superiores (Bronquitis)"
    ENFERMEDADES_OIDO = "Infecciones al oído medio (Dolores de oído)"
    ENFERMEDADES_FIEBRE = "Fiebre no determinada por más de 5 días"
    ENFERMEDADES_OTRO = "Otro"
    ENFERMEDADES_CHOICES = (
        (ENFERMEDADES_BRONQUITIS, ENFERMEDADES_BRONQUITIS),
        (ENFERMEDADES_OIDO, ENFERMEDADES_OIDO),
        (ENFERMEDADES_FIEBRE, ENFERMEDADES_FIEBRE),
        (ENFERMEDADES_OTRO, "Otro (Especifique)")
    )
    enfermedades = models.CharField(max_length=256, blank=True)
    edad_alimentacion_complementaria = models.PositiveSmallIntegerField("¿A qué edad inició la alimentación complementaria? (meses)")

    FORMA_ALIMENTO_PAPILLA = "Papilla"
    FORMA_ALIMENTO_JUGO = "Jugo"
    FORMA_ALIMENTO_COMPOTA = "Compota" 
    FORMA_ALIMENTO_LICUADO = "Licuado"
    FORMA_ALIMENTO_PURE = "Puré"
    FORMA_ALIMENTO_COCIDO = "Cocido"
    FORMA_ALIMENTO_FRITO = "Frito"
    FORMA_ALIMENTO_OTRO = "Otro"
    FORMA_ALIMENTO_CHOICES = (
        (FORMA_ALIMENTO_PAPILLA, FORMA_ALIMENTO_PAPILLA),
        (FORMA_ALIMENTO_JUGO, FORMA_ALIMENTO_JUGO),
        (FORMA_ALIMENTO_COMPOTA, FORMA_ALIMENTO_COMPOTA),
        (FORMA_ALIMENTO_LICUADO, FORMA_ALIMENTO_LICUADO),
        (FORMA_ALIMENTO_PURE, FORMA_ALIMENTO_PURE),
        (FORMA_ALIMENTO_COCIDO, FORMA_ALIMENTO_COCIDO),
        (FORMA_ALIMENTO_FRITO, FORMA_ALIMENTO_FRITO),
        (FORMA_ALIMENTO_OTRO, "Otro (Especifique)"),
    )
    forma_alimento = models.CharField(max_length=100)

    lugar_desayuno = models.CharField("desayuno", max_length=50)
    lugar_comida_media_manana = models.CharField("media mañana", max_length=50, blank=True)
    lugar_almuerzo = models.CharField("almuerzo", max_length=50)
    lugar_comida_media_tarde = models.CharField("media tarde", max_length=50, blank=True)
    lugar_cena = models.CharField("cena", max_length=50)
    lugar_comida_otro = models.CharField("otro", max_length=50, blank=True)
    alimento_preferido = models.CharField("¿Cuál es el alimento preferido por el niño(a)?", max_length=20)
    alimento_rechazado = models.CharField("¿Cuál es el alimento que rechaza el niño(a)?", max_length=20)

    APETITO_BUENO = 0
    APETITO_MALO = 1
    APETITO_MUY_BUENO = 2
    APETITO_REGULAR = 3
    APETITO_CHOICES = (
        (APETITO_MUY_BUENO, "Muy Bueno"),
        (APETITO_BUENO, "Bueno"),
        (APETITO_REGULAR, "Regular"),
        (APETITO_MALO, "Malo")
    )
    apetito = models.PositiveSmallIntegerField("¿Cómo es el apetito del niño?")

    motivo_cambios_alimentacion = models.CharField("Describa los principales cambios de la alimentación del fin de semana de los demás días", max_length=256, blank=True)


class SuplementoAlimenticio(models.Model):
    "Suplementos alimenticios consumidos por el niño(a)"
    frecuencia = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    cantidad = models.PositiveSmallIntegerField()
    alimentacion = models.ForeignKey(AlimentacionCostumbres, on_delete=models.CASCADE, related_name='suplementos')
 
