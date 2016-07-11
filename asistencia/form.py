# -*- encoding: utf-8 -*-
from django import forms

class ConsultaAsistenciaForm (forms.Form):
    nombre = forms.CharField()