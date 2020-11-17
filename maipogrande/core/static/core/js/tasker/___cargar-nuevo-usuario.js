$( document ).ready(function() {
    $.ajax({url: "{% url 'cargarNuevoUsuario' %}"});
});