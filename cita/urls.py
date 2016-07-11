from django.conf.urls import patterns, url
from cita.views import ReservarCitaView, CitasListView, BusquedaCitasView, eliminar_cita_view, CitaEditView, cita_view

urlpatterns =[ 
    # Examples:
    # url(r'^$', 'proyecto_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$',  views.registro_view, name='registro_view'),
    #url(r'^$',  CitaView.as_view(), name='cita_view'),
    #url(r'reservarcita/',  ReservarCitaView.as_view(), name='reservar_cita_view'),
    url(r'^$',  ReservarCitaView.as_view(), name='reservar_cita_view'),
    url(r'^eliminar/',  eliminar_cita_view, name='cita_delete_view'),
    #url(r'citas/edit/(?P<id_cita>[0-9]+)/$', CitaEditView.as_view(), name='cita_edit'),
    url(r'citas/edit/(?P<id_cita>[0-9]*)$', CitaEditView.as_view(), name='cita_edit'),    
    url(r'busqueda_citas/', BusquedaCitasView.as_view(), name='busqueda_citas'),
    url(r'citas/', CitasListView.as_view(), name='citas_list'),    
    url(r'cita/(?P<id_cita>[0-9]*)$', cita_view, name='cita_view')
]