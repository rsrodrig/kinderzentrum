from django.contrib import admin
from asistencia.models import Tipo_terapia,Terapista,Terapia__Tipo_terapia

admin.site.register(Tipo_terapia)
admin.site.register(Terapista)
admin.site.register(Terapia__Tipo_terapia)
