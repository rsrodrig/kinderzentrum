
function validate() {
    var txt = document.getElementById("datepicker2");
    if(txt.value == "Por favor hacer click aqui para mostrar el calendario y escoger una fecha" || txt.value== null) {
        alert("Por favor escoja una fecha del calendario");
        return false
    } else {
        confirmar();
    }
}

 function confirmar(){ 
     confirmar=confirm(
     	"¿Usted está seguro(a) de los datos que ha seleccionado para la cita:?" + "\n"    	 
     	+ "¿Está seguro(a) de continuar?"
     	); 
     	      
     if (confirmar) 
         // si pulsamos en aceptar, continuamos y guardamos.
         return true;
     else 
         // si pulsamos en cancelar no continuamos.         
         return false;
} 
/*
$(document).ready(function(){ 
  document.getElementById('id_start').name = 'start';
  document.getElementById('id_end').name = 'end';
  document.getElementById('id_date').name = 'date_holder';
  
});
*/