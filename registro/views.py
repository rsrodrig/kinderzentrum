# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from registro.forms import *
from django.template import RequestContext
from registro.modelos.paciente_model import Paciente
from registro.modelos.familiars_models import DatosFamiliaresOtros, Familiar
from registro.modelos.alimentacion_models import AlimentacionCostumbres
from registro.modelos.recien_nacido_model import RecienNacido
from registro.modelos.medico_model import Medico
from registro.modelos.historial_madre_models import Actividad_Gestacion, Situacion_Gestacion
from registro.modelos.descripcion_models import Terapia
from django.http import HttpResponseRedirect
from django.views.generic import View, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import formset_factory
from init_forms import *

from django.db.models import Q
from django.core import serializers
from django.http.response import HttpResponse
import json
# Create your views here.


@method_decorator(login_required, name="dispatch")
class RegistroView(View):
    template_name = 'registro/registro_ficha_medica.html'
    def get(self, request, *args, **kwargs):
        datos = PacienteForm(prefix="paciente")
        datos_familia = DatosFamiliaresFormset(prefix="familiares", instance=Paciente())
        datos_medico = DatosMedicoFormset(prefix="medico", instance=Paciente())

        historial_madre = HistorialMadreForm(prefix="historial_madre")
        descripcion_paciente = DescripcionPacienteForm(prefix="descripcion_paciente")
        terapia_formset = TerapiaFormset(prefix="terapia", instance=Descripcion(),
                                         initial=[{'tipo': x[0]} for x in Terapia.TERAPIA_CHOICES])
        medicamento_formset = MedicamentoFormset(instance=Descripcion())
        gestacion = DesarrolloDeLaGestacionForm(prefix="gestacion")
        actividad_gestacion = ActividadGestacionFormset(prefix="actividad",
                                                        initial=[{'nombre_actividad':x} for x in Actividad_Gestacion.ACTIVIDADES_CHOICES])
        situacion_gestacion = SituacionGestacionFormset(prefix="situacion",
                                                        initial=[{'nombre_situacion':x} for x in Situacion_Gestacion.SITUACIONES_CHOICES])
        nacimiento = NacimientoForm(prefix="nacimiento")
        datos_recien_nacido = RecienNacidoForm(prefix="recien_nacido",
                                               initial={'tiempo_apego_precoz': RecienNacido.APEGO_PRECOZ_NADA,
                                                        'tipo_contacto': RecienNacido.CONTACTO_NINGUNA})
        primeros_dias = PrimerosDiasForm(prefix="primeros_dias", initial={'icteria': False})
        alimentacion = AlimentacionForm(prefix="alimentacion")
        suplementos_formset = SuplementosFormset(instance=AlimentacionCostumbres())
        datos_familiares = DatosFamiliaresOtrosForm(prefix="familiares_otros")
        hermanos_formset = HermanosFormset(instance=DatosFamiliaresOtros())
        return render(request, self.template_name,
                      {'datos_medico_formset':datos_medico,
                       'datos_familia_formset':datos_familia,
                       'ficha_datos_form':datos,
                       'descripcion_paciente':descripcion_paciente,
                       'terapia_formset': terapia_formset,
                       'medicamento_formset':medicamento_formset,
                       'historial_madre_form': historial_madre,
                       'gestacion': gestacion,
                       'actividad_gestacion':actividad_gestacion,
                       'situacion_gestacion':situacion_gestacion,
                       'nacimiento': nacimiento,
                       'recien_nacido': datos_recien_nacido,
                       'alimentacion': alimentacion,
                       'suplementos_formset': suplementos_formset,
                       'datos_familiares': datos_familiares,
                       'hermanos_formset': hermanos_formset,
                       'primeros_dias': primeros_dias,
                       'pagina_actual':'registro'})


    def post(self, request, *args, **kwargs):
        datos_paciente = PacienteForm(request.POST, prefix="paciente")
        datos_familia = DatosFamiliaresFormset(request.POST, prefix="familiares", instance=Paciente())
        datos_medico = DatosMedicoFormset(request.POST, prefix="medico", instance=Paciente())
        datos_historial_madre = HistorialMadreForm(request.POST, prefix="historial_madre")
        datos_descripcion_paciente = DescripcionPacienteForm(request.POST, prefix="descripcion_paciente")
        terapia_formset = TerapiaFormset(request.POST, prefix="terapia", instance=Descripcion())
        medicamento_formset = MedicamentoFormset(request.POST, instance=Descripcion())
        datos_gestacion = DesarrolloDeLaGestacionForm(request.POST, prefix="gestacion")
        actividad_gestacion = ActividadGestacionFormset(request.POST, prefix="actividad")
        situacion_gestacion = SituacionGestacionFormset(request.POST, prefix="situacion")
        datos_nacimiento = NacimientoForm(request.POST, prefix="nacimiento")
        datos_recien_nacido = RecienNacidoForm(request.POST, prefix="recien_nacido")
        datos_primeros_dias = PrimerosDiasForm(request.POST, prefix="primeros_dias")
        datos_alimentacion = AlimentacionForm(request.POST, prefix="alimentacion")
        suplementos_formset = SuplementosFormset(request.POST, instance=AlimentacionCostumbres())
        datos_familiares = DatosFamiliaresOtrosForm(request.POST, prefix="familiares_otros")
        hermanos_formset = HermanosFormset(request.POST, instance=DatosFamiliaresOtros())
        print "post"

        if (datos_paciente.is_valid() and
            datos_familia.is_valid() and
            datos_medico.is_valid() and
            datos_descripcion_paciente.is_valid() and medicamento_formset.is_valid() and
            terapia_formset.is_valid(datos_descripcion_paciente) and
            datos_historial_madre.is_valid() and
            datos_gestacion.is_valid() and
            datos_nacimiento.is_valid() and
            datos_recien_nacido.is_valid() and
            datos_primeros_dias.is_valid() and
            datos_alimentacion.is_valid() and suplementos_formset.is_valid() and
            datos_familiares.is_valid() and hermanos_formset.is_valid()):


            paciente = datos_paciente.save(commit=False)
            familiares_instances = datos_familia.save(commit=False)
            medicos_instances = datos_medico.save(commit = False)

            descripcion = datos_descripcion_paciente.save()
            #datos_descripcion_paciente.cleaned_data
            medicamentos_instances = medicamento_formset.save(commit=False)
            terapias_instances = terapia_formset.save(commit=False)
            for medicamento in medicamentos_instances:
                medicamento.descripcion = descripcion
                medicamento.save()
            for terapia in terapias_instances:
                terapia.descripcion = descripcion
                terapia.save()

            historial_madre = datos_historial_madre.save()
            gestacion = datos_gestacion.save()
            for actividad_form in actividad_gestacion:
                if actividad_form.is_valid():
                    actividad = actividad_form.save(commit=False)
                    actividad.gestacion = gestacion
                    actividad.save()
            for situacion_form in situacion_gestacion:
                if situacion_form.is_valid():
                    situacion = situacion_form.save(commit=False)
                    situacion.gestacion = gestacion
                    situacion.save()

            nacimiento = datos_nacimiento.save()
            recien_nacido = datos_recien_nacido.save()
            primeros_dias = datos_primeros_dias.save()
            alimentacion = datos_alimentacion.save()
            familiares = datos_familiares.save()


            suplementos = suplementos_formset.save(commit=False)
            for suplemento in suplementos:
                suplemento.alimentacion = alimentacion
                suplemento.save()

            hermanos = hermanos_formset.save(commit=False)
            for hermano in hermanos:
                hermano.datos_familiares = familiares
                hermano.save()

            paciente.descripcion = descripcion
            paciente.historial_madre = historial_madre
            paciente.gestacion = gestacion
            paciente.nacimiento = nacimiento
            paciente.recien_nacido = recien_nacido
            paciente.primeros_dias = primeros_dias
            paciente.alimentacion = alimentacion
            paciente.datos_familiares = familiares

            paciente.save()
            print("Paciente saved")

            for familiar in familiares_instances:
                familiar.paciente = paciente
                familiar.save()

            for medico in medicos_instances:
                medico.paciente = paciente
                medico.save()

            print("Paciente saved")
            return redirect('pacientes-list')


        print "datos is invalid"
        print("Errors paciente:", datos_paciente.errors)
        print("Errors familiares:", datos_familia.errors)
        print("Errors medico:", datos_medico.errors)
        print("Errors descripcion", datos_descripcion_paciente.errors)
        print("Errors historial madre", datos_historial_madre.errors)
        print("Errors gestacion", datos_gestacion.errors)
        print("Errors nacimiento:", datos_nacimiento.errors)
        print("Errors recien_nacido:", datos_recien_nacido.errors)
        print("Errors primeros_dias:", datos_primeros_dias.errors)
        print("Errors alimentacion:", datos_alimentacion.errors)
        print("Errors suplementos", suplementos_formset.errors)
        print("Errors DatosFamiliares", datos_familiares.errors)
        print("Errors Hermano", hermanos_formset.errors)
        return render(request, self.template_name,
                      {'ficha_datos_form': datos_paciente,
                       'datos_familia_formset': datos_familia,
                       'datos_medico_formset': datos_medico,
                       'descripcion_paciente': datos_descripcion_paciente,
                       'terapia_formset': terapia_formset,
                       'medicamento_formset':medicamento_formset,
                       'historial_madre_form': datos_historial_madre,
                       'gestacion': datos_gestacion,
                       'actividad_gestacion':actividad_gestacion,
                       'situacion_gestacion':situacion_gestacion,
                       'nacimiento': datos_nacimiento,
                       'recien_nacido': datos_recien_nacido,
                       'alimentacion': datos_alimentacion,
                       'suplementos_formset': suplementos_formset,
                       'datos_familiares': datos_familiares,
                       'hermanos_formset': hermanos_formset,
                       'primeros_dias': datos_primeros_dias,
                       'pagina_actual': 'registro'
                      })


@method_decorator(login_required, name="dispatch")
class PacienteListView(ListView):
    model = Paciente
    #paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PacienteListView, self).get_context_data(**kwargs)
        context['pagina_actual'] = 'registro'
        return context


@method_decorator(login_required, name="dispatch")
class RegistroEditView(View):
    template_name = 'registro/registro_ficha_medica.html'

    def get(self, request, *args, **kwargs):
        id_paciente = kwargs.get('id_paciente')

        paciente = get_object_or_404(Paciente, pk=id_paciente)
        datos = PacienteForm(prefix="paciente", instance=paciente)
        datos_familia = DatosFamiliaresFormset(prefix="familiares", instance=paciente)
        datos_medico = DatosMedicoFormset(prefix="medico", instance=paciente)
        historial_madre = init_historial_madre_form(paciente.historial_madre)
        descripcion_paciente = init_descripcion_form(paciente.descripcion)
        terapia_formset = TerapiaFormset(instance=paciente.descripcion, prefix="terapia")
        medicamento_formset = MedicamentoFormset(instance=paciente.descripcion)
        gestacion = init_gestacion_form(paciente.gestacion)

        actividad_gestacion = init_actividades(paciente.gestacion.actividad_gestacion_set.all(), paciente.gestacion)
        situacion_gestacion = init_situaciones(paciente.gestacion.situacion_gestacion_set.all(), paciente.gestacion)

        nacimiento = init_nacimiento_form(paciente.nacimiento)
        datos_recien_nacido = init_recien_nacido_form(paciente.recien_nacido)
        primeros_dias = init_primeros_dias_form(paciente.primeros_dias)
        suplementos = paciente.alimentacion.suplementos
        alimentacion = init_alimentacion_form(paciente.alimentacion, 'True' if suplementos.count() else 'False')
        suplementos_formset = SuplementosFormset(instance=paciente.alimentacion)
        datos_familiares = init_historia_familiar_form(paciente.datos_familiares)
        hermanos_formset = HermanosFormset(instance=paciente.datos_familiares)
        return render(request, self.template_name,
                      {'datos_medico_formset':datos_medico,
                       'datos_familia_formset':datos_familia,
                       'ficha_datos_form':datos,
                       'descripcion_paciente':descripcion_paciente,
                       'terapia_formset': terapia_formset,
                       'medicamento_formset':medicamento_formset,
                       'historial_madre_form': historial_madre,
                       'gestacion': gestacion,
                       'actividad_gestacion':actividad_gestacion,
                       'situacion_gestacion':situacion_gestacion,
                       'nacimiento': nacimiento,
                       'recien_nacido': datos_recien_nacido,
                       'alimentacion': alimentacion,
                       'suplementos_formset': suplementos_formset,
                       'datos_familiares': datos_familiares,
                       'hermanos_formset': hermanos_formset,
                       'primeros_dias': primeros_dias,
                       'pagina_actual':'registro'})


    def post(self, request, *args, **kwargs):
        id_paciente = kwargs.get('id_paciente')
        paciente = get_object_or_404(Paciente, pk=id_paciente)
        datos_paciente = PacienteForm(request.POST, prefix="paciente", instance=paciente)
        datos_familia = DatosFamiliaresFormset(request.POST, prefix="familiares", instance=paciente)
        datos_medico = DatosMedicoFormset(request.POST, prefix="medico", instance=paciente)
        datos_historial_madre = HistorialMadreForm(request.POST, prefix="historial_madre", instance=paciente.historial_madre)
        datos_descripcion_paciente = DescripcionPacienteForm(request.POST, prefix="descripcion_paciente", instance=paciente.descripcion)
        terapia_formset = TerapiaFormset(request.POST, instance=paciente.descripcion, prefix="terapia")
        medicamento_formset = MedicamentoFormset(request.POST, instance=paciente.descripcion)
        datos_gestacion = DesarrolloDeLaGestacionForm(request.POST, prefix="gestacion", instance=paciente.gestacion)
        actividad_gestacion = ActividadGestacionFormset(request.POST, prefix="actividad", instance=paciente.gestacion)
        situacion_gestacion = SituacionGestacionFormset(request.POST, prefix="situacion", instance=paciente.gestacion)
        datos_nacimiento = NacimientoForm(request.POST, prefix="nacimiento", instance=paciente.nacimiento)
        datos_recien_nacido = RecienNacidoForm(request.POST, prefix="recien_nacido", instance=paciente.recien_nacido)
        datos_primeros_dias = PrimerosDiasForm(request.POST, prefix="primeros_dias", instance=paciente.primeros_dias)
        datos_alimentacion = AlimentacionForm(request.POST, prefix="alimentacion", instance=paciente.alimentacion)
        suplementos_formset = SuplementosFormset(request.POST, instance=paciente.alimentacion)
        datos_familiares = DatosFamiliaresOtrosForm(request.POST, prefix="familiares_otros", instance=paciente.datos_familiares)
        hermanos_formset = HermanosFormset(request.POST, instance=paciente.datos_familiares)

        if (datos_paciente.is_valid() and
            datos_familia.is_valid() and
            datos_medico.is_valid() and
            datos_descripcion_paciente.is_valid() and medicamento_formset.is_valid() and
            terapia_formset.is_valid(datos_descripcion_paciente) and
            datos_historial_madre.is_valid() and
            datos_gestacion.is_valid() and
            datos_nacimiento.is_valid() and
            datos_recien_nacido.is_valid() and
            datos_primeros_dias.is_valid() and
            datos_alimentacion.is_valid() and suplementos_formset.is_valid() and
            datos_familiares.is_valid() and hermanos_formset.is_valid()):


            paciente = datos_paciente.save()
            familiares_instances = datos_familia.save()
            medicos_instances = datos_medico.save()

            descripcion = datos_descripcion_paciente.save()
            medicamentos_instances = medicamento_formset.save()
            terapias = terapia_formset.save()
            historial_madre = datos_historial_madre.save()
            gestacion = datos_gestacion.save()
            for actividad_form in actividad_gestacion:
                if actividad_form.is_valid():
                    actividad = actividad_form.save()
            for situacion_form in situacion_gestacion:
                if situacion_form.is_valid():
                    situacion = situacion_form.save()

            nacimiento = datos_nacimiento.save()
            recien_nacido = datos_recien_nacido.save()
            primeros_dias = datos_primeros_dias.save()
            alimentacion = datos_alimentacion.save()
            familiares = datos_familiares.save()
            suplementos = suplementos_formset.save()
            hermanos = hermanos_formset.save()

            # for familiar in familiares_instances:
            #     familiar.paciente = paciente
            #     familiar.save()

            # for medico in medicos_instances:
            #     medico.paciente = paciente
            #     medico.save()

            return redirect('pacientes-list')
        #assert False
        print("Errors paciente:", datos_paciente.errors)
        print("Errors familiares:", datos_familia.errors)
        print("Errors medico:", datos_medico.errors)
        print ("Errors descripcion", datos_descripcion_paciente.errors)
        print("Errors historial madre", datos_historial_madre.errors)
        print("Errors gestacion", datos_gestacion.errors)
        print("Errors nacimiento:", datos_nacimiento.errors)
        print("Errors recien_nacido:", datos_recien_nacido.errors)
        print("Errors primeros_dias:", datos_primeros_dias.errors)
        print("Errors alimentacion:", datos_alimentacion.errors)
        print("Errors suplementos", suplementos_formset.errors)
        print("Errors DatosFamiliares", datos_familiares.errors)
        print("Errors Hermano", hermanos_formset.errors)

        return render(request, self.template_name,
                      {'ficha_datos_form': datos_paciente,
                       'datos_familia_formset': datos_familia,
                       'datos_medico_formset': datos_medico,
                       'descripcion_paciente': datos_descripcion_paciente,
                       'terapia_formset': terapia_formset,
                       'medicamento_formset':medicamento_formset,
                       'historial_madre_form': datos_historial_madre,
                       'gestacion': datos_gestacion,
                       'actividad_gestacion':actividad_gestacion,
                       'situacion_gestacion':situacion_gestacion,
                       'nacimiento': datos_nacimiento,
                       'recien_nacido': datos_recien_nacido,
                       'alimentacion': datos_alimentacion,
                       'suplementos_formset': suplementos_formset,
                       'datos_familiares': datos_familiares,
                       'hermanos_formset': hermanos_formset,
                       'primeros_dias': datos_primeros_dias,
                       'pagina_actual': 'registro'
                      })



@login_required
def eliminar_paciente_view(request):
    respuesta = {}
    if request.user.is_authenticated() and request.POST:
        #grupos = request.user.groups.all()
        user = request.user
        registro = user.has_module_perms('registro')
        print "\n\nregistro: ", registro
        if registro:
            paciente_id = request.POST.get("paciente_id")
            print paciente_id, type(paciente_id)
            paciente = Paciente.objects.get(pk=paciente_id)
            deletion = paciente.delete()
            respuesta = {"mensaje": "paciente eliminado", "result": deletion}

        else:
            respuesta = {"error": "No tiene permisos para eliminar éste usuario"}
        #registro = grupos.filter(name='registro').count() == 1
    else:
        respuesta = {"error": "no es posible eliminar usuario"}
    data = json.dumps(respuesta)
    return HttpResponse(data, content_type="application/json")

@login_required
def paciente_view(request, id_paciente=""):
    """Vista para mostrar detalles de un paciente"""
    paciente = get_object_or_404(Paciente, pk=id_paciente)
    assert False
    return render(request, "registro/paciente_view.html",
                  {'pagina_actual': 'paciente_view',
                   'paciente': paciente})


#@method_decorator(login_required, name="dispatch")
class BusquedaPacientesView(View):

    def post(self, request, *args, **kwargs):
      try:
          busqueda = request.POST['busqueda']
          print busqueda
          #busacamos los parecidos
          respuesta = Paciente.objects.filter(Q(nombres__icontains=busqueda)|Q(apellidos__icontains=busqueda))
          #data = serializers.serialize("json", pacientes)
          #return HttpResponse(data, content_type="application/json")
      except MultiValueDictKeyError:
          respuesta = {"mensaje":"busqueda_error"}
          print "error"
      data = serializers.serialize("json", respuesta)
      return HttpResponse(data, content_type="application/json")
