$(".callGroupContainer .phoneCall").css({'width':($(".phoneCall").width()+'px')});

$('.phoneCall').draggable({
     revert: "invalid",
     helper: "clone"
 });

$( ".callGroupContainer, #inactiveCallContainer" ).droppable({
    drop: function( event, ui ) {
            
        //remove hover from dropped box 
        $(this).removeClass('groupHover');

        //get info from dropped call box
        var origin = $(ui.draggable[0]).data('callgroup')
        var phoneNumber = $(ui.draggable[0]).data('phonenumber')
        var routing = $(this).data('roomid')

        console.log("FROM " + origin + " BY " + phoneNumber + " TO " +routing)

        //determine routing of call
        //first get rid of false drops where same box was used
        if (origin != routing) {
            console.log("Hey this box MOVED!");
            //route call appropriately
            if (routing == 'inactiveRoom') {
                action = 'end'
                console.warn("THIS IS ENDING A CALL")
            } else if (origin == 'inactiveRoom') {
                action = 'start'
                console.warn("THIS IS A NEW CALL")
            } else {
                action = 'reroute'
                console.warn("THIS IS REROUTING A CALL")
            }

            //server action
            changeCall(action, phoneNumber, routing, origin)

            //front end action
            moveCall($(ui.draggable), routing)

        } 
    },
    over: function (event, ui) {
        $(this).addClass('groupHover');
    },
    out: function(event, ui) {
        $(this).removeClass('groupHover');
    }
});

$('#startAllCalls').on('click', function(){
    console.log("start all calls")
    var routing = $('#selectRouting').val()
    startAllCalls(routing)
});

$('#endAllCalls').on('click', function(){
    console.log("end all calls")
    endAllCalls()
});


function checkCallStatus() {
    $.get( "/callsStatus").done(function( res ) {

        obj = JSON.parse(res)
        
        setTimeout(checkCallStatus, 500)
    });
    
} 

function startAllCalls(routing) {
    $.post( "/startAllCalls", { routing: routing } )
        .done(function(res) {
            var calls = $('#inactiveCallContainer .phoneCall')

            for (var i = 0; i < calls.length; i++) {
                moveCall($(calls[i]), routing)
            }

    });
}   

function endAllCalls() {
    $.post( "/endAllCalls")
        .done(function(res) {
            console.log(res);
    });
}

function changeCall(action, phoneNumber, routing, origin) {
    $.post( "/callChange", { action: action, phoneNumber: phoneNumber, routing: routing, origin: origin } )
        .done(function( res ) {
            console.log(res);
    });
}

function moveCall(call, routing) {

    var target = $('[data-roomid="' + routing + '"]');
    $(call[0]).data('callgroup', routing)
    call.appendTo(target);
}
