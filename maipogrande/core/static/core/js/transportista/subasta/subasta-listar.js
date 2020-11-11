$( document ).ready(function() {
	// Cargar lista de subastas.
	$.ajax({url: "{% url 'actualizarListaSubastas' %}", data={},
		success: function () { 
			console.log('Subastas cargadas!!');}
	});
});