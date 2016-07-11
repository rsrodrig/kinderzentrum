# -*- coding: utf-8 -*-

from django.db import models
#from .paciente_model  import Paciente

class Familiar(models.Model):
    """ Familiar del paciente """
    
    ESTUDIO_PRIMARIA = 0
    ESTUDIO_SECUNDARIA = 1
    ESTUDIO_UNIVERSIDAD = 2
    ESTUDIO_SUPERIOR = 3

    NIVEL_ESTUDIO_CHOICES = (
        (ESTUDIO_PRIMARIA, "Primaria"),
        (ESTUDIO_SECUNDARIA, "Secundaria"),
        (ESTUDIO_UNIVERSIDAD, "Universidad"),
        (ESTUDIO_SUPERIOR, "Superior"),
    )

    TRABAJO_NO_TRABAJA = 0
    TRABAJO_TIEMPO_COMPLETO = 1
    TRABAJO_MEDIO_TIEMPO = 2 
    TRABAJO_POR_HORAS = 3
    JORNADA_TRABAJO_CHOICES = (
        (TRABAJO_NO_TRABAJA, "No Trabaja"),
        (TRABAJO_TIEMPO_COMPLETO, "Tiempo completo"),
        (TRABAJO_MEDIO_TIEMPO, "Medio tiempo"),
        (TRABAJO_POR_HORAS, "Por horas")
    )

    parentesco = models.CharField(max_length=50)
    nombres = models.CharField(max_length=256)
    apellidos = models.CharField(max_length=256)
    nivel_estudio = models.PositiveSmallIntegerField("nivel de estudio",
                                                     choices=NIVEL_ESTUDIO_CHOICES)

    direccion = models.CharField("dirección", max_length=256)
    telefonos = models.CharField("teléfono", max_length=50)
    empresa = models.CharField("lugar de trabajo",
                               max_length=256,
                               blank=True)
    direccion_empresa = models.CharField("dirección de empresa",
                                         max_length=256,
                                         blank=True)
    jornada = models.PositiveSmallIntegerField("jornada de trabajo", choices=JORNADA_TRABAJO_CHOICES)
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.apellidos + " " + self.nombres


class DatosFamiliaresOtros(models.Model):
    "Datos de historia clinica familiar y otra informacion"

    ORIENTACION_RADIO = "Radio"
    ORIENTACION_TV = "Tv"
    ORIENTACION_PERIODICO = "Periódico"
    ORIENTACION_OTRO = "Otro"
    ORIENTACION_CONOCIDO = "Invitación de un conocido"
    ORIENTACION_CHOICES = (
        (ORIENTACION_RADIO, ORIENTACION_RADIO),
        (ORIENTACION_TV, ORIENTACION_TV),
        (ORIENTACION_PERIODICO, ORIENTACION_PERIODICO),
        (ORIENTACION_CONOCIDO, ORIENTACION_CONOCIDO),
        (ORIENTACION_OTRO, "Otro (Especifique)")
    )
    
    numero_hermanos = models.PositiveSmallIntegerField("Número de hermanos")
    transtorno_hermanos = models.NullBooleanField("¿Alguno de los hermanos tiene algún tipo de transtorno?")
    hermano_transtorno = models.PositiveSmallIntegerField("¿Cuál de los hermanos? (Orden en que nació)", blank=True, null=True)
    transtorno = models.CharField("Qué transtorno?", max_length=50, blank=True)
    alteracion_desarrollo = models.NullBooleanField("¿Ha existido algún tipo de alteración en su desarrollo?")
    tipo_enfermedad_parientes = models.CharField("Detallar el tipo de enfermedad que se ha presentado en los parientes", max_length=256, blank=True)
    orientacion_a_institucion = models.CharField("Quién los orientó a ésta institución?", max_length=100)

class Hermano(models.Model):
    "Datos de hermano"
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField("Fecha de nacimiento")
    datos_familiares = models.ForeignKey(DatosFamiliaresOtros, on_delete=models.CASCADE, related_name='hermanos_set')
