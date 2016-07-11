from django.conf.urls import url
from registro.views import RegistroView, RegistroEditView, BusquedaPacientesView, PacienteListView, eliminar_paciente_view, paciente_view

urlpatterns =[
    # Examples:
    # url(r'^$', 'proyecto_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$',  views.registro_view, name='registro_view'),
    url(r'^$',  RegistroView.as_view(), name='registro_view'),
    url(r'^eliminar/',  eliminar_paciente_view, name='paciente_delete_view'),
    url(r'pacientes/edit/(?P<id_paciente>[0-9]*)$', RegistroEditView.as_view(), name='paciente_edit'),
    url(r'busqueda_pacientes/', BusquedaPacientesView.as_view(), name='busqueda_pacientes'),
    url(r'pacientes/', PacienteListView.as_view(), name='pacientes-list'),
    url(r'paciente/(?P<id_paciente>[0-9]*)$', paciente_view, name='paciente_view')
]
