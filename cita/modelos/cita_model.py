# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from registro.modelos.paciente_model import Paciente
from asistencia.models import Terapista,Tipo_terapia
import datetime

class Cita(models.Model):
    ESTADO_CHOICES = (
        ("A", "Agendada"),
        ("S", "Asistio"),
        ("N", "No asistio"),
        ("C", "Cancelada")
    )
    """ Representa la cita del paciente """
    fecha_registro = models.DateField(auto_now =True)
    fecha_cita = models.DateField(auto_now=False)
    hora_inicio = models.TimeField(auto_now=False)
    hora_fin = models.TimeField(auto_now=False)
    estado = models.CharField(choices=ESTADO_CHOICES, max_length=2, default='A')
    indicaciones = models.CharField(max_length=256)  
    tipo_terapia = models.ForeignKey(Tipo_terapia, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    terapista = models.ForeignKey(Terapista, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.paciente)
