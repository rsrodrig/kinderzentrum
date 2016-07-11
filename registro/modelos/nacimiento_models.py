# -*- coding: utf-8 -*-

from django.db import models

class Nacimiento(models.Model):
    TIPO_LUGAR_NACIMIENTO_CLINICA = 0
    TIPO_LUGAR_NACIMIENTO_HOSPITAL = 1
    TIPO_LUGAR_NACIMIENTO_MATERNIDAD = 2
    TIPO_LUGAR_NACIMIENTO_CASA = 3
    TIPO_LUGAR_NACIMIENTO_CHOICES = (
        (TIPO_LUGAR_NACIMIENTO_CLINICA, "Clínica"),
        (TIPO_LUGAR_NACIMIENTO_HOSPITAL, "Hospital"),
        (TIPO_LUGAR_NACIMIENTO_MATERNIDAD, "Maternidad"),
        (TIPO_LUGAR_NACIMIENTO_CASA, "Casa")
    )

    tipo_lugar_nacimiento = models.PositiveSmallIntegerField("¿Dónde ocurrió el nacimiento?")
    nombre_lugar_nacimiento = models.CharField("Nombre de institución", max_length=500, blank=True)
    semana_gestacion = models.PositiveSmallIntegerField("¿En qué semana de gestación nació el bebé?")

    METODO_NACIMIENTO_PARTO_VAGINAL = "Parto Vaginal"
    METODO_NACIMIENTO_CESAREA = "Cesárea"
    METODO_NACIMIENTO_EPISIOTOMIA = "Episiotomía"
    METODO_NACIMIENTO_FORCEPS = "Fórceps"
    METODO_NACIMIENTO_VENTOSA = "Ventosa"
    METODO_NACIMIENTO_CHOICES = (
        (METODO_NACIMIENTO_PARTO_VAGINAL, METODO_NACIMIENTO_PARTO_VAGINAL),
        (METODO_NACIMIENTO_CESAREA, METODO_NACIMIENTO_CESAREA),
        (METODO_NACIMIENTO_EPISIOTOMIA, METODO_NACIMIENTO_EPISIOTOMIA),
        (METODO_NACIMIENTO_FORCEPS, METODO_NACIMIENTO_FORCEPS),
        (METODO_NACIMIENTO_VENTOSA, METODO_NACIMIENTO_VENTOSA)
    )
    metodo_nacimiento = models.CharField("¿Cómo nación el bebé? Marque todas las opciones que necesite", max_length=100)

    MANERA_INICIO_PARTO_ESPONTANEA = 0
    MANERA_INICIO_PARTO_NO_TUVE = 1
    MANERA_INICIO_PARTO_INDUCIDA = 2
    MANERA_INICIO_PARTO_CHOICES = (
        (MANERA_INICIO_PARTO_ESPONTANEA, "Espontánea"),
        (MANERA_INICIO_PARTO_NO_TUVE, "No tuve"),
        (MANERA_INICIO_PARTO_INDUCIDA, "Inducida")
    )
    manera_inicio_parto = models.PositiveSmallIntegerField("¿Cuál fue la manera en que inició su labor de parto?")
    TIPO_RUPTURA_FUENTE_ESPONTANEA = 0
    TIPO_RUPTURA_FUENTE_INDUCIDA = 1
    TIPO_RUPTURA_FUENTE_CHOICES = (
        (TIPO_RUPTURA_FUENTE_ESPONTANEA, "Espontánea"),
        (TIPO_RUPTURA_FUENTE_INDUCIDA, "Inducida(El personal médico la rompió durante el tacto)")
    )
    tipo_ruptura_fuente= models.PositiveSmallIntegerField("¿Cómo fue la ruptura del agua fuente?")

    sentimientos_parto = models.CharField("¿Cómo se sintió durante su labor de parto?", max_length=500)
    sentimientos_nacimiento = models.CharField("¿Cómo se sintió durante el nacimiento de su hijo?", max_length=500)
    duracion_nacimiento = models.PositiveSmallIntegerField("¿Cuánto fue la duración del nacimiento? (Horas/minutos)")
    gemelar = models.BooleanField("¿Fue embarazo gemelar?")
    PRIMERA_PARTE_CUERPO_CABEZA = 0
    PRIMERA_PARTE_CUERPO_NALGA = 1
    PRIMERA_PARTE_CUERPO_EXTREMIDAD = 2
    PRIMERA_PARTE_CUERPO_CHOICES = (
        (PRIMERA_PARTE_CUERPO_CABEZA, "Cabeza"),
        (PRIMERA_PARTE_CUERPO_NALGA, "Nalga"),
        (PRIMERA_PARTE_CUERPO_EXTREMIDAD, "Brazo/Pierna")
    )
    primera_parte_cuerpo = models.PositiveSmallIntegerField("Seleccione qué parte del cuerpo salió primero")

    COMPLICACIONES_RUPTURA_UTERINA = "Ruptura Uterina"
    COMPLICACIONES_SANGRADO = "Sangrado"
    COMPLICACIONES_HIPERTONIA_UTERINA = "Hipertonía Uterina"
    COMPLICACIONES_RETENCION_PLACENTA = "Retención de placenta"
    COMPLICACIONES_ANESTESIA = "Anestesia General"
    COMPLICACIONES_DESCONOCE = "Desconoce"
    COMPLICACIONES_CHOICES = (
        (COMPLICACIONES_RUPTURA_UTERINA, COMPLICACIONES_RUPTURA_UTERINA),
        (COMPLICACIONES_SANGRADO, COMPLICACIONES_SANGRADO),
        (COMPLICACIONES_HIPERTONIA_UTERINA, COMPLICACIONES_HIPERTONIA_UTERINA),
        (COMPLICACIONES_RETENCION_PLACENTA, COMPLICACIONES_RETENCION_PLACENTA),
        (COMPLICACIONES_ANESTESIA, COMPLICACIONES_ANESTESIA),
        (COMPLICACIONES_DESCONOCE, COMPLICACIONES_DESCONOCE)
    )
    complicaciones = models.CharField("¿Tuvo usted complicaciones?", max_length=200, blank=True)

    medicamentos_parto = models.NullBooleanField("¿Se le administraron medicamentos o inyección durante el embarazo?")
    complicaciones_cordon = models.NullBooleanField("¿Hubieron complicaciones con el cordón umbilical?")
