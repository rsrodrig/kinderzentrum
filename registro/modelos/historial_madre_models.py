# -*- coding: utf-8 -*-
from django.db import models

CHOICES_TRIMESTRES = ((1,'1er Trimestre'),(2,'2do Trimestre'),(3,'3er Trimestre'))

class HistorialMadre(models.Model):

    CHOICES_ENFERMEDADES_PREVIAS = [('diabetes','Diabetes'),
                                    ('hipertension','Hipertensión'),
                                    ('infeccion_urinaria','Infecciones en las vías urinarias'),
                                    ('otra','Otras(Especifique)')]

    CHOICES_ENFERMEDADES_ANTES_EMBARA = [('enfemedad_cardiaca','Enfermedades cardíacas'),
                                         ('enfermedad_hepatica','Enfermedades hepáticas'),
                                         ('enfermedad_mental','Enfermedades mentales'),
                                         ('problema_azucar','Problemas con el azúcar'),
                                         ('otra','Otras(Especifique)')]

    CHOICES_ANTICONCEPTIVO = [('pildoras','Píldoras'),
                              ('ritmo','Ritmo'),
                              ('diu_cobre','Diu de cobre'),
                              ('preservativos','Preservativos'),
                              ('parches','Parches'),
                              ('anillo_vaginal','Anillo vaginal'),
                              ('implante_sudermico','Implante sudérmico'),
                              ('inyectables','Inyectables')]
    enfermedades_previas = models.CharField("Indique si antes del embarazo ha sufrido algunas de las siguientes enfermedades",
                                        max_length=200, blank=True)
    enfermedades_durante_embarazo = models.CharField("Indique si durante el embarazo sufrió algunas de las siguientes enfermedades", max_length=256, blank=True)

    enfermedad_cronica = models.CharField("Indique algún tipo de enfermedad crónica", blank=True, max_length=100)
 
    defunciones_fetales = models.PositiveSmallIntegerField("¿Cuántas defunciones fetales ha tenido durante su vida?", default=0)

    hijos_nacidos_muertos = models.PositiveSmallIntegerField("Número de hijos nacidos muertos", default=0)
    hijos_nacidos_vivos = models.PositiveSmallIntegerField("Número de hijos nacidos vivos", default=0)
    embarazos = models.PositiveSmallIntegerField("número de embarazos", default=1)
    anticonceptivos = models.CharField(max_length=100, blank=True)

    enfermedades_antes_concepcion = models.CharField("¿Tuvo usted alguna enfermedad grave, dolencia, accidente o infección, antes de concebir a éste bebé?", max_length=256, blank=True)


class Gestacion(models.Model):
    CHOICES_SENTIMIENTOS = [('felicidad','Felicidad'),('miedo','Miedo'),('júbilo','Júbilo'),('ansiedad','Ansiedad'),('estres','Estrés'),('incertidumbre','Incertidumbre')]
    CHOICES_MOMENTO = [('pocos_dias','A los pocos días'),('primer_mes','El primer mes'),('segundo_mes','El segundo mes'),('tercer_mes','El tercer mes'),('cuarto_mes','El cuarto mes'),('quinto_mes','El quinto mes'),('sexto_mes','El sexto mes'),('septimo_mes','El séptimo mes')]
    CHOICES_COMUNICA_BEBE = [('canto','Canto'),('cuentos','Cuentos'),('musica','Música (audífonos para gestación)'),('caricias','Caricias'),('estimulacion_intrauterina','Estimulación intrauterina (luces en barriga o clash overflow)'),('ninguno','Ninguno')]
    
    sentimientos = models.CharField("¿Qué sintió cuando se enteró que estaba embarazada? Marque todas las opciones que desee", max_length=200, blank=True)
    num_embarazo = models.PositiveSmallIntegerField("¿Qué número de embarazo es este?")
    momento_desc_embarazo = models.CharField("¿En qué momento se enteró que estaba embarazada?", max_length=250)
    lugar_curso_prenatal = models.CharField("¿En qué lugar fue el curso prenatal?",max_length=100, blank=True)
    carga_horaria = models.CharField("¿Cuánta fue la carga del curso prenatal?",max_length=100, blank=True)
    #nauseas_trimestre = models.SmallIntegerField()
    vacuna_tetano = models.BooleanField("¿Se vacunó usted contra el tétano durante el embarazo?")
    comunicacion_bebe = models.CharField("¿Cómo se comunicaba con el bebe? Marque todas las opciones que desee.",max_length=500)
    

class Actividad_Gestacion(models.Model):
    ACTIVIDADES_CHOICES = (u'Fumar',u'Ingerir Alcohol',u'Consumir drogas',u'Realizar radiografías',u'Trabajar')
    periodo = models.SmallIntegerField(choices=CHOICES_TRIMESTRES)
    nombre_actividad = models.CharField(max_length=100, blank=True)
    gestacion = models.ForeignKey(Gestacion, on_delete=models.CASCADE)

class Situacion_Gestacion(models.Model):
    SITUACIONES_CHOICES = (u'Sangrados',u'Presión sanguínea elevada',u'Enfermedades infecciosas',
                           u'Accidentes graves',u'Operaciones',u'Crisis epilépticas',
                           u'Fiebre mayor a 38 ⁰C no determinada',u'Edema',
                           u'Depresión (Tristeza, ansiedad, estrés, problemas para dormir)',
                           u'Interrupción repentina de los movimientos del niño',
                           u'Nauseas',u'Otras enfermedades')
    periodo = models.SmallIntegerField(choices=CHOICES_TRIMESTRES)
    nombre_situacion = models.CharField(max_length=100, blank=True)
    gestacion = models.ForeignKey(Gestacion, on_delete=models.CASCADE)

