console.log("connected")

$('#startCalls').on('click', function(){
    console.log("start calls")
    // $.post( "/startCalls", function( res ) {

    // });
    $.post( "/startCalls", { routing: $('#selectRouting').val() } )
        .done(function( res ) {
    });
});

$('#endCalls').on('click', function(){
    console.log("end calls")

    $.post( "/endCalls", { routing: "test" } )
        .done(function( res ) {
    });
});


