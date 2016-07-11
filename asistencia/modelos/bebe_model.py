# -*- coding: utf-8 -*-
from django.db     import models
from terapia_model import Terapia


class Bebe (models.Model):
    nombre  = models.CharField(max_length=200)
    terapia = models.ForeignKey(Terapia)

    def __unicode__(self):
        return self.nombre
