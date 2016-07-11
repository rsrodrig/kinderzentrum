# -*- coding: utf-8 -*-

from django.db import models
import datetime

class RecienNacido(models.Model):
    "Datos del recién nacido"

    edad_madre = models.PositiveSmallIntegerField("Edad de la madre cuando nació el bebé", blank=True, null=True)

    edad_padre = models.PositiveSmallIntegerField("Edad del padre cuando nació el bebé", blank=True, null=True)

    peso = models.FloatField("peso(gr)")

    tamanio = models.FloatField("tamaño(cm)")

    diametro_encefalico = models.FloatField("diámetro encefálico(cm)")

    APGAR_1 = 0
    APGAR_5 = 1
    APGAR_10 = 2
    APGAR_DESCONOCIDO = 4
    APGAR_CHOICES = (
        (APGAR_1, "APGAR 1"),
        (APGAR_5, "APGAR 5"),
        (APGAR_10, "APGAR 10"),
        (APGAR_DESCONOCIDO, "Desconoce")
    )
    apgar_score = models.PositiveSmallIntegerField("¿Cuál fue la puntuación del apgar? Si no lo sabe podría ayudarnos con la historia clínica de su hijo(a)") 

    COMPLICACIONES_REANIMACION = "Necesitó reanimación"
    COMPLICACIONES_OXIGENO = "Requirió oxígeno"
    COMPLICACIONES_SANGRE = "Transfusión sanguínea"
    COMPLICACIONES_INTRAVENOSA = "Alguna medicina intravenosa"
    COMPLICACIONES_CIRUGIA = "Cirugía inmediata"
    COMPLICACIONES_OTRO = "Otro"
    COMPLICACIONES_CHOICES = (
        (COMPLICACIONES_REANIMACION, COMPLICACIONES_REANIMACION),
        (COMPLICACIONES_OXIGENO, COMPLICACIONES_OXIGENO),
        (COMPLICACIONES_SANGRE, COMPLICACIONES_SANGRE),
        (COMPLICACIONES_INTRAVENOSA, COMPLICACIONES_INTRAVENOSA),
        (COMPLICACIONES_CIRUGIA, COMPLICACIONES_CIRUGIA),
        (COMPLICACIONES_OTRO, "Otro (Especifique)")
    )

    complicaciones_nacimiento = models.CharField("¿El niño(a) tuvo alguna de éstas complicaciones al nacer?", max_length=256, blank=True)

    APEGO_PRECOZ_MUY_POCO = 0
    APEGO_PRECOZ_MUCHO_TIEMPO = 1
    APEGO_PRECOZ_NADA = 2
    APEGO_PRECOZ_CHOICES = (
        (APEGO_PRECOZ_MUY_POCO, "Muy Poco"),
        (APEGO_PRECOZ_MUCHO_TIEMPO, "Mucho Tiempo"),
        (APEGO_PRECOZ_NADA, "Nada")
    )
    tiempo_apego_precoz = models.PositiveSmallIntegerField("¿Cuánto tiempo duró el apego precoz?")

    SOSTENER_BEBE_MENOS_10 = 0
    SOSTENER_BEBE_MENOS_30 = 1
    SOSTENER_BEBE_1_HORA = 2
    SOSTENER_BEBE_2_HORAS = 3
    SOSTENER_BEBE_3_HORAS = 4
    SOSTENER_BEBE_4_HORAS = 5
    SOSTENER_BEBE_1_DIA = 6
    SOSTENER_BEBE_1_SEMANA = 7
    SOSTENER_BEBE_CHOICES = (
        (SOSTENER_BEBE_MENOS_10, "Menos de 10 minutos"),
        (SOSTENER_BEBE_MENOS_30, "Menos de 30 minutos"),
        (SOSTENER_BEBE_1_HORA, "1 Hora"),
        (SOSTENER_BEBE_2_HORAS, "2 Horas"),
        (SOSTENER_BEBE_3_HORAS, "3 Horas"),
        (SOSTENER_BEBE_4_HORAS, "4 Horas"),
        (SOSTENER_BEBE_1_DIA, "1 Día"),
        (SOSTENER_BEBE_1_SEMANA, "1 Semana")
    )
    tiempo_sostener_bebe = models.PositiveSmallIntegerField("¿Cuánto tiempo pasó hasta que usted pudo sostener a su bebé?")

    tiempo_internado = models.DurationField("¿Cuánto tiempo permaneció internado(a)?", blank=True, default=datetime.timedelta())

    CONTACTO_VISITAS_ESTABLECIDAS = 0
    CONTACTO_VISITAS_CUANDO_QUERIA = 1
    CONTACTO_SOLO_PARA_DAR_LACTAR = 2
    CONTACTO_NINGUNA = 3
    CONTACTO_CHOICES = (
        (CONTACTO_VISITAS_ESTABLECIDAS, "Visitas establecidas por el hospital"),
        (CONTACTO_VISITAS_CUANDO_QUERIA, "Visitas cuando yo quería"),
        (CONTACTO_SOLO_PARA_DAR_LACTAR , "Sólo para darle de lactar"),
        (CONTACTO_NINGUNA, "Ninguna") 
    )
    tipo_contacto = models.PositiveSmallIntegerField("¿Qué tipo de contacto tuvo con su bebé mientras estuvo internado?", blank=True)

    PRIMERA_LACTANCIA_BIBERON = 0
    PRIMERA_LACTANCIA_SONDA = 1
    PRIMERA_LACTANCIA_LACTANCIA_MATERNA = 2
    PRIMERA_LACTANCIA_CHOICES = (
        (PRIMERA_LACTANCIA_BIBERON, "Biberón"),
        (PRIMERA_LACTANCIA_SONDA, "Sonda"),
        (PRIMERA_LACTANCIA_LACTANCIA_MATERNA, "Lactancia materna")
    )
    primera_lactancia = models.PositiveSmallIntegerField("La primera vez que el bebé tomó leche fue con")
