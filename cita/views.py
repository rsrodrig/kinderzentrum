# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import View, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import formset_factory
from django.db.models import Q
from django.core import serializers
from django.http.response import HttpResponse
import json
from cita.forms import *
from modelos.cita_model  import Cita
from asistencia.modelos.Terapista_model  import Terapista
from asistencia.modelos.Tipo_terapia_model  import Tipo_terapia
from asistencia.modelos.Terapia__Tipo_terapia_models  import Terapia__Tipo_terapia
from registro.modelos.paciente_model  import Paciente


@method_decorator(login_required, name="dispatch")
class ReservarCitaView(View):
    template_name = 'cita/reservar_cita.html'
    def get(self, request, *args, **kwargs):
        datosCita = CitaForm(prefix="cita")
        return render(request,self.template_name,{'datosCitaForm':datosCita, 'pagina_actual': 'cita'})

    def post(self, request, *args, **kwargs):
        datosCita = CitaForm(request.POST, prefix="cita")
        if (datosCita.is_valid()):
            cita = datosCita.save(commit=False)   
            cita.save()
            print("Cita saved")
            return redirect('citas_list')
        print "datos is invalid"
        print("Errors cita:", datosCita.errors)
        return render(request,self.template_name,{'datosCitaForm':datosCita, 'pagina_actual': 'cita'})


@method_decorator(login_required, name="dispatch")
class CitasListView(ListView):
    model = Cita
    #paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CitasListView, self).get_context_data(**kwargs)
        context['pagina_actual'] = 'cita'
        return context


@method_decorator(login_required, name="dispatch")
class CitaEditView(View):
    template_name = 'cita/reservar_cita.html'
   

    def get(self, request, *args, **kwargs):
        id_cita = kwargs.get('id_cita')
        cita_object = get_object_or_404(Cita, pk=id_cita)    
        datosCita = CitaForm(prefix="cita", instance=cita_object)   
        return render(request, self.template_name,{'datosCitaForm':datosCita, 'pagina_actual': 'cita'})

    def post(self, request, *args, **kwargs):
        id_cita = kwargs.get('id_cita')
        cita_object = get_object_or_404(Cita, pk=id_cita)
        datosCita = CitaForm(request.POST, prefix="cita", instance=cita_object)
        if (datosCita.is_valid()):
            cita = datosCita.save()   
            print("Cita saved")
            return redirect('citas_list')
        #print "datos is invalid"
        print("Errors cita:", datosCita.errors)
        return render(request,self.template_name,{'datosCitaForm':datosCita, 'pagina_actual': 'cita'})        


@login_required
def eliminar_cita_view(request):
    respuesta = {}
    if request.user.is_authenticated() and request.POST:
        #grupos = request.user.groups.all()
        user = request.user
        cita = user.has_module_perms('cita')
        print "\n\ncita: ", cita
        if cita:
            cita_id = request.POST.get("cita_id")
            print cita_id, type(cita_id)
            cita = Cita.objects.get(pk=cita_id)
            deletion = cita.delete()
            respuesta = {"mensaje": "cita eliminada", "result": deletion}

        else:
            respuesta = {"error": "No tiene permisos para eliminar esta cita"}
        #registro = grupos.filter(name='registro').count() == 1
    else:
        respuesta = {"error": "no es posible eliminar la cita"}
    data = json.dumps(respuesta)
    return HttpResponse(data, content_type="application/json")


@login_required
def cita_view(request, id_cita=""):
    """Vista para mostrar detalles de una cita"""
    cita = get_object_or_404(Cita, pk=id_cita)
    assert False
    return render(request, "cita/cita_view.html",
                  {'pagina_actual': 'cita_view',
                   'cita': cita})
    

#@method_decorator(login_required, name="dispatch")
class BusquedaCitasView(View):

    def post(self, request, *args, **kwargs):
      try:
          busqueda = request.POST['busqueda']
          print busqueda
          #busacamos los parecidos
          respuesta = Cita.objects.filter(Q(paciente__icontains=busqueda))
          #data = serializers.serialize("json", pacientes)
          #return HttpResponse(data, content_type="application/json")
      except MultiValueDictKeyError:
          respuesta = {"mensaje":"busqueda_error"}
          print "error"
      data = serializers.serialize("json", respuesta)
      return HttpResponse(data, content_type="application/json")