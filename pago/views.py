from django.shortcuts import render, render_to_response, redirect

from django.db import connection

import json
from django.http import HttpResponse

from django.core.serializers.json import DjangoJSONEncoder

# import cStringIO as StringIO
# from xhtml2pdf import pisa
# from django.template.loader import get_template
# from django.template import Context
# from cgi import escape

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

# Create your views here.
def index_view(request):
    if request.user.is_authenticated():
        #grupos = request.user.groups.all()
        user = request.user
        '''
        Aqui vamos a colocar las condiciones para que se habiliten las condiciones que el usuario
        va a usar
        '''
        registro = user.has_module_perms('registro')
        #registro = grupos.filter(name='registro').count() == 1
        ctx = {'registro':registro}
        return render(request, 'pago/index.html', ctx)
    else:
        return redirect('/')

def patient_payments(request, patientId):
    fromDate = request.GET.get('from', '0')
    toDate = request.GET.get('to', '0')
    cursor = connection.cursor()
    cursor.execute("select p.id, p.nombres, p.apellidos, t.nombre as terapia_nombre, t.tiempo, c.hora_inicio, c.hora_fin, c.fecha_cita, t.costo from registro_paciente p left join cita_cita c on p.id = c.paciente_id left join asistencia_tipo_terapia t on c.tipo_terapia_id = t.id where p.id = \'{0}\' and c.fecha_cita between date({1}, 'unixepoch') and date({2}, 'unixepoch')".format(patientId, fromDate, toDate))
    row = dictfetchall(cursor)
    return HttpResponse(json.dumps(row, cls=DjangoJSONEncoder), content_type='application/json')

def patient_suggestions(request):
    query = request.GET.get('query', '').strip()
    limit = request.GET.get('limit', '5')
    if (query == ''):
        return HttpResponse(json.dumps([]), content_type='application/json')
    cursor = connection.cursor()
    cursor.execute("select p.id, p.nombres, p.apellidos from registro_paciente p where p.nombres like \'%{0}%\' or p.apellidos like \'%{0}%\' limit {1}".format(query, limit))
    row = dictfetchall(cursor)
    return HttpResponse(json.dumps(row), content_type='application/json')

# def to_pdf(request):
#     patientId = request.GET.get('patientId', '').strip()
#     fromDate = request.GET.get('from', '0')
#     toDate = request.GET.get('to', '0')
#     comment = request.GET.get('comment', '').strip()
#     cursor = connection.cursor()
#     cursor.execute("select p.id, p.nombres, p.apellidos, t.nombre as terapia_nombre, t.tiempo, c.hora_inicio, c.hora_fin, c.fecha_cita, t.costo from registro_paciente p left join cita_cita c on p.id = c.paciente_id left join asistencia_tipo_terapia t on c.tipo_terapia_id = t.id where p.id = \'{0}\' and c.fecha_cita between date({1}, 'unixepoch') and date({2}, 'unixepoch')".format(patientId, fromDate, toDate))
#     row = dictfetchall(cursor)
#     patientCursor = connection.cursor()
#     patientCursor.execute("select p.id, p.nombres, p.apellidos from registro_paciente p where p.id = \'%{0}%\' limit 1".format(patientId))
#     patient = dictfetchall(patientCursor)
#     total = reduce(lambda x, y: x + y, map(lambda x: float(x.costo), row))
#     params = { context: { patient: { nombres: patient[0].nombres, apellidos: patient[0].apellidos }, payments_info: { payments: row, total: total }, comment: comment } }
#     return render_to_pdf('pago/index.html', params)

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
