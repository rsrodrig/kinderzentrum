var page=1, total_pages=4;

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

function setProgressBar(prog){
	var bar = $("#progress-bar");
	bar.html(prog+" %");
	bar.attr("style","width: "+prog+"%");	
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
			nav_i.attr("class","current");
		} else {
			var nav_i = $("#nav"+i);
			nav_i.attr("class","");
		}
	}
}

$(function() {

  	/* Creamos un widget de calendario con jquery-ui */

    $( "#datepicker2" ).datepicker({
    	/*showOn: 'button',
    	autoOpen: true,*/
		changeMonth: true,
		changeYear: true,
		yearRange: "2000:2030",
		dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá'],
		monthNamesShort: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
		'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
		dateFormat: 'yy-mm-dd',
		showButtonPanel: true,  
		closeText: 'Cerrar', 
		currentText: 'Hoy',
		beforeShow: function(){    
           $(".ui-datepicker").css('font-size', 15) 
        }   
		//mas opciones
    });

});

