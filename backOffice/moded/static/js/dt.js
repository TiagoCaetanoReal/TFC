//  Chamar botao em JS
$(document).ready( function () {
    $('#tabela').DataTable();
 } );

//  funcao butao
$(".Apagar").click(function(e){
   e.preventDefault();
   let DadosReserva={
       id: $(this).attr("id"),
       action: "Apagar"
       
   }
   console.log(DadosReserva);
   $.ajax({
       url: '/usersPage',
       type: 'POST',
       data: DadosReserva,
       async: false,
       success: function(data){
           alert(data.message);
           console.log(data.message)
           window.location.reload()
       },
       error: function(data){
           alert(data);
       }
   })
})

$(".ApagarB").click(function(e){
    e.preventDefault();
    let DadosReserva={
        id: $(this).attr("id")
        
    }
    console.log(DadosReserva);
    $.ajax({
        url: '/ridePage',
        type: 'POST',
        data: DadosReserva,
        async: false,
        success: function(data){
            alert(data.message);
            console.log(data.message)
            window.location.reload()
        },
        error: function(data){
            alert(data);
        }
    })
 })

 $(".ApagarR").click(function(e){
    e.preventDefault();
    let DadosReserva={
        id: $(this).attr("id")
        
    }
    console.log(DadosReserva);
    $.ajax({
        url: '/reservaPage',
        type: 'POST',
        data: DadosReserva,
        async: false,
        success: function(data){
            alert(data.message);
            console.log(data.message)
            window.location.reload()
        },
        error: function(data){
            alert(data);
        }
    })
 })


 // editar user ajax + button 

 $(".Editar").click(function(e){
    e.preventDefault();
    let DadosUser={
        id: $(this).attr("id"),
        action: "Editar"
    }
    console.log(DadosUser);
    $.ajax({
        url: '/usersPage',
        type: 'POST',
        data: DadosUser,
        async: false,
        success: function(data){
            $('#id').val(data.id),
            $('#name').val(data.name),
            $('#usern').val(data.student_number),
            $('#phone').val(data.phone_number)
           
            //console.log(data.message)
            //window.location.reload()
        },
        error: function(data){
            alert(data);
        }
    })
 })
 $("#editsave").submit(function(e){
    e.preventDefault();

    let DadosUser={
        action: "editsave",
        id:$('#id').val(),
        name:  $('#name').val(),
        student_number: $('#usern').val(),
        phone_number: $('#phone').val(),
        password: $('#password').val()
    }
    
    
    console.log(DadosUser);
    $.ajax({
        url: '/usersPage',
        type: 'POST',
        data: DadosUser,
        async: false,
        success: function(data){
            
            alert(data.message)
            //console.log(data.message)
            window.location.reload()
        },
        error: function(data){
            alert(data);
        }
    })
 })

 $(".ApagarV").click(function(e){
    e.preventDefault();
    let DadosReserva={
        id: $(this).attr("id")
        
    }
    console.log(DadosReserva);
    $.ajax({
        url: '/vehiclesPage',
        type: 'POST',
        data: DadosReserva,
        async: false,
        success: function(data){
            alert(data.message);
            console.log(data.message)
            window.location.reload()
        },
        error: function(data){
            alert(data);
        }
    })
 })