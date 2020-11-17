$( document ).ready(function() {
        alert("aqui estoy");
	$.ajax({url: "{% url 'cargarNuevoUsuario' %}",
		success: function () { 
			console.log('Usuarios creados');}
	});
});