from django.contrib import admin

# Register your models here.
from modelos.medico_model import *
from modelos.alimentacion_models import *
from modelos.descripcion_models import *
from modelos.paciente_model import *
from modelos.historial_madre_models import *
from modelos.nacimiento_models import *
from modelos.familiars_models import *
from modelos.primeros_dias_model import *
from modelos.recien_nacido_model import *

#alimentacion_models
admin.site.register(SuplementoAlimenticio)
admin.site.register(AlimentacionCostumbres)

#descripcion_models
admin.site.register(Descripcion)
admin.site.register(Terapia)
admin.site.register(Medicamento)

#familiars_models
admin.site.register(Familiar)
admin.site.register(DatosFamiliaresOtros) 
admin.site.register(Hermano)

#historial_madre_models
admin.site.register(HistorialMadre)
admin.site.register(Gestacion) 
admin.site.register(Actividad_Gestacion) 
admin.site.register(Situacion_Gestacion)

#paciente_model
admin.site.register(Paciente)

#medico_models
admin.site.register(Medico)

#nacimiento_models
admin.site.register(Nacimiento)

#primeros_dias_models
admin.site.register(PrimerosDias)

#recien_nacido_models
admin.site.register(RecienNacido)




