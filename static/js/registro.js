var page=1, total_pages=11;
var test;
function showButton(id,btnClass){
	var obj = $("#"+id);
	obj.attr("class","show "+btnClass);
}

function hideButton(id,btnClass){
	var obj = $("#"+id);
	obj.attr("class","hide "+btnClass);
}

function showPanel(id){
	var obj = $("#"+id);
	obj.attr("class","show panel panel-default");
}

function hidePanel(id){
	var obj = $("#"+id);
	obj.attr("class","hide panel panel-default");
}

function nextPanel(){
	hidePanel("panel"+page);
	page++;
	showPanel("panel"+page);
	showButton("btn_previous","previous");
	setProgressBar(Math.round((page-1)*100/total_pages));
	if(page==total_pages){
		hideButton("btn_next","next");
	}
}

function previousPanel(){
	hidePanel("panel"+page);
	page--;
	showPanel("panel"+page);
	showButton("btn_next","next");
	setProgressBar(Math.round((page-1)*100/total_pages));
	if(page==1){
		hideButton("btn_previous","previous");
		//setProgressBar();
		setProgressBar(0);
	}
}

function setPanelVisible(id){
	var i;
	for(i=1; i<=total_pages; i++){
		if(i==id){
			var panel = $("#panel"+i);
			panel.attr("class","show panel panel-default");
		} else {
			var panel = $("#panel"+i);
			panel.attr("class","hide panel panel-default");
		}
	}
	for(i=1; i<=total_pages; i++){
		if(i==id){
			var nav_i = $("#nav"+i);
			if($("#panel"+i).attr("data-error") == "0"){
				nav_i.attr("class","separator current");
			} else {
				nav_i.attr("class","separator current error");
			}
		} else {
			var nav_i = $("#nav"+i);
			if($("#panel"+i).attr("data-error") == "0"){
				nav_i.attr("class","separator current shown");
			} else {
				nav_i.attr("class","separator current shown error");
			}
		}
	}
}

var datepickerValues = {
		changeMonth: true,
		changeYear: true,
		yearRange: "1995:2030",
		// Podemos poner más opciones
		dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá'],
		monthNamesShort: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
		'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
		dateFormat: 'dd/mm/yy'

};
$(function() {

  	/* Creamos un widget de calendario con jquery-ui */

    // $( ".datepicker" ).datepicker(datepickerValues);

	$('body').on('focus',".datepicker", function(){
		$(this).datepicker(datepickerValues);
	});
    //ocultamos los campos que no son necesarios a menos que se realice una eleccion
    $('[oculto=oculto]').parent().hide();
    //$('#id_descripcion_otros').parent().hide();
    //$('#id_descripcion_pregunta_4').parent().hide();


	$('input[type=text], [type=number]').addClass('form-control');
	function value_changed(bool_value,  element){
		if(bool_value)
			element.show();
		else
			element.hide();
	}
    /*	Si ha seleccionado la opcion de otros, entonces mostramos un casillero adicional
     que permite describir de forma especifica la opcion "otros" */
	value_changed($('select[name=descripcion_paciente-disc_molestias]').val() == 'otros', $('#id_descripcion_paciente-otro_disc_molestias').parent());
    $('select[name=descripcion_paciente-disc_molestias]').change(function() {
		value_changed($(this).val() == 'otros', $('#id_descripcion_paciente-otro_disc_molestias').parent());
    });
	value_changed($('input:radio[name=descripcion_paciente-tratamiento]:checked').val() == "True", $("#id_descripcion_paciente-lugar_tratamiento").parent());
	$('input:radio[name=descripcion_paciente-tratamiento]').on('change', function(e) {
		value_changed(e.target.value == "True", $("#id_descripcion_paciente-lugar_tratamiento").parent());
	});
	value_changed($("#id_descripcion_paciente-tipo_terapia_0").is(":checked"), $("#id_terapia-0-tiempo_terapia").parent());
	value_changed($("#id_descripcion_paciente-tipo_terapia_1").is(":checked"), $("#id_terapia-1-tiempo_terapia").parent());
    $('input[name=descripcion_paciente-tipo_terapia').on('click', function(e){
    	if(e.target.value == 1)
			value_changed(e.target.checked, $("#id_terapia-0-tiempo_terapia").parent());
    	else if(e.target.value == 2)
			value_changed(e.target.checked, $("#id_terapia-1-tiempo_terapia").parent());
    });

	value_changed($("#id_descripcion_paciente-areas_dificultad_8").is(":checked"), $("#id_descripcion_paciente-otro_dificultad").parent());
    $('input[name=descripcion_paciente-areas_dificultad]').on('click',function(e) {
		value_changed($("#id_descripcion_paciente-areas_dificultad_8").is(":checked"), $("#id_descripcion_paciente-otro_dificultad").parent());
    });
	value_changed($('select[name=descripcion_paciente-had_convulsion]').val() == 1, $("#id_descripcion_paciente-tipo_crisis").parent());
	value_changed($('select[name=descripcion_paciente-had_convulsion]').val() == 1, $("#id_descripcion_paciente-edad_crisis").parent());
    $('select[name=descripcion_paciente-had_convulsion]').change(function() {
		value_changed($(this).val() == 1, $("#id_descripcion_paciente-tipo_crisis").parent());
		value_changed($(this).val() == 1, $("#id_descripcion_paciente-edad_crisis").parent());
    });

	value_changed($("select[name=descripcion_paciente-tomo_medicamentos]").val() == "True", $("#medicamentos-formset"));
	$("select[name=descripcion_paciente-tomo_medicamentos]").change(function (e) {
		value_changed($(this).val() == "True", $("#medicamentos-formset"));
	});

	value_changed($("#id_historial_madre-enfermedades_previas_3").is(":checked"), $("#id_historial_madre-otra_enf_previa").parent());
	$('input[name=historial_madre-enfermedades_previas]').on('click', function (e) {
        value_changed(e.target.value == "otra" && e.target.checked, $("#id_historial_madre-otra_enf_previa").parent());
	});

	value_changed($("#id_historial_madre-enfermedades_durante_embarazo_4").is(":checked"), $("#id_historial_madre-otra_enf_embarazo").parent());
	$('input[name=historial_madre-enfermedades_durante_embarazo]').on('click', function (e) {
        value_changed(e.target.value == "otra" && e.target.checked, $("#id_historial_madre-otra_enf_embarazo").parent());
	});

	value_changed($("input:radio[name=historial_madre-tuvo_defuncion_fetal]:checked").val() == "True", $("#id_historial_madre-defunciones_fetales").parent());
	$('input:radio[name=historial_madre-tuvo_defuncion_fetal]').change(function (e) {
        value_changed(e.target.value == "True", $("#id_historial_madre-defunciones_fetales").parent());
	});

	value_changed($("input:radio[name=historial_madre-tuvo_hijos_muertos]:checked").val() == "True", $("#id_historial_madre-hijos_nacidos_muertos").parent());
	$('input:radio[name=historial_madre-tuvo_hijos_muertos]').change(function (e) {
        value_changed(e.target.value == "True", $("#id_historial_madre-hijos_nacidos_muertos").parent());
	});

	value_changed($("input:radio[name=historial_madre-uso_anticonceptivo]:checked").val() == "True", $("#id_historial_madre-anticonceptivos").parent());
	$('input:radio[name=historial_madre-uso_anticonceptivo]').change(function (e) {
        value_changed(e.target.value == "True", $("#id_historial_madre-anticonceptivos").parent());
	});

	value_changed($('input:radio[name=gestacion-curso_prenatal]:checked').val() == "True", $("#id_gestacion-lugar_curso_prenatal").parent());
	value_changed($('input:radio[name=gestacion-curso_prenatal]:checked').val() == "True", $("#id_gestacion-carga_horaria").parent());
	$('input:radio[name=gestacion-curso_prenatal]').change(function (e) {
        value_changed(e.target.value == "True", $("#id_gestacion-lugar_curso_prenatal").parent());
        value_changed(e.target.value == "True", $("#id_gestacion-carga_horaria").parent());
	});

	value_changed($('input:radio[name=alimentacion-suplementos]:checked').val() == "True", $("#suplementos-formset"));
	$('input[name=alimentacion-suplementos]').change(function(e){
		value_changed(e.target.value == "True", $("#suplementos-formset"));
	});

	value_changed($('input:radio[name=recien_nacido-hubo_apego_precoz]:checked').val() == "True", $("#id_recien_nacido-tiempo_apego_precoz").parent());
	$('input:radio[name=recien_nacido-hubo_apego_precoz]').change(function(e){
		value_changed(e.target.value == "True", $("#id_recien_nacido-tiempo_apego_precoz").parent());
	});
	value_changed($('input:radio[name=recien_nacido-permanecio_internado]:checked').val() == "True", $("#id_recien_nacido-tiempo_internado").parent());
	value_changed($('input:radio[name=recien_nacido-permanecio_internado]:checked').val() == "True", $("#id_recien_nacido-tipo_contacto").parent());
	$('input:radio[name=recien_nacido-permanecio_internado]').change(function(e){
		value_changed(e.target.value == "True", $("#id_recien_nacido-tiempo_internado").parent());
		value_changed(e.target.value == "True", $("#id_recien_nacido-tipo_contacto").parent());
	});
	value_changed($("#id_recien_nacido-complicaciones_nacimiento_5").is(":checked"), $("#otra-complicacion"));
	$('input[name=recien_nacido-complicaciones_nacimiento]').change(function(e){
		value_changed($("#id_recien_nacido-complicaciones_nacimiento_5").is(":checked"), $("#otra-complicacion"));
	});

	value_changed($("#id_primeros_dias-situaciones_despues_nacimiento_4").is(":checked"), $("#id_primeros_dias-otra_situacion").parent());
	$('input[name=primeros_dias-situaciones_despues_nacimiento]').change(function(e){
		value_changed($("#id_primeros_dias-situaciones_despues_nacimiento_4").is(":checked"), $("#id_primeros_dias-otra_situacion").parent());
	});

	value_changed($("#id_primeros_dias-examenes_2").is(":checked"), $("#id_primeros_dias-otro_examen").parent());
	$('input[name=primeros_dias-examenes]').change(function(e){
		value_changed($("#id_primeros_dias-examenes_2").is(":checked"), $("#id_primeros_dias-otro_examen").parent());
	});

	value_changed($('input:radio[name=primeros_dias-clinica]:checked').val() == "True", $("#id_primeros_dias-clinica_permanencia").parent());
	value_changed($('input:radio[name=primeros_dias-clinica]:checked').val() == "True", $("#id_primeros_dias-dias_permanencia").parent());
	$('input:radio[name=primeros_dias-clinica]').change(function(e){
		value_changed(e.target.value == "True", $("#id_primeros_dias-clinica_permanencia").parent());
		value_changed(e.target.value == "True", $("#id_primeros_dias-dias_permanencia").parent());
	});
	value_changed($('input:radio[name=primeros_dias-icteria]:checked').val() == "True", $("#id_primeros_dias-tratamiento_icteria").parent());
	$('input:radio[name=primeros_dias-icteria]').change(function(e){
		value_changed(e.target.value == "True", $("#id_primeros_dias-tratamiento_icteria").parent());
	});
	value_changed($('input:radio[name=primeros_dias-dormia_toda_noche]:checked').val() == "False", $("#id_primeros_dias-veces_despertar_noche").parent());
	$('input:radio[name=primeros_dias-dormia_toda_noche]').change(function(e){
		value_changed(e.target.value == "False", $("#id_primeros_dias-veces_despertar_noche").parent());
	});
	value_changed($('input:radio[name=alimentacion-lactancia]:checked').val() == "True", $("#id_alimentacion-tiempo_leche_materna").parent());
	value_changed($('input:radio[name=alimentacion-lactancia]:checked').val() == "True", $("#id_alimentacion-motivo_suspencion_lactancia").parent());
	value_changed($('input:radio[name=alimentacion-lactancia]:checked').val() == "True", $("#id_alimentacion-otro_motivo_suspencion_lactancia"));
	$('input:radio[name=alimentacion-lactancia]').change(function(e){
		value_changed(e.target.value == "True", $("#id_alimentacion-tiempo_leche_materna").parent());
		value_changed(e.target.value == "True", $("#id_alimentacion-motivo_suspencion_lactancia").parent());
		value_changed(e.target.value == "True", $("#id_alimentacion-otro_motivo_suspencion_lactancia"));
	});
	value_changed($('input:radio[name=alimentacion-difiere_alimentacion]:checked').val() == "True", $("#id_alimentacion-motivo_cambios_alimentacion").parent());
	$('input:radio[name=alimentacion-difiere_alimentacion]').change(function(e){
		value_changed(e.target.value == "True", $("#id_alimentacion-motivo_cambios_alimentacion").parent());
	});

	value_changed($("#id_alimentacion-motivo_suspencion_lactancia_5").is(":checked"), $("#id_alimentacion-otro_motivo_suspencion_lactancia").parent());
	$('input[name=alimentacion-motivo_suspencion_lactancia]').change(function(e){
		value_changed($("#id_alimentacion-motivo_suspencion_lactancia_5").is(":checked"), $("#id_alimentacion-otro_motivo_suspencion_lactancia").parent());
	});
	value_changed($("#id_alimentacion-afecciones_2").is(":checked"), $("#id_alimentacion-otra_afeccion").parent());
	$('input[name=alimentacion-afecciones]').change(function(e){
		value_changed($("#id_alimentacion-afecciones_2").is(":checked"), $("#id_alimentacion-otra_afeccion").parent());
	});
	value_changed($("#id_alimentacion-enfermedades_3").is(":checked"), $("#id_alimentacion-otra_enfermedad").parent());
	$('input[name=alimentacion-enfermedades]').change(function(e){
		value_changed($("#id_alimentacion-enfermedades_3").is(":checked"), $("#id_alimentacion-otra_enfermedad").parent());
	});
	value_changed($("#id_alimentacion-forma_alimento_7").is(":checked"), $("#id_alimentacion-otra_forma_alimento").parent());
	$('input[name=alimentacion-forma_alimento]').change(function(e){
		value_changed($("#id_alimentacion-forma_alimento_7").is(":checked"), $("#id_alimentacion-otra_forma_alimento").parent());
	});

	value_changed($("#id_familiares_otros-orientacion_a_institucion_4").is(":checked"), $("#id_familiares_otros-otro_orientador").parent());
	$('input[name=familiares_otros-orientacion_a_institucion]').change(function(e){
		value_changed($("#id_familiares_otros-orientacion_a_institucion_4").is(":checked"), $("#id_familiares_otros-otro_orientador").parent());
	});

	$('input:radio[name=familiares_otros-transtorno_hermanos]').change(function(e){
		value_changed(e.target.value == "True", $("#id_familiares_otros-hermano_transtorno").parent());
		value_changed(e.target.value == "True", $("#id_familiares_otros-transtorno").parent());
		value_changed(e.target.value == "True", $("#id_familiares_otros-alteracion_desarrollo").parent());
	});

	var num_hermanos = $('input[name=familiares_otros-numero_hermanos]').val();
	var formCount = $("#id_hermanos_set-TOTAL_FORMS").val();
	if(num_hermanos > 0 && formCount > num_hermanos){
		for( var i=num_hermanos; i < formCount; i++){
			$(".row-hermanos:last").remove();
		}
		$("#id_hermanos_set-TOTAL_FORMS").val(num_hermanos);
	}
	value_changed(num_hermanos != "0" && num_hermanos != '',
				  $("#hermanos-formset"));
	value_changed(num_hermanos != "0" && num_hermanos != '',
				  $("#id_familiares_otros-transtorno_hermanos").parent());

	value_changed(num_hermanos != "0" && num_hermanos != '' &&
				  $('input:radio[name=familiares_otros-transtorno_hermanos]:checked').val() == "True",
				  $("#id_familiares_otros-hermano_transtorno").parent());
	value_changed(num_hermanos != "0" && num_hermanos != '' &&
				  $('input:radio[name=familiares_otros-transtorno_hermanos]:checked').val() == "True",
				  $("#id_familiares_otros-transtorno").parent());
	value_changed(num_hermanos != "0" && num_hermanos != '' &&
				  $('input:radio[name=familiares_otros-transtorno_hermanos]:checked').val() == "True",
				  $("#id_familiares_otros-alteracion_desarrollo").parent());
	$('input[name=familiares_otros-numero_hermanos]').change(function(e){
		var num_hermanos = parseInt(e.target.value);
		var formCount = $("#id_hermanos_set-TOTAL_FORMS").val();
		console.log(num_hermanos);
		console.log(formCount);
		if(num_hermanos != formCount && num_hermanos != 0){
			if(num_hermanos > formCount){
				for(var i = formCount; i < num_hermanos; i++){
					var row = $(".row-hermanos:first").clone(false);
					row.insertAfter(".row-hermanos:last").slideDown(300);
					$(row).find("#id_hermanos_set-0-id").
						attr("name", "hermanos_set-"+i+"-id").
						attr("id", "id_hermanos_set-"+i+"-id").val('');
					$(row).find("#id_hermanos_set-0-nombres").
						attr("name", "hermanos_set-"+i+"-nombres").
						attr("id", "id_hermanos_set-"+i+"-nombres").val('');
					$(row).find("#id_hermanos_set-0-apellidos").
						attr("name", "hermanos_set-"+i+"-apellidos").
						attr("id", "id_hermanos_set-"+i+"-apellidos").val('');
					$(row).find("#id_hermanos_set-0-fecha_nacimiento").
						attr("name", "hermanos_set-"+i+"-fecha_nacimiento").
						attr("id", "id_hermanos_set-"+i+"-fecha_nacimiento").val('').removeClass("hasDatepicker");
				}
			}else if(formCount > num_hermanos){
				for( var i=num_hermanos; i < formCount; i++){
					$(".row-hermanos:last").remove();
				}
			}
			$("#id_hermanos_set-TOTAL_FORMS").val(num_hermanos);
		}

		value_changed(e.target.value != "0" && e.target.value != '', $("#hermanos-formset"));
		value_changed(e.target.value != "0" && e.target.value != '', $("#id_familiares_otros-transtorno_hermanos").parent());
		value_changed(e.target.value != "0" && e.target.value != '' &&
					  $('input:radio[name=familiares_otros-transtorno_hermanos]:checked').val() == "True",
					  $("#id_familiares_otros-hermano_transtorno").parent());
		value_changed(e.target.value != "0" && e.target.value != '' &&
					  $('input:radio[name=familiares_otros-transtorno_hermanos]:checked').val() == "True",
					  $("#id_familiares_otros-transtorno").parent());
		value_changed(e.target.value != "0" && e.target.value != '' &&
					  $('input:radio[name=familiares_otros-transtorno_hermanos]:checked').val() == "True",
					  $("#id_familiares_otros-alteracion_desarrollo").parent());

	});

	function clearForm(form) {
		// iterate over all of the inputs for the form
		// element that was passed in
		$(':input', form).each(function() {
			console.log(this.type);
			var type = this.type;
			var tag = this.tagName.toLowerCase(); // normalize case
			// it's ok to reset the value attr of text inputs,
			// password inputs, and textareas
			if (type == 'text' || type== 'hidden' || type=='numbre' || type == 'password' || tag == 'textarea'){
				this.value = "";
				$(this).attr('value', '');
			}
			// checkboxes and radios need to have their checked state cleared
			// but should *not* have their 'value' changed
			else if (type == 'checkbox' || type == 'radio')
				this.checked = false;
			// select elements need to have their 'selectedIndex' property set to -1
			// (this works for both single and multiple select elements)
			else if (tag == 'select'){
				this.selectedIndex = -1;
				test = $(this);
				$(this).find('option[selected]').removeAttr('selected');
			}
		});
	};
	function addFormset(prefix, regex){
        var formCount = parseInt($("#id_"+prefix+"-TOTAL_FORMS").val());
		var row = $(".formset-"+prefix+":first").clone(false);
		$(row).insertAfter(".formset-"+prefix+":last").slideDown();
		clearForm($(row));
		var row_html = $(row).html();
		$(row).html(row_html.replace(regex, prefix+"-"+formCount));
        $("#id_"+prefix+"-TOTAL_FORMS").val(formCount + 1);
	}
	function deleteFormset(prefix) {
		var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
		if(formCount > 1){
			$(".formset-"+prefix+":last").remove();
			$("#id_" + prefix + "-TOTAL_FORMS").val(formCount - 1);
		}
	}
	$("#btn-add-suplemento").click(function (e) {
        addFormset("suplementos", /suplementos-0/g);
	});

	$("#btn-add-familiar").click(function (e) {
        addFormset("familiares", /familiares-0/g);
	});

	$("#btn-add-medico").click(function (e) {
        addFormset("medico", /medico-0/g);
	});

	$("#btn-add-medicamento").click(function(e){
		addFormset("medicamentos", /medicamentos-0/g);
	});

	$("#btn-delete-suplemento").click(function() {
		deleteFormset("suplementos");
	});

	$("#btn-delete-medicamento").click(function (arg) {
        deleteFormset("medicamentos");
	});



});
