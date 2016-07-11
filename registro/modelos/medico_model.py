# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

class Medico(models.Model):
    """ Representa al medico del paciente """
    nombres = models.CharField(max_length=256)
    apellidos = models.CharField(max_length=256)
    direccion = models.CharField(max_length=256)
    telefonos = models.CharField(max_length=50)
    area = models.CharField(max_length=100)
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.apellidos + " " + self.nombres

