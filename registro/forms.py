# -*- encoding: utf-8 -*-
import datetime
from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.forms import inlineformset_factory, BaseInlineFormSet, formset_factory, modelformset_factory
from registro.modelos.historial_madre_models import HistorialMadre, Gestacion, Actividad_Gestacion, Situacion_Gestacion, CHOICES_TRIMESTRES
from modelos.nacimiento_models import Nacimiento
from modelos.familiars_models import Familiar, Hermano, DatosFamiliaresOtros
from modelos.paciente_model import Paciente
from modelos.alimentacion_models import AlimentacionCostumbres, SuplementoAlimenticio
from modelos.primeros_dias_model import PrimerosDias
from modelos.recien_nacido_model import RecienNacido
from modelos.medico_model import Medico
from modelos.paciente_model import Paciente
from modelos.descripcion_models import Descripcion, Terapia, Medicamento

#from django.contrib.auth.models import User
CHOICES_SI_NO_DES = [(True, 'Si'), (False, 'No'), (None, 'Desconoce')]

CHOICES_SI_NO = ((True, "Si"), (False, "No"))

DATEFORMAT = '%d/%m/%Y'

# class MyForm(ModelForm):
#     """
#     Extend from this form so your widgets have an 'error' class if there's
#     an error on the field.
#     """
#     def __init__(self, *args, **kwargs):
#         super(MyForm, self).__init__(*args, **kwargs)
#         if self.errors:
#             for f_name in self.fields:
#                 if f_name in self.errors:
#                     classes = self.fields[f_name].widget.attrs.get('class', '')
#                     classes += 'has-error'
#                     self.fields[f_name].widget.attrs['class'] = classes

class PacienteForm(ModelForm):
    # grupo_sanguineo = forms.ChoiceField(choices=Paciente.GRUPO_SANGUINEO_CHOICES,
    #                                     widget=forms.Select(attrs={'class':'form-control', 'required': 'required'}))
    error_css_class = 'has-error'
    fecha_nacimiento = forms.DateField(input_formats=[DATEFORMAT],
                                       label='Fecha de nacimiento',
                                       widget=forms.DateInput(attrs=
                                                              {
                                                                  'class':'datepicker form-control',
                                                                  'required': 'required'
                                                              },
                                                              format=DATEFORMAT))
    class Meta:
        model = Paciente
        fields = ['nombres',
                  'apellidos',
                  'sexo',
                  'lugar_nacimiento',
                  'fecha_nacimiento',
                  'nacionalidad',
                  'grupo_sanguineo']
        widgets = {'sexo': forms.RadioSelect(choices=Paciente.SEXO_CHOICES),
                   'grupo_sanguineo': forms.Select(attrs={'class':'form-control', 'required': 'required'})
        }


class DatosFamiliaresForm(ModelForm):
    class Meta:
        model = Familiar
        fields = ['parentesco', 'nombres', 'apellidos', 'nivel_estudio', 'direccion','telefonos',
                  'empresa', 'direccion_empresa', 'jornada']
        widgets = {'nivel_estudio': forms.Select(choices=Familiar.NIVEL_ESTUDIO_CHOICES,attrs={'class':'form-control'}),
                   'jornada': forms.Select(choices=Familiar.JORNADA_TRABAJO_CHOICES, attrs={'class': 'form-control'})
                }


class DatosMedicoForm(ModelForm):
    class Meta:
        model = Medico
        # fields = '__all__'
        exclude = ('paciente',)


class DescripcionPacienteForm(ModelForm):
    otro_disc_molestias = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control adjust', 'placeholder': 'Especifique quién descubrió las molestias'}),
                                          required=False
    )
    tipo_terapia = forms.MultipleChoiceField(required=True, choices=Terapia.TERAPIA_CHOICES, widget=forms.CheckboxSelectMultiple, label="Que tipo de terapia realiza?")
    areas_dificultad = forms.MultipleChoiceField(required=False, choices=Descripcion.DIFICULTADES_OPTIONS,
                                                 widget=forms.CheckboxSelectMultiple,
                                                 label="Ha presentado su hijo(a) algun tipo de dificultades en estas áreas? marque todas las opciones que desee.")
    otro_dificultad = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Especifique'}),
                                      label="Otras dififultades",
                                      required=False)
    tomo_medicamentos = forms.ChoiceField(choices=CHOICES_SI_NO,
                                          widget=forms.Select(attrs={'class':'form-control'}),
                                          label="¿Tomó medicamentos?")
    class Meta:
        model = Descripcion
        fields = ['preocupacion','disc_molestias','otro_disc_molestias',
                  'edad_disc_molestia','tratamiento',
                  'lugar_tratamiento','tipo_terapia',
                  'areas_dificultad','otro_dificultad',
                  'limitaciones_movimiento','had_convulsion',
                  'tipo_crisis','edad_crisis','tomo_medicamentos']
        widgets = {'preocupacion':forms.TextInput(attrs={'class':'adjust', 'placeholder': 'Especifique'}),
                    'disc_molestias': forms.Select(choices=model.DESCUBRIO_MOLESTIAS_OPTIONS, attrs={'class':'form-control'}),
                   'tratamiento': forms.RadioSelect(choices=CHOICES_SI_NO),
                   'limitaciones_movimiento': forms.Select(choices=model.LIMITACIONES_OPTIONS, attrs={'class':'form-control'}),
                   'had_convulsion': forms.Select(choices=model.LIMITACIONES_OPTIONS, attrs={'class':'form-control'})
                   }
    def clean(self):
        cleaned_data = super(DescripcionPacienteForm, self).clean()
        disc_molestias = cleaned_data.get('disc_molestias')
        tratamiento = cleaned_data.get('tratamiento')
        areas_dificultad = cleaned_data.get('areas_dificultad')
        had_convulsion = cleaned_data.get('had_convulsion')
        tomo_medicamentos = cleaned_data.get('tomo_medicamentos')
        if disc_molestias == 'otros':
            if not cleaned_data.get('otro_disc_molestias'):
                self.add_error('otro_disc_molestias', 'Debe llenar este campo')
        if tratamiento:
            if not cleaned_data.get('lugar_tratamiento'):
                self.add_error('lugar_tratamiento', 'Debe llenar este campo')

        if areas_dificultad and 'otro' in areas_dificultad:
            if not cleaned_data.get('otro_dificultad'):
                self.add_error('otro_dificultad', 'Debe llenar este campo')
        if had_convulsion == 1:
            if not cleaned_data.get('tipo_crisis'):
                self.add_error('tipo_crisis', 'Debe llenar este campo')
            if not cleaned_data.get('edad_crisis'):
                self.add_error('edad_crisis', 'Debe llenar este campo')

    def save(self):
        model = super(DescripcionPacienteForm, self).save(commit=False)
        areas_dificultad = self.cleaned_data.get('areas_dificultad')
        if self.cleaned_data.get('disc_molestias') == 'otros':
            model.disc_molestias = 'otros,'+self.cleaned_data.get('otro_disc_molestias')
        if not self.cleaned_data.get('tratamiento'):
            model.lugar_tratamiento = ''
        if self.cleaned_data.get('had_convulsion') != 1:
            model.tipo_crisis = ''
            model.edad_crisis = None
        if areas_dificultad and 'otro' in areas_dificultad:
            areas_dificultad.append(self.cleaned_data.get('otro_dificultad'))
        if not areas_dificultad is None:
            model.areas_dificultad = ','.join(areas_dificultad)

        model.save()
        return model


class HistorialMadreForm(ModelForm):

    enfermedades_previas = forms.MultipleChoiceField(choices=HistorialMadre.CHOICES_ENFERMEDADES_PREVIAS,
                                                     widget=forms.CheckboxSelectMultiple, required=False,
                                                     label="Indique si durante el embarazo sufrió algunas de las siguientes enfermedades")
    otra_enf_previa = forms.CharField(required=False,
                                      widget=forms.TextInput(attrs={'placeholder':'Especifique otra enfermedad'}))
    enfermedades_durante_embarazo = forms.MultipleChoiceField(choices=HistorialMadre.CHOICES_ENFERMEDADES_ANTES_EMBARA,
                                                              widget=forms.CheckboxSelectMultiple, required=False,
                                                              label="Indique si antes del embarazo sufrió algunas de las siguientes enfermedades")
    otra_enf_embarazo = forms.CharField(required=False,
                                        widget=forms.TextInput(attrs={'placeholder':'Especifique otra enfermedad'}))
    tuvo_defuncion_fetal = forms.ChoiceField(choices=CHOICES_SI_NO,
                                             widget=forms.RadioSelect,
                                             label="¿Tuvo usted alguna defunción fetal antes de concebir al bebé/niño(a) que trae a consulta?")
    tuvo_hijos_muertos = forms.ChoiceField(choices=CHOICES_SI_NO,
                                           widget=forms.RadioSelect,
                                             label="¿Ha tenido hijos muertos?")
    uso_anticonceptivo =  forms.ChoiceField(choices=CHOICES_SI_NO,
                                            widget=forms.RadioSelect,
                                            label="¿Utilizó algún método anticonceptivo antes de estar embarazada?")
    anticonceptivos = forms.MultipleChoiceField(choices=HistorialMadre.CHOICES_ANTICONCEPTIVO,
                                                widget=forms.CheckboxSelectMultiple, required=False,
                                                label="¿Cuál método anticonceptivo?")
    class Meta:
        model = HistorialMadre
        fields = ('enfermedades_previas', 'otra_enf_previa',
                  'enfermedades_durante_embarazo', 'otra_enf_embarazo',
                  'enfermedad_cronica', 'tuvo_defuncion_fetal',
                  'defunciones_fetales', 'tuvo_hijos_muertos',
                  'hijos_nacidos_muertos', 'hijos_nacidos_vivos',
                  'embarazos', 'uso_anticonceptivo', 'anticonceptivos',
                  'enfermedades_antes_concepcion')

    def clean(self):
        cleaned_data = super(HistorialMadreForm, self).clean()
        if 'otra' in cleaned_data.get('enfermedades_previas') and not cleaned_data.get('otra_enf_previa'):
            self.add_error('otra_enf_previa', 'Debe llenar este campo')
        if 'otra' in cleaned_data.get('enfermedades_durante_embarazo') and not cleaned_data.get('otra_enf_embarazo'):
            self.add_error('otra_enf_embarazo', 'Debe llenar este campo')
        if cleaned_data.get('tuvo_defuncion_fetal', '') == "True" and cleaned_data.get('defunciones_fetales', 0) <= 0:
            self.add_error('defunciones_fetales', 'Debe llenar este campo con un valor mayor a 0')
        if cleaned_data.get('tuvo_hijos_muertos', '') == "True" and cleaned_data.get('hijos_nacidos_muertos', 0) <= 0:
            self.add_error('hijos_nacidos_muertos', 'Debe llenar este campo con un valor mayor a 0')
        if cleaned_data.get('hijos_nacidos_vivos', 0) < 1:
            self.add_error('hijos_nacidos_vivos', 'Debe llenar este campo con un valor mayor a 0')
        if cleaned_data.get('embarazos', 0) < 1:
            self.add_error('embarazos', 'Debe llenar este campo con un valor mayor a 0')
        if cleaned_data.get('uso_anticonceptivo', '') == "True" and not cleaned_data.get('anticonceptivos'):
            self.add_error('anticonceptivos', 'Debe seleccionar alguna opción')


    def save(self):
        model = super(HistorialMadreForm, self).save(commit=False)
        enf_previas = self.cleaned_data.get('enfermedades_previas')
        enf_emb = self.cleaned_data.get('enfermedades_durante_embarazo')
        anticonceptivos = self.cleaned_data.get('anticonceptivos')
        uso_anticonceptivo = self.cleaned_data.get('uso_anticonceptivo', '')
        if 'otra' in enf_previas:
            enf_previas.append(self.cleaned_data.get('otra_enf_previa'))
        if 'otra' in enf_emb:
            enf_emb.append(self.cleaned_data.get('otra_enf_embarazo'))
        if self.cleaned_data.get('tuvo_hijos_muertos', 'False') == "False":
            model.hijos_nacidos_muertos = 0
        if self.cleaned_data.get('tuvo_defuncion_fetal', 'False') == "False":
            model.defunciones_fetales = 0

        model.anticonceptivos = ','.join(anticonceptivos) if anticonceptivos and uso_anticonceptivo == "True" else ''
        model.enfermedades_previas = ','.join(enf_previas) if enf_previas else ''
        model.enfermedades_durante_embarazo = ','.join(enf_emb) if enf_emb else ''
        model.save()

        return model


class DesarrolloDeLaGestacionForm(ModelForm):
    curso_prenatal = forms.ChoiceField(choices=CHOICES_SI_NO, widget=forms.RadioSelect, label="¿Asistió a algún curso prenatal?")
    vacuna_tetano = forms.ChoiceField(choices=CHOICES_SI_NO, widget=forms.RadioSelect, label="¿Se vacunó usted contra el tetano durante el embarazo?")
    sentimientos = forms.MultipleChoiceField(required=False, choices=Gestacion.CHOICES_SENTIMIENTOS,
                                             widget=forms.CheckboxSelectMultiple,
                                             label="¿Qué sintió cuando se enteró que estaba embarazada? Marque todas las opciones que desee")
    comunicacion_bebe = forms.MultipleChoiceField(choices=Gestacion.CHOICES_COMUNICA_BEBE,
                                                  widget=forms.CheckboxSelectMultiple,
                                                  label="¿Cómo se comunicaba con el bebe? Marque todas las opciones que dese.")
    class Meta:
        model = Gestacion
        fields = ['sentimientos','momento_desc_embarazo','num_embarazo','curso_prenatal',
                  'lugar_curso_prenatal','carga_horaria','vacuna_tetano','comunicacion_bebe',
                  ]
        widgets = {'momento_desc_embarazo': forms.Select(choices=model.CHOICES_MOMENTO,attrs={'class':'form-control'})}
    def clean(self):
        cleaned_data = super(DesarrolloDeLaGestacionForm, self).clean()
        curso_prenatal = cleaned_data.get('curso_prenatal', '')
        if curso_prenatal == "True":
            if not cleaned_data.get('lugar_curso_prenatal'):
                self.add_error('lugar_curso_prenatal', 'Debe llenar este campo')
            if not cleaned_data.get('carga_horaria'):
                self.add_error('carga_horaria', 'Debe llenar este campo')
        if self.cleaned_data.get('num_embarazo', 0) < 1:
            self.add_error('num_embarazo', 'Debe ingresar un valor mayor a 0')

    def save(self):
        model = super(DesarrolloDeLaGestacionForm, self).save(commit=False)
        curso_prenatal = self.cleaned_data.get('curso_prenatal')
        sentimientos = self.cleaned_data.get('sentimientos')
        if curso_prenatal != "True":
            model.lugar_curso_prenatal = ''
            model.carga_horaria = ''
        if not sentimientos is None:
            model.sentimientos = ','.join(sentimientos)
        model.comunicacion_bebe = ','.join(self.cleaned_data.get('comunicacion_bebe'))
        model.save()
        return model


class SituacionGestacionForm(ModelForm):
    class Meta:
        model = Situacion_Gestacion
        fields=['id', 'nombre_situacion','periodo']
        widgets={'periodo': forms.Select(choices=CHOICES_TRIMESTRES,attrs={'class':'form-control'})}


class ActividadGestacionForm(ModelForm):
    class Meta:
        model = Actividad_Gestacion
        fields=['id', 'nombre_actividad','periodo']
        widgets={'periodo': forms.Select(choices=CHOICES_TRIMESTRES,attrs={'class':'form-control'})}


class NacimientoForm(ModelForm):
    gemelar = forms.ChoiceField(choices=CHOICES_SI_NO, widget=forms.RadioSelect, label="¿Fue embarazo gemelar?")
    medicamentos_parto = forms.ChoiceField(choices=CHOICES_SI_NO_DES, widget=forms.RadioSelect, label="¿Se le administró medicamentos o inyección durante el parto?")
    complicaciones_cordon = forms.ChoiceField(choices=CHOICES_SI_NO_DES, widget=forms.RadioSelect, label="¿Hubieron complicaciones en el cordón umbilical?")
    complicaciones = forms.MultipleChoiceField(choices=Nacimiento.COMPLICACIONES_CHOICES,
                                               widget=forms.CheckboxSelectMultiple,
                                               label="¿Tuvo usted complicaciones?")
    metodo_nacimiento = forms.MultipleChoiceField(choices=Nacimiento.METODO_NACIMIENTO_CHOICES,
                                                  widget=forms.CheckboxSelectMultiple,
                                                  label="¿Cómo nación el bebé? Marque todas las opciones que necesite")

    class Meta:
        model = Nacimiento
        fields = '__all__'
        widgets = {
            'tipo_lugar_nacimiento': forms.RadioSelect(choices=Nacimiento.TIPO_LUGAR_NACIMIENTO_CHOICES),
            'manera_inicio_parto': forms.RadioSelect(choices=Nacimiento.MANERA_INICIO_PARTO_CHOICES),
            'tipo_ruptura_fuente': forms.RadioSelect(choices=Nacimiento.TIPO_RUPTURA_FUENTE_CHOICES),
            'primera_parte_cuerpo': forms.RadioSelect(choices=Nacimiento.PRIMERA_PARTE_CUERPO_CHOICES),
            'medicamentos_parto': forms.RadioSelect(choices=CHOICES_SI_NO_DES),
            'complicaciones_cordon': forms.RadioSelect(choices=CHOICES_SI_NO_DES),
        }

    def clean(self):
        cleaned_data = super(NacimientoForm, self).clean()
        lugar = cleaned_data.get('tipo_lugar_nacimiento', -1)
        if lugar != 3 and not cleaned_data.get('nombre_lugar_nacimiento', ''):
            self.add_error('nombre_lugar_nacimiento', 'Debe llenar este campo')
        if cleaned_data.get('semana_gestacion', 0) < 25:
            self.add_error('semana_gestacion', 'Ingrese una semana válida')

    def save(self):
        model = super(NacimientoForm, self).save(commit=False)
        model.complicaciones = ','.join(self.cleaned_data.get('complicaciones'))
        model.metodo_nacimiento = ','.join(self.cleaned_data.get('metodo_nacimiento'))
        model.save()
        return model


class RecienNacidoForm(ModelForm):
    hubo_apego_precoz = forms.ChoiceField(choices=CHOICES_SI_NO, widget=forms.RadioSelect, label="¿Hubo apego precoz(le pusieron a su bebé encima del pecho cuando nació)?")
    permanecio_internado = forms.ChoiceField(choices=CHOICES_SI_NO, widget=forms.RadioSelect, label="¿Tuvo el bebé que permanecer internado cuando nació?")
    otra_complicacion = forms.CharField(required=False)

    complicaciones_nacimiento = forms.MultipleChoiceField(required=False, choices=RecienNacido.COMPLICACIONES_CHOICES,
                                                          widget=forms.CheckboxSelectMultiple,
                                                          label="¿El niño(a) tuvo alguna de éstas complicaciones al nacer?")

    class Meta:
        model = RecienNacido
        fields = ['edad_madre', 'edad_padre', 'peso', 'tamanio', 'diametro_encefalico', 'apgar_score', 'complicaciones_nacimiento', 'otra_complicacion', 'hubo_apego_precoz', 'tiempo_apego_precoz', 'tiempo_sostener_bebe','permanecio_internado', 'tiempo_internado', 'tipo_contacto', 'primera_lactancia']
        widgets = {
            'apgar_score': forms.RadioSelect(choices=RecienNacido.APGAR_CHOICES),
            'tiempo_apego_precoz': forms.RadioSelect(choices=RecienNacido.APEGO_PRECOZ_CHOICES),
            'tiempo_sostener_bebe': forms.RadioSelect(choices=RecienNacido.SOSTENER_BEBE_CHOICES),
            'tipo_contacto': forms.RadioSelect(choices=RecienNacido.CONTACTO_CHOICES),
            'primera_lactancia': forms.RadioSelect(choices=RecienNacido.PRIMERA_LACTANCIA_CHOICES)
        }

    def clean(self):
        cleaned_data = super(RecienNacidoForm, self).clean()
        hubo_apego_precoz = cleaned_data.get('hubo_apego_precoz')
        permanecio_internado = cleaned_data.get('permanecio_internado')
        complicaciones = cleaned_data.get("complicaciones_nacimiento")
        edad_madre = cleaned_data.get('edad_madre')
        edad_padre = cleaned_data.get('edad_padre')
        if  edad_madre and (edad_madre <= 12 or edad_madre > 50):
            self.add_error('edad_madre', 'Ingrese una edad válida')
        if  edad_padre and (edad_padre <= 12 or edad_padre > 80):
            self.add_error('edad_padre', 'Ingrese una edad válida')
        if cleaned_data.get('diametro_encefalico', 0) <= 0:
            self.add_error('diametro_encefalico', 'Ingrese un valor válido')
        if cleaned_data.get('peso', 0) <= 0:
            self.add_error('peso', 'Ingrese un valor válido')
        if cleaned_data.get('tamanio', 0) <= 0:
            self.add_error('tamanio', 'Ingrese un valor válido')
        if hubo_apego_precoz == 'True':
            tiempo =  cleaned_data.get('tiempo_apego_precoz')
            if not tiempo or tiempo == RecienNacido.APEGO_PRECOZ_NADA:
                self.add_error('tiempo_apego_precoz', "Debe llenar este campo con valor distinto a Nada")
        if permanecio_internado == 'True':
            if not cleaned_data.get('tiempo_internado'):
                self.add_error('tiempo_internado', "Debe llenar este campo")
            if not cleaned_data.get('tipo_contacto'):
                self.add_error('tipo_contacto', "Debe llenar este campo")
        if 'Otro' in complicaciones:
            if not cleaned_data.get('otra_complicacion'):
                self.add_error('otra_complicacion', "Debe llenar este campo")

    def save(self):
        model = super(RecienNacidoForm, self).save(commit=False)
        if self.cleaned_data.get('hubo_apego_precoz') == 'False':
            model.tiempo_apego_precoz = RecienNacido.APEGO_PRECOZ_NADA
        if self.cleaned_data.get('permanecio_internado') == 'False':
            model.tiempo_internado = datetime.timedelta()
            model.tipo_contacto = RecienNacido.CONTACTO_NINGUNA
        complicaciones = self.cleaned_data.get("complicaciones_nacimiento", [])
        if 'Otro' in complicaciones:
            complicaciones.append(self.cleaned_data.get("otra_complicacion"))
        model.complicaciones_nacimiento = ','.join(complicaciones) if complicaciones else ''
        model.save()
        return model


class PrimerosDiasForm(ModelForm):
    clinica = forms.ChoiceField(choices=CHOICES_SI_NO, widget=forms.RadioSelect, label="¿El niño(a) tuvo que permanecer después de su nacimiento en una clínica u hospital?")
    dormia_toda_noche = forms.ChoiceField(choices=CHOICES_SI_NO, widget=forms.RadioSelect, label="¿El recién nacido dormía toda la noche?")
    otra_situacion = forms.CharField(required=False)
    otro_examen = forms.CharField(required=False)
    examenes = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=PrimerosDias.EXAMENES_CHOICES,
                                         label="¿Le realizaron al recién nacido algún tipo de exámen?",
                                         required=False)
    situaciones_despues_nacimiento = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=PrimerosDias.SITUACIONES_CHOICES,
                                         label="¿Presentó su bebé alguna de éstas situaciones después del nacimiento?",
                                         required=False)

    class Meta:
        model = PrimerosDias
        fields = ['clinica',
                  'clinica_permanencia',
                  'dias_permanencia',
                  'situaciones_despues_nacimiento',
                  'otra_situacion',
                  'icteria',
                  'tratamiento_icteria',
                  'examenes',
                  'otro_examen',
                  'dormia_toda_noche',
                  'veces_despertar_noche',
                  'lugar_dormir',
                  'descripcion_bebe',
                  'descripcion_madre'
        ]
        widgets = {
            'icteria': forms.RadioSelect(choices=CHOICES_SI_NO_DES),
            'situaciones_despues_nacimiento': forms.CheckboxSelectMultiple(choices=PrimerosDias.SITUACIONES_CHOICES),
            'lugar_dormir': forms.RadioSelect(choices=PrimerosDias.LUGAR_DORMIR_CHOICES)
        }
    def save(self):
        model = super(PrimerosDiasForm, self).save(commit=False)
        situaciones = self.cleaned_data.get('situaciones_despues_nacimiento')
        examenes = self.cleaned_data.get('examenes')
        if self.cleaned_data.get("clinica") == 'False':
            model.dias_permanencia = None
            model.clinica_permanencia = ''
        if not self.cleaned_data.get("icteria"):
            model.tratamiento_icteria = ''
        if self.cleaned_data.get('dormia_toda_noche') == 'True':
            model.veces_despertar_noche = 0
        if situaciones and "Otro" in situaciones:
            situaciones.append(self.cleaned_data.get('otra_situacion'))
        if examenes and "Otro" in examenes:
            examenes.append(self.cleaned_data.get('otro_examen'))
        if not examenes is None:
            model.examenes = ','.join(examenes)
        if not situaciones is None:
            model.situaciones_despues_nacimiento = ','.join(situaciones)
        model.save()
        return model

    def clean(self):
        cleaned_data = super(PrimerosDiasForm, self).clean()
        clinica = cleaned_data.get('clinica')
        dormia_toda_noche = cleaned_data.get('dormia_toda_noche')
        icteria = cleaned_data.get('icteria')
        situaciones = cleaned_data.get('situaciones_despues_nacimiento')
        examenes = cleaned_data.get('examenes')
        if icteria:
            if not cleaned_data.get('tratamiento_icteria'):
                self.add_error('tratamiento_icteria', "Debe llenar este campo")
        if clinica == 'True':
            if not cleaned_data.get('clinica_permanencia'):
                self.add_error('clinica_permanencia', "Debe llenar este campo")
            if not cleaned_data.get('dias_permanencia'):
                self.add_error('dias_permanencia', "Debe llenar este campo con valor mayor a 0")
        if dormia_toda_noche == 'False':
            veces = cleaned_data.get('veces_despertar_noche')
            if not veces or veces <= 0:
                self.add_error('veces_despertar_noche', "Debe llenar este campo con valor mayor a 0")
        if situaciones and "Otro" in situaciones:
            if not cleaned_data.get('otra_situacion'):
                self.add_error('otra_situacion', "Debe llenar este campo")
        if examenes and "Otro" in examenes:
            if not cleaned_data.get('otro_examen'):
                self.add_error('otro_examen', "Debe llenar este campo")


class AlimentacionForm(ModelForm):
    lactancia = forms.ChoiceField(choices=CHOICES_SI_NO, widget=forms.RadioSelect,
                                  label="¿Recibió lactancia materna?")
    motivo_suspencion_lactancia = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                            choices=AlimentacionCostumbres.MOTIVO_SUSPENSION_CHOICES,
                                                            label="¿Por qué suspendió la leche materna?", required=False)
    tiempo_leche_materna = forms.ChoiceField(widget= forms.RadioSelect,choices=AlimentacionCostumbres.TIEMPO_LACTANCIA_CHOICES,
                                             label="¿Cuánto tiempo recibió leche materna?", required=False)
    afecciones = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices = AlimentacionCostumbres.AFECCIONES_CHOICES,
                                           label="Indique si el niño ha tenido una de las siguientes afecciones",
                                           required=False)
    enfermedades = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices = AlimentacionCostumbres.ENFERMEDADES_CHOICES,
                                             label="¿Cuáles de las siguientes enfermedades ha presentado el niño(a)? Marque todas las que necesite",
                                             required=False)
    forma_alimento = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices = AlimentacionCostumbres.FORMA_ALIMENTO_CHOICES,
                                               label="¿Cuál era la forma o preparación del alimento?")
    apetito = forms.ChoiceField(widget=forms.RadioSelect, choices=AlimentacionCostumbres.APETITO_CHOICES, label="¿Cómo es el apetito del niño?")
    difiere_alimentacion = forms.ChoiceField(choices=CHOICES_SI_NO, widget=forms.RadioSelect, label="¿Difiere la alimentación del fin de semana de los demás días?")
    suplementos = forms.ChoiceField(choices=CHOICES_SI_NO, widget=forms.RadioSelect, label="¿Consumía suplementos alimenticios?")
    otro_motivo_suspencion_lactancia = forms.CharField(required=False)
    otra_afeccion = forms.CharField(required=False)
    otra_enfermedad = forms.CharField(required=False)
    otra_forma_alimento = forms.CharField(required=False)

    class Meta:
        model = AlimentacionCostumbres
        fields = '__all__'
        fields = ['lactancia', 'tiempo_leche_materna', 'motivo_suspencion_lactancia',
                  'otro_motivo_suspencion_lactancia', 'afecciones', 'otra_afeccion', 'enfermedades',
                  'otra_enfermedad', 'edad_alimentacion_complementaria', 'forma_alimento',
                  'otra_forma_alimento', 'lugar_desayuno', 'lugar_comida_media_manana',
                  'lugar_almuerzo', 'lugar_comida_media_tarde', 'lugar_cena', 'lugar_comida_otro',
                  'alimento_preferido', 'alimento_rechazado', 'suplementos', 'apetito',
                  'difiere_alimentacion', 'motivo_cambios_alimentacion']

    def clean(self):
        cleaned_data = super(AlimentacionForm, self).clean()
        lactancia = cleaned_data.get('lactancia')
        difiere_alimentacion = cleaned_data.get('difiere_alimentacion')
        motivo_suspencion_lactancia = cleaned_data.get('motivo_suspencion_lactancia')
        afecciones = cleaned_data.get('afecciones')
        enfermedades = cleaned_data.get('enfermedades')
        forma_alimento = cleaned_data.get('forma_alimento')
        if lactancia == 'True':
            if not cleaned_data.get('tiempo_leche_materna'):
                self.add_error('tiempo_leche_materna', "Debe llenar este campo")
            if not cleaned_data.get('motivo_suspencion_lactancia'):
                self.add_error('motivo_suspencion_lactancia', "Debe llenar este campo")
        if difiere_alimentacion == 'True':
            if not cleaned_data.get('motivo_cambios_alimentacion'):
                self.add_error('motivo_cambios_alimentacion', "Debe llenar este campo")
        if motivo_suspencion_lactancia and "Otro" in motivo_suspencion_lactancia:
            if not cleaned_data.get('otro_motivo_suspencion_lactancia'):
                self.add_error('otro_motivo_suspencion_lactancia', "Debe llenar este campo")
        if afecciones and "Otros" in afecciones:
            if not cleaned_data.get('otra_afeccion'):
                self.add_error('otra_afeccion', "Debe llenar este campo")
        if enfermedades and "Otro" in enfermedades:
            if not cleaned_data.get('otra_enfermedad'):
                self.add_error('otra_enfermedad', "Debe llenar este campo")
        if forma_alimento and "Otro" in forma_alimento:
            if not cleaned_data.get('otra_forma_alimento'):
                self.add_error("otra_forma_alimento", "Debe llenar este campo")

    def save(self):
        model = super(AlimentacionForm, self).save(commit=False)
        motivo_suspencion_lactancia = self.cleaned_data.get('motivo_suspencion_lactancia')
        afecciones = self.cleaned_data.get('afecciones')
        enfermedades = self.cleaned_data.get('enfermedades')
        forma_alimento = self.cleaned_data.get('forma_alimento')
        if self.cleaned_data.get('lactancia') == 'False':
            model.tiempo_leche_materna = None
            model.motivo_suspencion_lactancia = None
            model.otro_motivo_suspencion_lactancia = ''
        elif motivo_suspencion_lactancia:
            model.motivo_suspencion_lactancia = ','.join(motivo_suspencion_lactancia)
        if self.cleaned_data.get('difiere_alimentacion') == 'False':
            model.motivo_cambios_alimentacion = ''
        if motivo_suspencion_lactancia and "Otro" in motivo_suspencion_lactancia:
            motivo_suspencion_lactancia.append(self.cleaned_data.get('otro_motivo_suspencion_lactancia'))
        if afecciones and "Otros" in afecciones:
            afecciones.append(self.cleaned_data.get('otra_afeccion'))
        if enfermedades and "Otro" in enfermedades:
            enfermedades.append(self.cleaned_data.get('otra_enfermedad'))
        if forma_alimento and "Otro" in forma_alimento:
            forma_alimento.append(self.cleaned_data.get('otra_forma_alimento'))
        if not afecciones is None:
            model.afecciones = ','.join(afecciones)
        if not enfermedades is None:
            model.enfermedades = ','.join(enfermedades)
        if forma_alimento:
            model.forma_alimento = ','.join(forma_alimento)
        model.save()
        return model


class DatosFamiliaresOtrosForm(ModelForm):

    orientacion_a_institucion = forms.ChoiceField(choices=DatosFamiliaresOtros.ORIENTACION_CHOICES,
                                                  widget=forms.RadioSelect, label="Quién los orientó a ésta institución?")
    otro_orientador = forms.CharField(required=False)
    class Meta:
        model = DatosFamiliaresOtros
        fields = '__all__'
        widgets = {
            'transtorno_hermanos': forms.RadioSelect(choices=CHOICES_SI_NO_DES),
            'alteracion_desarrollo': forms.RadioSelect(choices=CHOICES_SI_NO_DES)
        }
    def clean(self):
        cleaned_data = super(DatosFamiliaresOtrosForm, self).clean()
        numero_hermanos = cleaned_data.get('numero_hermanos')
        orientador = cleaned_data.get('orientacion_a_institucion')
        if orientador and orientador == DatosFamiliaresOtros.ORIENTACION_OTRO:
            if not cleaned_data.get('otro_orientador'):
                self.add_error('otro_orientador', "Debe llenar este campo")
        if numero_hermanos > 0:
            trans_hermanos = cleaned_data.get('transtorno_hermanos')
            if trans_hermanos:
                hermano_transtorno = cleaned_data.get("hermano_transtorno")
                if not hermano_transtorno:
                    self.add_error('hermano_transtorno', "Debe llenar este campo")
                elif hermano_transtorno > numero_hermanos or hermano_transtorno <= 0:
                    self.add_error('hermano_transtorno', "No tiene tantos hermanos")
                if not cleaned_data.get('transtorno'):
                    self.add_error('transtorno', "Debe llenar este campo")

    def save(self):
        model = super(DatosFamiliaresOtrosForm, self).save(commit=False)
        orientador = self.cleaned_data.get('orientacion_a_institucion')
        numero_hermanos = self.cleaned_data.get('numero_hermanos')
        if orientador == DatosFamiliaresOtros.ORIENTACION_OTRO:
            model.orientacion_a_institucion = "Otro,"+self.cleaned_data.get('otro_orientador')
        if numero_hermanos <= 0:
            model.transtorno_hermanos = None
            model.hermano_transtorno = 0
            model.transtorno = ''
        model.save()
        return model


# class SuplementoFormset(BaseInlineFormSet):
#     def __init__(self, *args, **kwargs):
#         super(SuplementoFormset, self).__init__(*args, **kwargs)
#         for form in self.forms:
#             form.empty_permitted = False

SuplementosFormset = inlineformset_factory(AlimentacionCostumbres, SuplementoAlimenticio,
                                           fields='__all__',
                                           can_delete=False,
                                           extra=1)

# class HermanoFormset(BaseInlineFormSet):
#     def __init__(self, *args, **kwargs):
#         super(HermanoFormset, self).__init__(*args, **kwargs)
#         for form in self.forms:
#             form.empty_permitted = False

class HermanoForm(ModelForm):
    fecha_nacimiento = forms.DateField(input_formats=[DATEFORMAT],
                                       label='Fecha de nacimiento',
                                       widget=forms.DateInput(attrs={
                                           'class':'datepicker form-control'},
                                                              format=DATEFORMAT))
    class Meta:
        model = Hermano
        fields = '__all__'

HermanosFormset = inlineformset_factory(DatosFamiliaresOtros, Hermano,
                                        fields='__all__',
                                        form=HermanoForm,
                                        #formset=HermanoFormset,
                                        can_delete=False)
MedicamentoFormset = inlineformset_factory(Descripcion, Medicamento,
                                           fields='__all__',
                                           can_delete=False,
                                           extra=1)
ActividadGestacionFormset = inlineformset_factory(Gestacion, Actividad_Gestacion, form=ActividadGestacionForm, max_num=5, extra=5)

SituacionGestacionFormset = inlineformset_factory(Gestacion, Situacion_Gestacion, form=SituacionGestacionForm, max_num=12, extra=12)

DatosMedicoFormset = inlineformset_factory(Paciente, Medico, form=DatosMedicoForm, extra=1, can_delete=False, exclude=('paciente',))
DatosFamiliaresFormset = inlineformset_factory(Paciente, Familiar, form=DatosFamiliaresForm, extra=2, can_delete=False, exclude=('paciente',))


class TerapiasForm(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(TerapiasForm, self).__init__(*args, **kwargs)
        self.tipos = []

    def is_valid(self, descripcion=None):
        if descripcion:
            self.tipos = descripcion.cleaned_data.get('tipo_terapia')
        valid = True
        if '1' in self.tipos:
            valid = valid and self.forms[0].is_valid()
        if '2' in self.tipos:
            valid = valid and self.forms[1].is_valid()
        return valid

    def clean(self):
        super(TerapiasForm, self).clean()

    def save(self, commit=True):
        models = []
        if '1' in self.tipos:
            models.append(self.forms[0].save(commit=commit))
        if '2' in self.tipos:
            self.forms[1].save()
            models.append(self.forms[1].save(commit=commit))
        return models


TerapiaFormset = inlineformset_factory(Descripcion, Terapia, fields='__all__', can_delete=False, max_num=2, extra=2,
                                       widgets={'tipo': forms.TextInput}, formset=TerapiasForm)

data_formsets = {'form-TOTAL_FORMS': '2',
                 'form-INITIAL_FORMS': '0',
                 'form-MAX_NUM_FORMS': ''}
