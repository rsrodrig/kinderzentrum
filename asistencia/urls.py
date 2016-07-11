from django.conf.urls import patterns, url
from asistencia import views
from asistencia.views import mostrar_lista_asistencia





urlpatterns =[
    # Examples:
    # url(r'^$', 'proyecto_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$',  views.registro_view, name='registro_view'),
    url(r'^$',  views.mostrar_lista_asistencia, name='lista_asistencia'),
    url(r'^consulta/$', views.consulta_asistencia, name='consulta_asistencia')
]

