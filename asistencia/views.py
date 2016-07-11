
import datetime
import json

from django.db import connection
from django.shortcuts import render, render_to_response, get_list_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.core.serializers.json import DjangoJSONEncoder

from models import Terapista, Tipo_terapia

def mostrar_lista_asistencia(request):
    fecha_desde = datetime.datetime.now().strftime("%Y-%m-%d")
    fecha_hasta = datetime.datetime.now().strftime("%Y-%m-%d")
    terapistas = Terapista.objects.all()
    tipo_terapia = Tipo_terapia.objects.all()
    ctx = {'pagina_actual': 'asistencia_paciente', 'terapistas': terapistas,
           'tipo_terapia': tipo_terapia, 'fdesde': fecha_desde, 'fhasta': fecha_hasta}

    return render(request, "asistencia/mostrar_lista.html",ctx)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return list


def consulta_asistencia(request):
    if request.method == "POST" and request.is_ajax:
        print("Esa eh lo muchachos")
        #json_resultados = json.dumps("[]")
        diccionario = generaQuery(request.POST['input_nombre'], int(request.POST['tipo_terapia']),
                                  int(request.POST['terapista']), request.POST['fdesde'],
                                  request.POST['fhasta'])

        json_resultados = json.dumps(diccionario,cls=DjangoJSONEncoder)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type='application/json')


def generaQuery(nombre, terapia, terapista, fdesde, fhasta):
    cursor = connection.cursor()

    if (nombre and not nombre.isspace()):
        nombre_str = "%"+nombre+"%"
    else:
        nombre_str = "%%"

    if (terapia == 0 and terapista == 0):
        cursor.execute('SELECT DISTINCT paciente.id as idPaciente, '
                       'strftime(\'%%d/%%m/%%Y\', cita.fecha_cita) as Fecha, '
                       'cita.hora_inicio as Hora, '
                       '(paciente.nombres || \' \' || paciente.apellidos) as paciente, '
                       '(terapista.nombres || \' \' || terapista.apellidos) as Terapista, '
                       'tipoT.nombre as tipoTerapia, '
                       'case cita.estado '
                       'when \'A\' then \'Agendado\' '
                       'when \'S\' then \'Asistio\' '
                       'when \'N\' then \'No asistio\' '
                       'when \'C\' then \'Cancelado\' '
                       'END as estado '
                       'from asistencia_tipo_terapia as tipoT, registro_paciente as paciente, cita_cita as cita, '
                       'asistencia_terapista as terapista '
                       'where tipoT.id = cita.tipo_terapia_id '
                       'and paciente.id = cita.paciente_id '
                       'and terapista.id = cita.terapista_id '
                       'and cita.fecha_cita BETWEEN %s and %s '
                       'and (paciente.nombres || \' \' || paciente.apellidos) like %s '
                       ,(fdesde, fhasta, nombre_str))
    else:
        if(terapia != 0 and terapista != 0):
            cursor.execute('SELECT paciente.id as idPaciente, '
                           'strftime(\'%%d/%%m/%%Y\', cita.fecha_cita) as Fecha, '
                           'cita.hora_inicio as Hora, '
                           '(paciente.nombres || \' \' || paciente.apellidos) as paciente, '
                           '(terapista.nombres || \' \' || terapista.apellidos) as Terapista, '
                           'tipoT.nombre as tipoTerapia, '
                           'case cita.estado '
                           'when \'A\' then \'Agendado\' '
                           'when \'S\' then \'Asistio\' '
                           'when \'N\' then \'No asistio\' '
                           'when \'C\' then \'Cancelado\' '
                           'END as estado '
                           'from asistencia_tipo_terapia as tipoT, registro_paciente as paciente, cita_cita as cita, '
                           'asistencia_terapista as terapista '
                           'where tipoT.id = cita.tipo_terapia_id '
                           'and paciente.id = cita.paciente_id '
                           'and terapista.id = cita.terapista_id '
                           'and cita.fecha_cita BETWEEN %s and %s '
                           'and (paciente.nombres || \' \' || paciente.apellidos) like %s '
                           'and terapista.id = %s '
                           'and tipoT.id = %s '
                           , (fdesde, fhasta, nombre_str, terapista, terapia))
        else:
            if (terapia == 0 and terapista != 0):
                cursor.execute('SELECT paciente.id as idPaciente, '
                               'strftime(\'%%d/%%m/%%Y\', cita.fecha_cita) as Fecha, '
                               'cita.hora_inicio as Hora, '
                               '(paciente.nombres || \' \' || paciente.apellidos) as paciente, '
                               '(terapista.nombres || \' \' || terapista.apellidos) as Terapista, '
                               'tipoT.nombre as tipoTerapia, '
                               'case cita.estado '
                               'when \'A\' then \'Agendado\' '
                               'when \'S\' then \'Asistio\' '
                               'when \'N\' then \'No asistio\' '
                               'when \'C\' then \'Cancelado\' '
                               'END as estado '
                               'from asistencia_tipo_terapia as tipoT, registro_paciente as paciente, cita_cita as cita, '
                               'asistencia_terapista as terapista '
                               'where tipoT.id = cita.tipo_terapia_id '
                               'and paciente.id = cita.paciente_id '
                               'and terapista.id = cita.terapista_id '
                               'and cita.fecha_cita BETWEEN %s and %s '
                               'and (paciente.nombres || \' \' || paciente.apellidos) like %s '
                               'and terapista.id = %s '
                               , (fdesde, fhasta, nombre_str, terapista))
            else:
                cursor.execute('SELECT paciente.id as idPaciente, '
                               'strftime(\'%%d/%%m/%%Y\', cita.fecha_cita) as Fecha, '
                               'cita.hora_inicio as Hora, '
                               '(paciente.nombres || \' \' || paciente.apellidos) as paciente, '
                               '(terapista.nombres || \' \' || terapista.apellidos) as Terapista, '
                               'tipoT.nombre as tipoTerapia, '
                               'case cita.estado '
                               'when \'A\' then \'Agendado\' '
                               'when \'S\' then \'Asistio\' '
                               'when \'N\' then \'No asistio\' '
                               'when \'C\' then \'Cancelado\' '
                               'END as estado '
                               'from asistencia_tipo_terapia as tipoT, registro_paciente as paciente, cita_cita as cita, '
                               'asistencia_terapista as terapista '
                               'where tipoT.id = cita.tipo_terapia_id '
                               'and paciente.id = cita.paciente_id '
                               'and terapista.id = cita.terapista_id '
                               'and cita.fecha_cita BETWEEN %s and %s '
                               'and (paciente.nombres || \' \' || paciente.apellidos) like %s '
                               'and tipoT.id = %s '
                               , (fdesde, fhasta, nombre_str,terapia))

    print("despues")
    ro = dictfetchall(cursor)
    print("despues2")
    return ro
