from registro.forms import *

def init_historial_madre_form(historial_madre):
    enf_previas = historial_madre.enfermedades_previas.split(',')
    otra_enf_previa = enf_previas[-1] if 'otra' in enf_previas else ''
    enf_emb = historial_madre.enfermedades_durante_embarazo.split(',')
    otra_enf_emb = enf_emb[-1] if 'otra' in enf_emb else ''
    tuvo_defuncion_fetal = "True" if historial_madre.defunciones_fetales > 0 else "False"
    tuvo_hijos_muertos = "True" if historial_madre.hijos_nacidos_muertos > 0 else "False"
    anticonceptivos = historial_madre.anticonceptivos.split(',')
    uso_anticonceptivo = "True" if anticonceptivos[0] != '' else "False"
    initial = {
        'enfermedades_previas': enf_previas,
        'otra_enf_previa': otra_enf_previa,
        'enfermedades_durante_embarazo': enf_emb,
        'otra_enf_embarazo': otra_enf_emb,
        'tuvo_defuncion_fetal': tuvo_defuncion_fetal,
        'tuvo_hijos_muertos': tuvo_hijos_muertos,
        'anticonceptivos': anticonceptivos,
        'uso_anticonceptivo': uso_anticonceptivo
    }
    return HistorialMadreForm(prefix="historial_madre",
                              instance=historial_madre,
                              initial=initial)


def init_gestacion_form(gestacion):
    sentimientos = gestacion.sentimientos.split(',')
    comun = gestacion.comunicacion_bebe.split(',')
    curso_prenatal = "True" if gestacion.lugar_curso_prenatal != '' else "False"
    initial = {
        'curso_prenatal': curso_prenatal,
        'sentimientos': sentimientos,
        'comunicacion_bebe': comun
    }
    return DesarrolloDeLaGestacionForm(prefix="gestacion",
                                       instance=gestacion,
                                       initial=initial)


def init_nacimiento_form(nacimiento):
    complicaciones = nacimiento.complicaciones.split(',')
    metodo = nacimiento.metodo_nacimiento.split(',')
    medicamento = "None" if nacimiento.medicamentos_parto is None else nacimiento.medicamentos_parto
    cordon = "None" if nacimiento.complicaciones_cordon is None else nacimiento.complicaciones_cordon
    initial = {
        'complicaciones': complicaciones,
        'metodo_nacimiento': metodo,
        'medicamentos_parto': medicamento,
        'complicaciones_cordon': cordon
    }
    return NacimientoForm(prefix="nacimiento",
                          instance=nacimiento,
                          initial=initial)


def init_recien_nacido_form(recien_nacido):
    comp_nacimiento = recien_nacido.complicaciones_nacimiento.split(',')
    otra_complicacion = comp_nacimiento[-1] if 'Otro' in comp_nacimiento else ''
    tiempo_internado = recien_nacido.tiempo_internado
    hubo_apego_precoz = 'False' if recien_nacido.tiempo_apego_precoz == RecienNacido.APEGO_PRECOZ_NADA else 'True'
    permanecio_internado = 'False' if tiempo_internado == datetime.timedelta() else 'True'
    initial = {
        'complicaciones_nacimiento': comp_nacimiento,
        'otra_complicacion': otra_complicacion,
        'hubo_apego_precoz': hubo_apego_precoz,
        'permanecio_internado': permanecio_internado
    }
    return RecienNacidoForm(prefix="recien_nacido",
                            instance=recien_nacido,
                            initial=initial)

def init_primeros_dias_form(primeros_dias):
    examenes = primeros_dias.examenes.split(',')
    situaciones = primeros_dias.situaciones_despues_nacimiento.split(',')
    initial = {
        'clinica': 'True' if primeros_dias.clinica_permanencia else 'False',
        'situaciones_despues_nacimiento': situaciones,
        'icteria': 'None' if primeros_dias.icteria is None else primeros_dias.icteria,
        'otro_examen': examenes[-1] if 'Otro' in examenes else '',
        'examenes': examenes,
        'otra_situacion': situaciones[-1] if 'Otro' in situaciones else '',
        'dormia_toda_noche': 'True' if primeros_dias.veces_despertar_noche == 0 else 'False'
    }
    return PrimerosDiasForm(prefix="primeros_dias",
                            initial=initial,
                            instance=primeros_dias)

def init_alimentacion_form(alimentacion, suplementos):
    
    motivo_suspencion = [] if alimentacion.motivo_suspencion_lactancia is None else alimentacion.motivo_suspencion_lactancia.split(',')
    afecciones = alimentacion.afecciones.split(',')
    enfs = alimentacion.enfermedades.split(',')
    forma_alim = alimentacion.forma_alimento.split(',')
    initial = {
        'lactancia': 'True' if motivo_suspencion else 'False',
        'motivo_suspencion_lactancia': motivo_suspencion,
        'otro_motivo_suspencion_lactancia': motivo_suspencion[-1] if 'Otro' in motivo_suspencion else '',
        'afecciones': afecciones,
        'otra_afeccion': afecciones[-1] if 'Otros' in afecciones else '',
        'otra_enfermedad': enfs[-1] if 'Otro' in enfs else '',
        'enfermedades': enfs,
        'otra_forma_alimento': forma_alim[-1] if 'Otro' in forma_alim else '',
        'forma_alimento': forma_alim,
        'difiere_alimentacion': 'True' if alimentacion.motivo_cambios_alimentacion else 'False',
        'suplementos': suplementos
    }
    return AlimentacionForm(prefix="alimentacion",
                            initial=initial,
                            instance=alimentacion)

def init_historia_familiar_form(historia_familiar):
    orientador = historia_familiar.orientacion_a_institucion.split(',')
    initial = {
        'transtorno_hermanos': 'None' if historia_familiar.transtorno_hermanos is None else historia_familiar.transtorno_hermanos,
        'alteracion_desarrollo':'None' if historia_familiar.alteracion_desarrollo is None else historia_familiar.alteracion_desarrollo,
        'otro_orientador': orientador[-1] if 'Otro' in orientador else '',
        'orientacion_a_institucion': orientador[0]
    }
    return  DatosFamiliaresOtrosForm(prefix="familiares_otros",
                                     initial=initial,
                                     instance=historia_familiar)

    
def init_descripcion_form(descripcion):
    areas_dificultad = descripcion.areas_dificultad.split(',')
    otra_area = areas_dificultad[-1] if 'otro' in areas_dificultad else ''
    terapias = descripcion.terapias
    terapias_reh_fisica = terapias.filter(tipo=1)
    terapias_est_temprana = terapias.filter(tipo=2)
    disc_molestias = descripcion.disc_molestias.split(',')
    tipo_terapia = []
    if len(terapias_reh_fisica):
        tipo_terapia.append("1")
    if len(terapias_est_temprana):
        tipo_terapia.append("2")
    if not tipo_terapia:
        tipo_terapia.append("3")
    initial={
        'areas_dificultad': areas_dificultad,
        'otro_dificultad': otra_area,
        'tipo_terapia': tipo_terapia,
        'tiempo_rehab_fisica': terapias_reh_fisica[0].tiempo_terapia if len(terapias_reh_fisica) else '',
        'tiempo_estimu_temprana': terapias_est_temprana[0].tiempo_terapia if len(terapias_est_temprana) else '',
        'disc_molestias': disc_molestias[0],
        'otro_disc_molestias': disc_molestias[-1] if len(disc_molestias) > 1 else ''
    }
    return DescripcionPacienteForm(prefix="descripcion_paciente",
                                   initial=initial,
                                   instance=descripcion,
    )

def init_actividades(actividades, gestacion):
    empty_acts = list(Actividad_Gestacion.ACTIVIDADES_CHOICES)
    for entry in actividades:
        if entry.nombre_actividad in empty_acts:
            empty_acts.remove(entry.nombre_actividad)
    
    initial=[{'nombre_actividad':x} for x in empty_acts]
    return ActividadGestacionFormset(prefix="actividad", initial=initial, instance=gestacion)

def init_situaciones(situaciones, gestacion):
    empty_sits = list(Situacion_Gestacion.SITUACIONES_CHOICES)
    for entry in situaciones:
        if entry.nombre_situacion in empty_sits:
            empty_sits.remove(entry.nombre_situacion)
    initial=[{'nombre_situacion':x} for x in empty_sits]
    return SituacionGestacionFormset(prefix="situacion", initial=initial, instance=gestacion)


