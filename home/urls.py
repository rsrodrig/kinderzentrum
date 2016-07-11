from django.conf.urls import patterns, url
from home.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'proyecto_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',  index_view, name='index_view'),
    url(r'^login/',  login_view, name='login_view'),
    url(r'^logout/$',  logout_view, name='logout_view'),
    url(r'^admin_usuarios/$',  AdminUsuariosView.as_view(), name='admin_usuarios'),
    url(r'^usuarios_permisos/$',  AdminUsuariosPermisosView.as_view(), name='usuarios_permisos'),
    #url(r'^registro/$',  views.registro_view, name='registro_view'),
]
