from django.conf.urls import patterns, url
from pago import views

urlpatterns = [
    # Examples:
  url(r'^$', views.index_view, name='pago_index_view'),
  url(r'^pacientes/sugerencias/$', views.patient_suggestions),
  url(r'^pacientes/(?P<patientId>\w{0,50})/$', views.patient_payments),
  # url(r'^pacientes/pdf/$', views.to_pdf),
]
