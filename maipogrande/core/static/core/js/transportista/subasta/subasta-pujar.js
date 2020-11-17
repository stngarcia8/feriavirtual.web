const url = $("#pujaForm").attr("url_pujas");
const url_actualizar = $("#pujaForm").attr("url_actualizar_pujas");
const maximo = $("#pujaForm").attr("valor_max");
var myInterval; 

$( document ).ready(function() {
    $("#id_Value").attr("max", maximo);    
    temporizador(true);
});

function temporizador(activate_interval){
    if(activate_interval){
        myInterval = setInterval(function() {
            $.ajax({url: url_actualizar,data: {},
                success: function (data) { 
                $("#id_pujita").html(data);}
            });
        }, 1000);
    } else {
        clearTimeout(myInterval);
    }
}

$("#pujaForm").submit(function() {
    let puja_value = $("#id_Value").val();
    $.ajax({url: url,data: {'value': puja_value},
        success: function (data) { 
        $("#id_pujita").html(data); }
    });
    return false;
});

$('#linkID').on("click", function() {
    temporizador(false);
});
